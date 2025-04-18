import rclpy
from rclpy.node import Node
from rcl_interfaces.msg import ParameterDescriptor, SetParametersResult
from geometry_msgs.msg import Vector3Stamped

import ADS1x15

class AnglePublisher(Node):
    def __init__(self):
        super().__init__('angle_publisher')
        self.publisher_ = self.create_publisher(Vector3Stamped, '/drone/angles', 10)
        
        # Declare parameters with descriptors for better documentation
        timer_descriptor = ParameterDescriptor(
            description='Frequency of angle publishing in Hz')
        self.declare_parameter('timer_frequency', 70.0, timer_descriptor)  # default 2.0 Hz
        
        # Get the initial parameter value
        timer_freq = self.get_parameter('timer_frequency').value
        timer_period = 1.0 / timer_freq  # Convert frequency to period
        
        # Create timer using the period
        self.timer = self.create_timer(timer_period, self.timer_callback)
        
        # Set up parameter change callback
        self.add_on_set_parameters_callback(self.parameters_callback)
        
        # Initialize ADS1x15
        self.ads = ADS1x15.ADS1115(1, 0x48)
        self.ads.setGain(self.ads.PGA_6_144V)
        self.ads.setDataRate(self.ads.DR_ADS111X_860) 
        self.ads.setMode(self.ads.MODE_SINGLE)
        
        self.get_logger().info(f'Angle publisher initialized with frequency: {timer_freq} Hz')

    def read_angles(self):
        """Read angles from the ADS1x15."""
        try:
            angle1 = self.ads.readADC(0)
            angle2 = self.ads.readADC(1)
            return angle1, angle2
        except Exception as e:
            self.get_logger().error(f"Error reading angles: {str(e)}")
            return None, None

    def timer_callback(self): 
        """Timer callback to publish angles."""
        msg = Vector3Stamped()
        msg.header.stamp = self.get_clock().now().to_msg()
        msg.header.frame_id = 'base_link'
        angle1, angle2 = self.read_angles()
        
        if angle1 is not None and angle2 is not None:
            msg.vector.x = float(angle1)
            msg.vector.y = float(angle2)
            msg.vector.z = 0.0
            self.publisher_.publish(msg)
            self.get_logger().debug(f'Published angles: x={angle1}, y={angle2}')
    
    def parameters_callback(self, params):
        """Callback for parameter changes."""
        for param in params:
            if param.name == 'timer_frequency':
                new_freq = param.value
                if new_freq <= 0:
                    self.get_logger().error(f"Invalid frequency value: {new_freq}. Must be positive.")
                    return SetParametersResult(successful=False, reason=f"Invalid frequency value: {new_freq}. Must be positive.")
                
                # Update timer with new frequency
                new_period = 1.0 / new_freq
                self.timer.timer_period_ns = int(new_period * 1e9)  # Convert to nanoseconds
                self.get_logger().info(f"Updated timer frequency to {new_freq} Hz (period: {new_period:.6f}s)")
        
        return SetParametersResult(successful=True, reason="Parameter updated successfully.")

def main(args=None):
    rclpy.init(args=args)
    node = AnglePublisher()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        node.get_logger().info('Keyboard interrupt, shutting down.')
    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from std_msgs.msg import Float32
import cv2
from cv_bridge import CvBridge
import numpy as np
import threading
import time
import tensorflow as tf 

class UcracksNode(Node):
    def __init__(self):
        super().__init__('ucracks_node')
        
        self.bridge = CvBridge()
        self.cap = cv2.VideoCapture(0)  # Rasp Camera
        
        # Load the segmentation model
        self.model = tf.keras.models.load_model('model_cracks.keras')
        
        # Publishers - Mask and percentage
        self.mask_publisher = self.create_publisher(Image, '/ucracks/mask', 10)
        self.crack_percentage_publisher = self.create_publisher(Float32, '/ucracks/crack_percentage', 10)
        
        # Previous masks for comparison
        self.previous_mask = None
        self.capture_thread = None
        self.running = True
        
        self.get_logger().info('Ucracks Node initialized')
        
        # Capture thread (separate thread to avoid bottlenecking Raspberri)
        self.capture_thread = threading.Thread(target=self.capture_loop)
        self.capture_thread.daemon = True
        self.capture_thread.start()
    
    def capture_loop(self):
        while self.running:
            ret, frame = self.cap.read()
            
            if ret:
                # Run segmentation algorithm on frame
                mask = self.segment_image(frame)
                
                # Publish mask
                mask_msg = self.bridge.cv2_to_imgmsg(mask, encoding='mono8')
                self.mask_publisher.publish(mask_msg)
                
                # Calculate and publish crack percentage
                crack_percentage = self.calculate_crack_percentage(mask)
                percentage_msg = Float32()
                percentage_msg.data = float(crack_percentage)
                self.crack_percentage_publisher.publish(percentage_msg)
                
                self.get_logger().info(f'Crack percentage: {crack_percentage:.2f}%')
                
                # Update previous mask
                self.previous_mask = mask.copy()
            
            time.sleep(3)  # Wait 3 seconds before next capture
    
    def segment_image(self, frame):
        """Apply your segmentation algorithm using the loaded model"""
        # Preprocess the frame for the model
        input_frame = cv2.resize(frame, (self.model.input_shape[1], self.model.input_shape[2]))
        input_frame = np.expand_dims(input_frame, axis=0) / 255.0  # Normalize
        
        # Get the model prediction
        prediction = self.model.predict(input_frame)
        mask = (prediction[0] > 0.5).astype(np.uint8) * 255  # Threshold to create binary mask
        
        return mask
    
    def calculate_crack_percentage(self, current_mask):
        """Compare current mask with previous mask to detect cracks"""
        if self.previous_mask is None:
            return 0.0
        
        # Find white pixels in current mask
        current_white = cv2.countNonZero(current_mask)
        
        # Find white pixels in previous mask
        previous_white = cv2.countNonZero(self.previous_mask)
        
        # Calculate difference
        total_pixels = current_mask.shape[0] * current_mask.shape[1]
        
        # Percentage of white pixels in similar places
        intersection = cv2.bitwise_and(current_mask, self.previous_mask)
        intersection_white = cv2.countNonZero(intersection)
        
        crack_percentage = (intersection_white / total_pixels) * 100
        
        return crack_percentage
    
    def destroy_node(self):
        """Clean up resources"""
        self.running = False
        if self.capture_thread:
            self.capture_thread.join()
        self.cap.release()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)
    node = UcracksNode()
    
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
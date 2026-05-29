#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import rclpy
from rclpy.node import Node
from rclpy.qos import QoSProfile
import RPi.GPIO as GPIO
import time
from nav_msgs.msg import Odometry

import tf_transformations
import numpy as np

# pin setup
Moisture_pin = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(Moisture_pin, GPIO.IN)

def callback_moisture():
    if GPIO.input(Moisture_pin):
        # In case there's a chance of moisture being detected, publish a message to topic /moisture
        pass
    else:
        pass


class Node_sensor(Node):

    def __init__(self):
        super().__init__('grid_mapping')

        q_profile_odom   = QoSProfile(depth=50)

        self.sub_odom = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_cb,
            q_profile_odom)
        
        self.moisture_cb = self.create_publisher(GPIO.add_event_detect(
            Moisture_pin, GPIO.RISING, 
            callback=callback_moisture
            ))

            

        self.timer = self.create_timer(0.5, self.publish_position)

        self.get_logger().info('Nó de mapeamento inicializado.')

    def odom_cb(self, msg: Odometry):
        """Guarda posição (x,y) e orientação (yaw) do robô."""
        self.x = msg.pose.pose.position.x
        self.y = msg.pose.pose.position.y

        q = msg.pose.pose.orientation
        _, _, self.yaw = tf_transformations.euler_from_quaternion(
            [q.x, q.y, q.z, q.w]
        )
        self.pose_ok = True

    def __del__(self):
        self.get_logger().info('Nó finalizado com sucesso.')


# ==============================================================
def main(args=None):
    rclpy.init(args=args)
    node = Node_sensor()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
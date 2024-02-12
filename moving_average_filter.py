#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float64
from sensor_msgs.msg import JointState

class moving_average_filter():

    def __init__(self, buffer_size):
        self.buffer_size = buffer_size
        self.buffer_list = list(0 for i in range(buffer_size))
    
    def apply_filter(self, current_data):
        new_list = list(0 for i in range(self.buffer_size))
        for i in range(1, self.buffer_size):
            new_list[i-1] = self.buffer_list[i]
        new_list[-1] = current_data
        self.buffer_list = new_list
    
    def get_average_value(self):
        total = 0
        for i in self.buffer_list:
            total = total + i
        new_data = total / self.buffer_size
        return new_data
            

MAV = moving_average_filter(10)

rospy.init_node('moving_average_filter_node')
publisher = rospy.Publisher("/moving_average_filter", Float64, queue_size=1)
rate = rospy.Rate(50)

def listener_callback(msg):
    
    data = msg.position[4]
    MAV.apply_filter(data)
    new_data = MAV.get_average_value()
    
    my_msg = Float64()
    my_msg.data = new_data
    publisher.publish(my_msg)
    
    print("publishing...")
        
rospy.Subscriber("/joint_states", JointState, listener_callback)
rospy.spin()

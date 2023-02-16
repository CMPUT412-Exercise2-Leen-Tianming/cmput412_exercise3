#!/usr/bin/env python3

import os
import rospy
from duckietown.dtros import DTROS, NodeType
from sensor_msgs.msg import CompressedImage
import numpy as np
import cv2


HOST_NAME = os.environ["VEHICLE_NAME"]


class MySubscriberNode(DTROS):
    def __init__(self, node_name):
        super(MySubscriberNode, self).__init__(node_name=node_name, node_type=NodeType.GENERIC)
        self.sub = rospy.Subscriber(f'{HOST_NAME}/camera_node/image/compressed', CompressedImage, self.callback)
        self.pub = rospy.Publisher(f'{HOST_NAME}/compressed', CompressedImage, queue_size=10)
        self.image = None
        self.seq = 0
    
    def callback(self, msg):
        # how to decode compressed image
        # reference: http://wiki.ros.org/rospy_tutorials/Tutorials/WritingImagePublisherSubscriber
        compressed_image = np.frombuffer(msg.data, np.uint8)
        im = cv2.imdecode(compressed_image, cv2.IMREAD_COLOR)
        rospy.loginfo(f'subscriber: image size is {np.shape(im)}')
        # cv2.imwrite('/home/duckie/image.jpg', im)
        self.image = im
    
    def run(self):
        rate = rospy.Rate(10)  # in Hz
        while not rospy.is_shutdown():
            if self.image is not None:
                load = load_calibration()
                camera_intrinsic_dict =  load.readYamlFile("camera_intrinsic.yaml")

                camera_matrix = np.array(camera_intrinsic_dict["camera_matrix"]["data"]).reshape(3,3)
                distort_coeff = np.array(camera_intrinsic_dict["distortion_coefficients"]["data"]).reshape(5,1)

                width = self.image.shape[1]
                height = self.image.shape[0]

                newmatrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix,distortion_coeff,(width,height),1, (width,height))
                # new_image= cv2.undistort(img,camera_intrinsic_matrix,distortion_coeff,newmatrix)


                dst = cv2.undistort(self.image, camera_matrix, distortion_coeff, None, newmatrix)

                x,y,w,h = roi 
                dst = dst[y:y+h, x:x+w]

                msg = CompressedImage()
                msg.header.seq = self.seq
                msg.header.stamp = rospy.Time.now()
                msg.format = 'jpeg'
                ret, buffer = cv2.imencode('.jpg', dst)
                if not ret:
                    print('failed to encode image!')
                else:
                    msg.data = np.array(buffer).tostring()
                    print(f'publishing an image to custom topic with header {str(msg.header)}')
                    self.pub.publish(msg)
                    self.seq += 1
            rate.sleep()


if __name__ == '__main__':
    node = MySubscriberNode('my_subscriber_node')
    node.run()
    rospy.spin()
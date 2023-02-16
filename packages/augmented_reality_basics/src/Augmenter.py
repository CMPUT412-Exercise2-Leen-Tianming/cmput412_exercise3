
import load_calibration
import cv2
import numpy as np

class Augmenter:
    def __init__(self,image):
        self.image = image
    def process_image(self):
        camera_intrinsic_dict =  load_calibration.readYamlFile("./packages/augmented_reality_basics/src/camera_intrinsic.yaml")

        camera_matrix = np.array(camera_intrinsic_dict["camera_matrix"]["data"]).reshape(3,3)
        distortion_coeff = np.array(camera_intrinsic_dict["distortion_coefficients"]["data"]).reshape(5,1)

        width = self.image.shape[1]
        height = self.image.shape[0]

        newmatrix, roi = cv2.getOptimalNewCameraMatrix(camera_matrix,distortion_coeff,(width,height),1, (width,height))
        # new_image= cv2.undistort(img,camera_intrinsic_matrix,distortion_coeff,newmatrix)


        dst = cv2.undistort(self.image, camera_matrix, distortion_coeff, None, newmatrix)

        x,y,w,h = roi 
        dst = dst[y:y+h, x:x+w]    
        return dst
    def ground2pixel(self):
        X_dict =  load_calibration.readYamlFile("./packages/augmented_reality_basics/src/map_file.yaml")
        X = np.array(X_dict["points"]).reshape(3,3)

        camera_intrinsic_dict =  load_calibration.readYamlFile("./packages/augmented_reality_basics/src/camera_intrinsic.yaml")

        camera_matrix = np.array(camera_intrinsic_dict["camera_matrix"]["data"]).reshape(3,3)

    def render_segments(self):
        pass 

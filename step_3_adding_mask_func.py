"""
@author: Yinglu Liu, Jun Wang
@date: 20201012
@contact: jun21wangustc@gmail.com
"""
import os
from main_masker import FaceMasker

def add_mask(image, image_path, mask_image_file, first_dir):
    # print("--------------------------------------ADD MASK-----------------------------")
    is_aug = False
    face_lms_file = '/media/ubuntu/DATA/vinh/face-datasets/ms1m-retinaface-t1/images/' + first_dir + "/" + image_path.split(".")[0].split("/")[-1] + "_landmark" + ".txt"
    template_name = mask_image_file
    #
    image_path_main = image_path.split(".")[0]
    image_path_ext = image_path.split(".")[1]
    masked_face_path = image_path_main + "_mask." + image_path_ext 
    #
    try:
        if os.path.exists(face_lms_file):
            face_lms_str = open(face_lms_file).readline().strip().split(' ')
            face_lms = [float(num) for num in face_lms_str]
            face_masker = FaceMasker(is_aug)
            face_masker.add_mask_one(image_path, face_lms, template_name, masked_face_path, image)
        else:
            pass
    except:
        pass

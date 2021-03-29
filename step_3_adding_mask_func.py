"""
@author: Yinglu Liu, Jun Wang
@date: 20201012
@contact: jun21wangustc@gmail.com
"""

from main_masker import FaceMasker

def add_mask(image, image_path, mask_image_file, first_dir, align_val):
    # print("--------------------------------------ADD MASK-----------------------------")
    is_aug = False
    # face_lms_file = 'data/images/' + first_dir + "/" + image_path.split(".")[0].split("/")[-1] + "_landmark" + ".txt"
    template_name = mask_image_file
    #
    image_path_main = image_path.split(".")[0]
    image_path_ext = image_path.split(".")[1]
    masked_face_path = image_path_main + "_mask." + image_path_ext 
    #
    # face_lms_str = open(face_lms_file).readline().strip().split(' ')
    face_lms_str = align_val.split(' ')
    print("----------------face_lms_str: ", face_lms_str)
    face_lms = [float(num) for num in face_lms_str]
    face_masker = FaceMasker(is_aug)
    face_masker.add_mask_one(image_path, face_lms, template_name, masked_face_path, image)

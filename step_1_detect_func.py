# import os

# dirs = []

# for dir in os.listdir():
#     if(os.path.isdir(dir)):
#         dirs.append(dir)

# print(dirs)

import sys
sys.path.append('.')
import logging.config
logging.config.fileConfig("face_sdk/config/logging.conf")
logger = logging.getLogger('api')

import yaml
import cv2
import numpy as np
from face_sdk.core.model_loader.face_detection.FaceDetModelLoader import FaceDetModelLoader
from face_sdk.core.model_handler.face_detection.FaceDetModelHandler import FaceDetModelHandler

with open('face_sdk/config/model_conf.yaml') as f:
    model_conf = yaml.load(f)

def detect(image, image_path, first_dir):
    # common setting for all model, need not modify.
    # print("--------------------------------------DETECT-----------------------------")
    model_path = 'face_sdk/models'

    # model setting, modified along with model
    scene = 'non-mask'
    model_category = 'face_detection'
    model_name =  model_conf[scene][model_category]

    logger.info('Start to load the face detection model...')
    # load model
    try:
        faceDetModelLoader = FaceDetModelLoader(model_path, model_category, model_name)
    except Exception as e:
        logger.error('Failed to parse model configuration file!')
        logger.error(e)
        sys.exit(-1)
    else:
        logger.info('Successfully parsed the model configuration file model_meta.json!')

    try:
        model, cfg = faceDetModelLoader.load_model()
    except Exception as e:
        logger.error('Model loading failed!')
        logger.error(e)
        sys.exit(-1)
    else:
        logger.info('Successfully loaded the face detection model!')

    faceDetModelHandler = FaceDetModelHandler(model, 'cpu', cfg)

    try:
        dets = faceDetModelHandler.inference_on_image(image)
    except Exception as e:
       logger.error('Face detection failed!')
       logger.error(e)
       sys.exit(-1)
    else:
       logger.info('Successful face detection!')

    # gen result
    image_path_main = image_path.split(".")[0]
    image_path_ext = image_path.split(".")[1]
    # save_path_img = image_path_main + "_detect." + image_path_ext

    save_path_txt = '/media/ubuntu/DATA/vinh/face-datasets/ms1m-retinaface-t1/images/' + first_dir + "/" + image_path.split(".")[0].split("/")[-1] + "_box" + ".txt"



    bboxs = dets
    # with open(save_path_txt, "w") as fd:
    #     for box in bboxs:
    #         line = str(int(box[0])) + " " + str(int(box[1])) + " " + \
    #                str(int(box[2])) + " " + str(int(box[3])) + " " + \
    #                str(box[4]) + " \n"
    #         fd.write(line)
    detect_val = []
    for box in bboxs:
            detect_val.append(str(int(box[0])) + " " + str(int(box[1])) + " " + \
                   str(int(box[2])) + " " + str(int(box[3])) + " " + \
                   str(box[4]))

    # for box in bboxs:
    #     box = list(map(int, box))
    #     cv2.rectangle(image, (box[0], box[1]), (box[2], box[3]), (0, 0, 255), 2)
    # cv2.imwrite(save_path_img, image)
    logger.info('Successfully generate face detection results!')
    return detect_val

"""
@author: JiXuan Xu, Jun Wang
@date: 20201023
@contact: jun21wangustc@gmail.com 
"""
import sys
import os
sys.path.append('.')
import logging.config
logging.config.fileConfig("face_sdk/config/logging.conf")
logger = logging.getLogger('api')

import yaml
import cv2
import numpy as np
from face_sdk.core.model_loader.face_alignment.FaceAlignModelLoader import FaceAlignModelLoader
from face_sdk.core.model_handler.face_alignment.FaceAlignModelHandler import FaceAlignModelHandler

with open('face_sdk/config/model_conf.yaml') as f:
    model_conf = yaml.load(f)

def align(image, image_path, first_dir, detect_val):
    # common setting for all model, need not modify.
    # print("--------------------------------------ALIGN-----------------------------")

    model_path = 'models'

    # model setting, modified along with model
    scene = 'non-mask'
    model_category = 'face_alignment'
    model_name =  model_conf[scene][model_category]

    logger.info('Start to load the face landmark model...')
    # load model
    try:
        faceAlignModelLoader = FaceAlignModelLoader(model_path, model_category, model_name)
    except Exception as e:
        logger.error('Failed to parse model configuration file!')
        logger.error(e)
        sys.exit(-1)
    else:
        logger.info('Successfully parsed the model configuration file model_meta.json!')

    try:
        model, cfg = faceAlignModelLoader.load_model()
    except Exception as e:
        logger.error('Model loading failed!')
        logger.error(e)
        sys.exit(-1)
    else:
        logger.info('Successfully loaded the face landmark model!')

    faceAlignModelHandler = FaceAlignModelHandler(model, 'cpu', cfg)

    # image_det_txt_path = '/media/ubuntu/DATA/vinh/face-datasets/ms1m-retinaface-t1/images/' + first_dir + "/" + image_path.split(".")[0].split("/")[-1] + "_box" + ".txt"
    # try:
    #     if os.path.exists(image_det_txt_path):
    #         with open(image_det_txt_path, 'r') as f:
    #             lines = f.readlines()
    #     else:
    #         pass
    # except:
    #     pass

    try:
        max_size = 0
        # for i, line in enumerate(lines):
        for i, line in enumerate(detect_val):
            line = line.strip().split()
            det = np.asarray(list(map(int, line[0:4])), dtype=np.int32)
            #Cal width height
            xy = np.array([det[0], det[1]])
            zz = np.array([det[2], det[3]])
            wh = zz - xy + 1
            box_area = wh[0] * wh[1]
            if box_area > max_size:
                max_size = box_area
                #Cal width height end
                landmarks = faceAlignModelHandler.inference_on_image(image, det)
                #
                image_path_main = image_path.split(".")[0]
                image_path_ext = image_path.split(".")[1]
                # save_path_img = image_path_main + "_landmark." + image_path_ext 
                #
                # save_path_txt = image_det_txt_path.replace("detect_res", "landmark_res")
                # save_path_txt = image_det_txt_path.replace("_box", "_landmark")
                # save_path_txt = 'data/images/' + first_dir + "/" + image_path.split(".")[0].split("/")[-1] + "_landmark" + ".txt"


                image_show = image.copy()
                # with open(save_path_txt, "w") as fd:
                #     for (x, y) in landmarks.astype(np.int32):
                #         cv2.circle(image_show, (x, y), 2, (255, 0, 0),-1)
                #         line = str(x) + ' ' + str(y) + ' '
                #         fd.write(line)
                align_val = ''
                for (x, y) in landmarks.astype(np.int32):
                        # cv2.circle(image_show, (x, y), 2, (255, 0, 0),-1)
                        align_val = align_val + str(x) + ' ' + str(y) + ' '
                        
                        # fd.write(line)
                align_val = align_val.strip()
            else:
                continue
            # cv2.imwrite(save_path_img, image_show)
    except Exception as e:
        logger.error('Face landmark failed!')
        logger.error(e)
        pass
    else:
        logger.info('Successful face landmark!')
        return align_val

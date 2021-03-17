"""
@author: JiXuan Xu, Jun Wang
@date: 20201023
@contact: jun21wangustc@gmail.com 
"""
import sys
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

def align(image, image_path, first_dir):
    # common setting for all model, need not modify.
    print("--------------------------------------ALIGN-----------------------------")

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

    # read image
    # image_path = 'data/images/images_test/TD_RGB_E_11.jpg'
    # image_det_txt_path = 'data/meta_data/detect_res/' + image_path.split(".")[0].split("/")[-1] + "_" + first_dir + ".txt"
    image_det_txt_path = 'data/images/' + first_dir + "/" + image_path.split(".")[0].split("/")[-1] + "_box" + ".txt"

    # image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    # # resize   
    # height, width, channels = image.shape
    # print("------------------: ", width, height)
    # if width > 1000 or height > 1000:
    #     image = cv2.resize(image, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
    # # resize

    with open(image_det_txt_path, 'r') as f:
        lines = f.readlines()
    try:
        for i, line in enumerate(lines):
            line = line.strip().split()
            det = np.asarray(list(map(int, line[0:4])), dtype=np.int32)
            landmarks = faceAlignModelHandler.inference_on_image(image, det)
            #
            image_path_main = image_path.split(".")[0]
            image_path_ext = image_path.split(".")[1]
            save_path_img = image_path_main + "_landmark." + image_path_ext 
            #
            # save_path_txt = image_det_txt_path.replace("detect_res", "landmark_res")
            save_path_txt = image_det_txt_path.replace("_box", "_landmark")


            image_show = image.copy()
            with open(save_path_txt, "w") as fd:
                for (x, y) in landmarks.astype(np.int32):
                    cv2.circle(image_show, (x, y), 2, (255, 0, 0),-1)
                    line = str(x) + ' ' + str(y) + ' '
                    fd.write(line)

            # cv2.imwrite(save_path_img, image_show)
    except Exception as e:
        logger.error('Face landmark failed!')
        logger.error(e)
        sys.exit(-1)
    else:
        logger.info('Successful face landmark!')
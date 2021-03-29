import os
from step_1_detect_func import detect
from step_2_alignment_func import align
from step_3_adding_mask_func import add_mask
import cv2
import random
from skimage.io import imread, imsave
import asyncio
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp
import math
import zipfile
import shutil
import filetype

async def main(loop):
    # print('entering main')
    num_processes = mp.cpu_count()
    executor = ProcessPoolExecutor(max_workers=num_processes)

    file_name_array = []

    image_test_folder = "data/images/"  

    number_folder = len(os.listdir(image_test_folder))
    w = math.ceil(number_folder / num_processes)
    h = num_processes

    folder_name_in_partition = [['' for x in range(w)] for y in range(h)] 
    index_w = 0
    index_h = 0

    for folder in  os.listdir(image_test_folder): 
        if os.path.isdir(image_test_folder + folder) == True: 
            folder_name_in_partition[index_h][index_w] = folder
            if index_h == h - 1:
                index_h = -1
                index_w = index_w + 1
            index_h = index_h + 1
    data = await asyncio.gather(*(loop.run_in_executor(executor, f, folders) for folders in folder_name_in_partition))

    # print('got result', data)
    # print('leaving main')

####################

def f(folders):
    image_test_folder = "data/images/"  
    index_to_zip = 0
    folder_arr = []

    try:
        for index, i in enumerate(folders, 0):
            if os.path.isdir(image_test_folder + i) == True and i != '': 
                folder_arr.append(image_test_folder + i)
                for file in  os.listdir(image_test_folder + i):
                    image_path = image_test_folder + i + "/" + file
                    if os.path.isfile(image_path) == True: 
                        if file != '':
                            image, is_image = read_and_resize(image_path)
                            if is_image == True:
                                detect_val = detect(image, image_path, i) 
                                
                                align_val = align(image, image_path, i, detect_val) 

                                image_2, is_image_2 = read_and_resize_add_mask(image_path)
                                list_mask_image_name = ["0.png", "1.png", "2.png", "3.png", "4.png", "5.png", "6.png", "7.png"]
                                add_mask(image_2, image_path, random.choice(list_mask_image_name), i, align_val)
                
                if index_to_zip == 1 or (index + 1 <= len(folders) - 1 and folders[index + 1] == '') or len(folders) - 1 == index:
                    zipit(folder_arr, "data/archive/" + i + ".zip")
                    folder_arr = []
                    # remove_folder(folder_arr)
                    index_to_zip = -1
                index_to_zip = index_to_zip + 1
    except Exception as e:
        print("-------------e-----------: ", e)

def read_and_resize(file):
    # read image
    if filetype.is_image(file):
        image = cv2.imread(file, cv2.IMREAD_COLOR)
        # resize
        height, width, channels = image.shape
        if width > 1024 or height > 1024:
            image = cv2.resize(image, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
        return image, True
    else:
        return None, False

def read_and_resize_add_mask(file):
    # read image
    if filetype.is_image(file):
        image = imread(file)
        # resize
        height, width, channels = image.shape
        if width > 1024 or height > 1024:
            image = cv2.resize(image, None, fx=0.2, fy=0.2, interpolation=cv2.INTER_CUBIC)
        return image, True
    else:
        return None, False


# main()

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file),
                       os.path.relpath(os.path.join(root, file),
                                       os.path.join(path, '..')))


def zipit(dir_list, zip_name):
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for dir in dir_list:
        zipdir(dir, zipf)
    zipf.close()

def remove_folder(dir_list):
    for i in dir_list:
        shutil.rmtree(i)


loop = asyncio.get_event_loop()
loop.run_until_complete(main(loop))
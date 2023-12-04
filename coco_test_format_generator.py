import os
import json
import cv2
import multiprocessing
import numpy as np

rootDircetory = '/PATH/TO/ROOT/'
testPath = 'ImagePath'
categories = ['cat1', 'cat2', 'cat3', 'cat4', 'cat5']


class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NpEncoder, self).default(obj)
    

def process_wrapper(args):
    return multi_process(*args)

def multi_process(image_path, idx):
    img = cv2.imread(image_path)    # you can use other pacakages to get image's width and height
    directory, fn = os.path.split(image_path)
    directory = directory.replace(os.path.join(rootDircetory, testPath), '')[1:]
    coco_dict = {'file_name': os.path.join(directory, fn),
                 'height': img.shape[0],
                 'width': img.shape[1],
                 'id': idx}
    
    return coco_dict


def is_image(fn):
    return True if os.path.splitext(os.path.split(fn)[-1])[1].lower() in ['.png', '.jpg'] else False    


def main():
    testDirectory = os.path.join(rootDircetory, testPath)
    image_list = [os.path.join(dir_path, f) for (dir_path, dir_names, fn) in os.walk(testDirectory) for f in fn]
    image_list = sorted(filter(is_image, image_list))
    indices_list = np.arange(len(image_list))
    
    with multiprocessing.Pool(multiprocessing.cpu_count()) as pool:
        out = pool.map(process_wrapper, zip(image_list, indices_list))
    out_dict = {}
    out_dict['images'] = out
    cate_list = []
    for idx, item in enumerate(categories):
        cate_list.append({'supercategory': 'Defect',
                          'id': idx + 1,
                          'name': item})
        
    out_dict['categories'] = cate_list
    out_dict['annotations'] = []

    with open('coco_test.json', 'wb') as f_w:
        f_w.write(json.dumps(out_dict, cls=NpEncoder, ensure_ascii=False, indent=4).encode('UTF-8'))    # safe encoding


if __name__ == "__main__":
    main()

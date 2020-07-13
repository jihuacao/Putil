# coding=utf-8
#In[]:
import numpy as np
import cv2
import Putil.data.aug as pAug
from Putil.data.common_data import CommonDataWithAug

from Putil.data.vision_data_aug.detection.rectangle import HorizontalFlip as BH
from Putil.data.vision_data_aug.image_aug import HorizontalFlip as IH
from Putil.data.aug import AugFunc

class Data(CommonDataWithAug):

    def _restart_process(self, restart_param):
        '''
        process while restart the data, process in the derived class and called by restart_data
        restart_param: the argv which the derived class need, dict
        '''
        pass

    def _inject_operation(self, inject_param):
        '''
        operation while the epoch_done is False, process in the derived class and called by inject_operation
        injecct_param: the argv which the derived class need, dict
        '''
        pass

    def __init__(self):
        CommonDataWithAug.__init__(self)
        self._index = [0]
    
    def _generate_from_origin_index(self, index):
        image = cv2.imread('../test_image.jpg')
        assert image is not None
        bboxes = [
            [5, 5, image.shape[1] // 2, image.shape[0] // 2], 
            [image.shape[1] // 3, image.shape[0] // 3, (image.shape[1] - image.shape[1] // 3) // 3, (image.shape[0] - image.shape[0] // 3) // 3], 
            [image.shape[1] // 4, image.shape[0] // 4, (image.shape[1] - image.shape[1] // 4) // 4, (image.shape[0] - image.shape[0] // 4) // 4] 
            ] # LTWHCR
        return image, bboxes


class CombineAugFunc(AugFunc):
    def __init__(self):
        self._image_aug = IH()
        self._bboxes_aug = BH()
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image = self._image_aug(image)
        bboxes = self._bboxes_aug(image, bboxes)
        return image, bboxes

root_node = pAug.AugNode(pAug.AugFuncNoOp())
root_node.add_child(pAug.AugNode(pAug.AugFuncNoOp()))
root_node.add_child(pAug.AugNode(CombineAugFunc()))
root_node.freeze_node()

data = Data()
data.set_aug_node_root(root_node)

import matplotlib.pyplot as plt

print(len(data))

for index in range(0, len(data)):
    image, bboxes = data[index]
    print(bboxes)
    for bbox in bboxes:
        cv2.rectangle(
            image, 
            (bbox[0], bbox[1]), 
            (bbox[0] + bbox[2], bbox[1] + bbox[3]), 
            (0, 255, 0),
            thickness=5)
        pass
    plt.imshow(image)
    plt.show()
    pass
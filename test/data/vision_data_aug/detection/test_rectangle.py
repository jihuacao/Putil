# coding=utf-8
import os
image_path = os.path.join(os.path.split(os.path.split(os.path.abspath(__file__))[0])[0], 'test_image.jpg')
#In[]:
import numpy as np
import os
import random
import cv2
import Putil.data.aug as pAug
from Putil.data.common_data import CommonDataWithAug

from Putil.data.vision_data_aug.detection.rectangle import HorizontalFlip as BH
from Putil.data.vision_data_aug.image_aug import HorizontalFlip as IH
from Putil.data.vision_data_aug.detection.rectangle import HorizontalFlipCombine as HFC
from Putil.data.vision_data_aug.detection.rectangle import RandomResampleCombine as RRC
from Putil.data.vision_data_aug.detection.rectangle import RandomTranslateConbine as RTC
from Putil.data.vision_data_aug.detection.rectangle import RandomRotateCombine as RRB
from Putil.data.vision_data_aug.detection.rectangle import RandomShearCombine as RSC
from Putil.data.vision_data_aug.detection.rectangle import VerticalFlipCombine as VFC 
from Putil.data.vision_data_aug.detection.rectangle import RandomHSVCombine as RHC
from Putil.data.vision_data_aug.detection.rectangle import SizeFloatCombine as SFC
from Putil.data.aug import AugFunc

image_wh = (800, 800)

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
        self._data_field = [0]
    
    def _generate_from_origin_index(self, index):
        image = np.zeros(shape=[image_wh[1], image_wh[0], 3], dtype=np.uint8)
        assert image is not None
        begin = 20
        bboxes = [
            [begin, begin, image.shape[1] // 2 - begin, image.shape[0] // 2 - begin], 
            [begin, begin + image.shape[0] // 2, image.shape[1] // 2 - 2 * begin, image.shape[0] // 2 - 2 * begin],
            [begin + image.shape[1] // 2, begin, image.shape[1] // 2 - 2 * begin, image.shape[0] // 2 - 2 * begin],
            [begin + image.shape[1] // 2, begin + image.shape[0] // 2, image.shape[1] // 2 - 2 * begin, image.shape[0] // 2 - 2 * begin]
            ] # LTWHCR
        color = {0: (125, 0, 0), 1: (0, 125, 0), 2: (0, 0, 125), 3: (125, 125, 0)}
        for index, bbox in enumerate(bboxes):
            image[bbox[1]: bbox[1] + bbox[3], bbox[0]: bbox[0] + bbox[2], :] = color[index]
        bboxes = np.array(bboxes, dtype=np.float64).tolist()
        image = (image / 255).astype(np.float32)
        return image, bboxes


class CombineAugFuncHF(AugFunc):
    def __init__(self):
        AugFunc.__init__(self)
        self._aug = HFC()
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(image, bboxes)
        return image, bboxes
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncVF(AugFunc):
    def __init__(self):
        AugFunc.__init__(self)
        self._aug = VFC()
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(image, bboxes)
        return image, bboxes
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncRRC(AugFunc):
    def __init__(self):
        AugFunc.__init__(self)
        self._aug = RRC(scale=1)
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(image, bboxes)
        return image, bboxes
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncRTC(AugFunc):
    def __init__(self):
        AugFunc.__init__(self)
        self._aug = RTC(translate=0.5)
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(image, bboxes)
        return image, bboxes
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncRRB(AugFunc):
    def __init__(self):
        AugFunc.__init__(self)
        self._aug = RRB(50)
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(image, bboxes)
        return image, bboxes
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncRSC(AugFunc):
    def __init__(self):
        AugFunc.__init__(self)
        self._aug = RSC(0.9)
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(image, bboxes)
        return image, bboxes
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncRHC(pAug.AugFunc):
    def __init__(self):
        self._aug = RHC(0.0, 50.0, 50.0)
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(image, bboxes)
        return image, bboxes
    
    @property
    def name(self):
        return self._aug.name


class CombineAugFuncSFC(pAug.AugFunc):
    def __init__(self):
        self._aug = SFC((0.5, 1.0), (0.5, 1.0))
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(image, bboxes)
        return image, bboxes

root_node = pAug.AugNode(pAug.AugFuncNoOp())
root_node.add_child(pAug.AugNode(pAug.AugFuncNoOp()))
HFNode = root_node.add_child(pAug.AugNode(CombineAugFuncHF()))
#HFNode.add_child(pAug.AugNode(CombineAugFuncRRC()))
#HFNode.add_child(pAug.AugNode(pAug.AugFuncNoOp()))
VFNode = root_node.add_child(pAug.AugNode(CombineAugFuncVF()))
RRCNode = root_node.add_child(pAug.AugNode(CombineAugFuncRRC()))
#RRCNode.add_child(pAug.AugNode(CombineAugFuncHF()))
#RRCNode.add_child(pAug.AugNode(pAug.AugFuncNoOp()))
RTCNode = root_node.add_child(pAug.AugNode(CombineAugFuncRTC()))
RRBNode = root_node.add_child(pAug.AugNode(CombineAugFuncRRB()))
RSCNode = root_node.add_child(pAug.AugNode(CombineAugFuncRSC()))
RHCNode = root_node.add_child(pAug.AugNode(CombineAugFuncRHC()))
SFCNode = root_node.add_child(pAug.AugNode(CombineAugFuncSFC()))
root_node.freeze_node()

for index in range(0, len(root_node)):
    node = root_node[index]
    print('name: {0}'.format(node.func.name))
    pass

data = Data()
data.set_aug_node_root(root_node)

import matplotlib.pyplot as plt
import matplotlib.patches as patches

print(len(data))

rect_color = ['m', 'c', 'y', 'w']
for index in range(0, len(data)):
    image, bboxes = data[index]
    #print(bboxes)
    #print(image.shape)
    print(np.max(image))
    assert image.shape == (image_wh[0], image_wh[1], 3), 'image shape: {0}'.format(image.shape)
    plt.imshow(image[:, :, ::-1])
    currentAxis=plt.gca()
    for i, bbox in enumerate(bboxes):
        #cv2.rectangle(image, (bbox[0], bbox[1]), (bbox[0] + bbox[2], bbox[1] + bbox[3]), (0, 255, 0), thickness=5)
        rect = patches.Rectangle(bbox[0: 2], bbox[2], bbox[3], linewidth=2, edgecolor=rect_color[i], facecolor='none')
        currentAxis.add_patch(rect)
        pass
    plt.show()
    pass
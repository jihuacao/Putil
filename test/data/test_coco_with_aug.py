# coding=utf-8
#import Putil.data.common_data as pcd
#import Putil.data.coco as coco
#
#manager_common_data = pcd.CommonDataManager()
#manager_common_data.start()
#coco_data = manager_common_data.COCOData('/data2/Public_Data/COCO', coco.COCOData.Stage.STAGE_TRAIN, './result', detection=True)
#print(len(coco_data))
import numpy as np
import Putil.base.logger as plog

plog.PutilLogConfig.config_handler(plog.stream_method)
plog.PutilLogConfig.config_format(plog.FormatRecommend)
plog.PutilLogConfig.config_log_level(stream=plog.DEBUG)
root_logger = plog.PutilLogConfig('test_coco').logger()
root_logger.setLevel(plog.DEBUG)
TestCocoLogger = root_logger.getChild('TestCoco')
TestCocoLogger.setLevel(plog.DEBUG)

import Putil.data.coco as COCO
import Putil.data.aug as pAug
from Putil.data.vision_data_aug.detection.rectangle import HorizontalFlip as BH
from Putil.data.vision_data_aug.image_aug import HorizontalFlip as IH
from Putil.data.vision_data_aug.detection.rectangle import HorizontalFlipCombine as HFC
from Putil.data.vision_data_aug.detection.rectangle import RandomResampleCombine as RRC
from Putil.data.vision_data_aug.detection.rectangle import RandomTranslateConbine as RTC
from Putil.data.vision_data_aug.detection.rectangle import RandomRotateCombine as RRB
from Putil.data.vision_data_aug.detection.rectangle import RandomShearCombine as RSC
from Putil.data.vision_data_aug.detection.rectangle import VerticalFlipCombine as VFC 
from Putil.data.vision_data_aug.detection.rectangle import RandomHSVCombine as RHC
from Putil.data.aug import AugFunc
import Putil.data.aug as pAug
from Putil.data.coco import COCOData
from Putil.data.io_convertor import IOConvertorNoOp


class COCOCommonAugFuncBase(AugFunc):
    def __init__(self):
        AugFunc.__init__(self)
        pass

    def bboxes(*args):
        return args[COCOData.detection_box_index]
    
    def image(*args):
        return args[COCOData.image_index]

    def get_image_and_bboxes(self, *args):
        return args[COCOData.image_index], args[COCOData.detection_box_index]
    
    def repack(self, *args, image, bboxes):
        temp_args = list(args)
        classes = temp_args[COCOData.detection_class_index]
        classes = np.delete(classes, np.argwhere(np.isnan(bboxes)), axis=0)
        bboxes = np.delete(bboxes, np.argwhere(np.isnan(bboxes)), axis=0)
        temp_args[COCOData.detection_box_index] = bboxes
        temp_args[COCOData.detection_class_index] = classes
        temp_args[COCOData.image_index] = image
        return tuple(temp_args)

        return self._repack(*args, image=image, bboxes=bboxes, classes=None)


class CombineAugFuncHF(COCOCommonAugFuncBase):
    def __init__(self):
        
        self._aug = HFC()
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(*self.get_image_and_bboxes(*args))
        return self.repack(*args, image=image, bboxes=bboxes)
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncVF(COCOCommonAugFuncBase):
    def __init__(self):
        
        self._aug = VFC()
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]
        image, bboxes = self._aug(*self.get_image_and_bboxes(*args))
        return self.repack(*args, image=image, bboxes=bboxes)
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncRRC(COCOCommonAugFuncBase):
    def __init__(self):
        
        self._aug = RRC(scale=1)
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(*self.get_image_and_bboxes(*args))
        return self.repack(*args, image=image, bboxes=bboxes)
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncRTC(COCOCommonAugFuncBase):
    def __init__(self):
        
        self._aug = RTC(translate=0.5)
        pass

    def __call__(self, *args):
        image, bboxes = self._aug(*self.get_image_and_bboxes(*args))
        ret = self.repack(*args, image=image, bboxes=bboxes)
        while len(self.bboxes(*ret)) == 0:
            image, bboxes = self._aug(*self.get_image_and_bboxes(*args))
            ret = self.repack(*args, image=image, bboxes=bboxes)
        return ret
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncRRB(COCOCommonAugFuncBase):
    def __init__(self):
        
        self._aug = RRB(50)
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(*self.get_image_and_bboxes(*args))
        return self.repack(*args, image=image, bboxes=bboxes)
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncRSC(COCOCommonAugFuncBase):
    def __init__(self):
        
        self._aug = RSC(0.2)
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]
        image, bboxes = self._aug(*self.get_image_and_bboxes(*args))
        return self.repack(*args, image=image, bboxes=bboxes)
    
    @property
    def name(self):
        return self._aug.name
    pass


class CombineAugFuncRHC(COCOCommonAugFuncBase):
    def __init__(self):
        
        self._aug = RHC(0.0, 50.0, 50.0)
        pass

    def __call__(self, *args):
        image = args[0]
        bboxes = args[1]

        image, bboxes = self._aug(*self.get_image_and_bboxes(*args))
        return self.repack(*args, image=image, bboxes=bboxes)
    
    @property
    def name(self):
        return self._aug.name
    pass

seed = 64

COCO.COCOData.set_seed(seed)
dataset_train = COCO.COCOData('/data2/Public_Data/COCO/unzip_data/2017', COCO.COCOData.Stage.Evaluate, './test/data/result/test_coco_with_aug', detection=True)
root_node = pAug.AugNode(pAug.AugFuncNoOp())
Original = root_node.add_child(pAug.AugNode(pAug.AugFuncNoOp()))
root_node.add_child(pAug.AugNode(CombineAugFuncHF()))
root_node.add_child(pAug.AugNode(CombineAugFuncRHC()))
root_node.add_child(pAug.AugNode(CombineAugFuncRRB()))
root_node.add_child(pAug.AugNode(CombineAugFuncRSC()))
root_node.add_child(pAug.AugNode(CombineAugFuncRTC()))
root_node.add_child(pAug.AugNode(CombineAugFuncVF()))
root_node.freeze_node()
dataset_train.set_aug_node_root(root_node, [np.random.sample() for _rn in root_node])
class_amount = 80
convertor = IOConvertorNoOp()
dataset_train.set_convert_to_input_method(convertor)
TestCocoLogger.info('data amount: {0}'.format(len(dataset_train)))
for i in range(0, len(dataset_train)):
    image, bboxes, classes, weight = dataset_train[i]
    TestCocoLogger.info('count: {0}'.format(i))
# coding=utf-8
#In[]
import os
from Putil.base import jupyter_state
jupyter_state.go_to_top(6, os.path.abspath(__file__))

import torch
import numpy as np
import random

from Putil.torch.util import set_torch_deterministic as STD

def test_iou(iou):
    seed = 64
    STD(seed)
    np.random.seed(seed)
    random.seed(seed)

    ran = np.linspace(0, 100)
    X, Y = np.meshgrid(ran, ran)

    shape = [10, 4, 100, 100]
    pre = torch.from_numpy(np.reshape(np.random.sample(np.prod(shape)) * 100 - 50, shape))
    gt = torch.from_numpy(np.reshape(np.random.sample(np.prod(shape)) * 50 - 25, shape)) 
    _iou = iou(pre, gt)
    print('min: {}'.format(_iou[iou.iou_index()].min()))
    print('max: {}'.format(_iou[iou.iou_index()].max()))
    print('nan: {}'.format(torch.isnan(_iou[iou.iou_index()]).sum()))
    print('inf: {}'.format(torch.isinf(_iou[iou.iou_index()]).sum()))
    return _iou

if __name__ == '__main__':
    from Putil.torch.indicator.vision.object_detection.iou import IoU as IoU
    iou = IoU()
    iou_data = test_iou(iou)
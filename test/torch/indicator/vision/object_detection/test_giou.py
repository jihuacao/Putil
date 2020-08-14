# coding=utf-8

import torch
import numpy as np
import random

from Putil.torch.util import set_torch_deterministic as STD
from Putil.torch.indicator.vision.object_detection.giou import compute_iou_giou as GIOU

seed = 64
STD(seed)
np.random.seed(seed)
random.seed(seed)


def main():
    shape = [10, 100, 100, 4]
    pre = torch.from_numpy(np.reshape(np.random.sample(np.prod(shape)) * 100, shape))
    gt = torch.from_numpy(np.reshape(np.random.sample(np.prod(shape)) * 100, shape)) 
    print(GIOU(pre, gt))


if __name__ == '__main__':
    main()
# coding=utf-8
import numpy as np
import cv2
import torch

#class GradCAM(object):
#    """
#    1: 网络不更新梯度,输入需要梯度更新
#    2: 使用目标类别的得分做反向传播
#    """
#
#    def __init__(self, net, layer_name):
#        self.net = net
#        self.layer_name = layer_name
#        self.feature = None
#        self.gradient = None
#        self.net.eval()
#        self.handlers = []
#        self._register_hook()
#
#    def _get_features_hook(self, module, input, output):
#        self.feature = output
#        print("feature shape:{}".format(output.size()))
#
#    def _get_grads_hook(self, module, input_grad, output_grad):
#        """
#        :param input_grad: tuple, input_grad[0]: None
#                                   input_grad[1]: weight
#                                   input_grad[2]: bias
#        :param output_grad:tuple,长度为1
#        :return:
#        """
#        self.gradient = output_grad[0]
#
#    def _register_hook(self):
#        for (name, module) in self.net.named_modules():
#            if name == self.layer_name:
#                self.handlers.append(module.register_forward_hook(self._get_features_hook))
#                self.handlers.append(module.register_backward_hook(self._get_grads_hook))
#
#    def remove_handlers(self):
#        for handle in self.handlers:
#            handle.remove()
#
#    def __call__(self, inputs, index):
#        """
#        :param inputs: [1,3,H,W]
#        :param index: class id
#        :return:
#        """
#        self.net.zero_grad()
#        output = self.net(inputs)  # [1,num_classes]
#        if index is None:
#            index = np.argmax(output.cpu().data.numpy())
#        target = output[0][index]
#        target.backward()
#
#        gradient = self.gradient[0].cpu().data.numpy()  # [C,H,W]
#        weight = np.mean(gradient, axis=(1, 2))  # [C]
#
#        feature = self.feature[0].cpu().data.numpy()  # [C,H,W]
#
#        cam = feature * weight[:, np.newaxis, np.newaxis]  # [C,H,W]
#        cam = np.sum(cam, axis=0)  # [H,W]
#        cam = np.maximum(cam, 0)  # ReLU
#
#        # 数值归一化
#        cam -= np.min(cam)
#        cam /= np.max(cam)
#        # resize to 224*224
#        cam = cv2.resize(cam, (224, 224))
#        return cam

class GradCam:
    def __init__(self, y, x):
        self._input = x
        self._output = y

        self._hook = lambda input_y, input_x: None
        pass

    def register_cam_pre_hook(self, hook):
        pass

    def cam(self):
        self._hook(self._output, self._input)
        return 1.0 / self._output.grad.detach().cpu().numpy() * self._input.grad.detach().cpu().numpy() * self._input.detach().cpu.numpy()
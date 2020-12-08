# coding=utf-8
'''
 @note 使用backbone 与 backend进行model的构建，model包含了一个模型所有需要存储的参数
'''
from torch.nn import Module


class Model:
    def __init__(self, args, *modules, **kwargs):
        self._model_name = args.model_name
        self._model_source = args.model_source
        pass
    pass


class _DefaultModel(Model):
    def __init__(self, args, *modules, **kwargs):
        Model.__init__(self, args)
        pass

    def forward(self, x):
        for module in modules:
            x = module(x)
            pass
        return x
    pass


def DefaultModel(args):
    def generate_default_model(*modules, **kwargs):
        return DefaultModel(args, *modules, **kwargs)
    return generate_default_model


def DefaultModelArg(parser):
    pass
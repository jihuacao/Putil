# coding=utf-8
import Putil.base.logger as plog

logger = plog.PutilLogConfig('loss_factory').logger()
logger.setLevel(plog.DEBUG)

import Putil.demo.deep_learning.base.loss as standard
from util import loss as project


def loss_factory(args, source, name, property_type='', **kwargs):
    '''
     @brief
     @note
     @param[in]
      args
       loss_name: the main type of the loss
       loss_source: from standard or project
    '''
    if args.framework == 'torch':
        pass
    else:
        raise NotImplementedError('loss of framework: {} is not implemented'.format(args.framework))
    model = '{0}.{1}'.format(source, name)
    return eval('{}(args, property_type, **kwargs)'.format(model))


def loss_arg_factory(parser, source, name, property_type='', **kwargs):
    arg = '{}.{}Arg'.format(source, name)
    logger.info('loss_arg: {}'.format(arg))
    return eval('{}(parser, property_type, **kwargs)'.format(arg)) 
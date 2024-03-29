# coding = utf-8
import tensorflow as tf
import tensorflow.contrib.layers as layers
from colorama import Fore
import numpy as np
import random
import Putil.np.util as npu
import Putil.tf.util as tfu
import base.logger as plog

root_logger = plog.PutilLogConfig('yolo2ModelBase').logger()
root_logger.setLevel(plog.DEBUG)

Yolo2BuildLogger = root_logger.getChild('Yolo2Build')
Yolo2BuildLogger.setLevel(plog.DEBUG)

Yolo2GenerateFeedLogger = root_logger.getChild('Yolo2GenerateFeed')
Yolo2GenerateFeedLogger.setLevel(plog.DEBUG)

StandardYolo2GenerateLogger = root_logger.getChild('StandardYolo2Generate')
StandardYolo2GenerateLogger.setLevel(plog.DEBUG)

Yolo2GenerateLogger = root_logger.getChild('Yolo2Generate')
Yolo2GenerateLogger.setLevel(plog.DEBUG)

Yolo2GenerateILogger = root_logger.getChild('Yolo2GenerateI')
Yolo2GenerateILogger.setLevel(plog.DEBUG)

assert tf.__version__ == '1.6.0', Fore.RED + 'version of tensorflow should be 1.6.0'


class Yolo2Build:
    def __init__(self, net_output, class_num, prior_h, prior_w, scalar, _dtype):
        self._net_output = net_output
        self._class_amount = class_num
        self.__check_prior(prior_h, prior_w)
        self._prior_height = prior_h
        self._prior_width = prior_w
        self._cluster_object_count = len(prior_h)
        self._scalar = scalar
        self._dtype = _dtype

        self._pro__ = self.GeneratePro()
        self._output_tensor = self._pro__['pro']
        self._anchor_pro__ = self._pro__['anchor']
        self._precision_pro__ = self._pro__['precision']
        self._class_pro__ = self._pro__['class']
        self._y_pro__ = self._pro__['y']
        self._x_pro__ = self._pro__['x']
        self._h_pro__ = self._pro__['h']
        self._w_pro__ = self._pro__['w']

        self._output_loss__, self._place_gt_result__, self._iou_result__ = self.AppendLoss()

        self._gt_one_hot_class__ = self._place_gt_result__['class']
        self._gt_feed_class__ = self._place_gt_result__['feed_class']
        self._gt_y_offset__ = self._place_gt_result__['y_offset']
        self._gt_y__ = self._place_gt_result__['y']
        self._gt_y_feed__ = self._place_gt_result__['y_feed']
        self._gt_x_offset__ = self._place_gt_result__['x_offset']
        self._gt_x__ = self._place_gt_result__['x']
        self._gt_x_feed__ = self._place_gt_result__['x_feed']
        self._gt_h__ = self._place_gt_result__['h']
        self._gt_h_feed__ = self._place_gt_result__['h_feed']
        self._gt_w__ = self._place_gt_result__['w']
        self.__gt_w_feed__ = self._place_gt_result__['w_feed']
        self._anchor_mask__ = self._place_gt_result__['anchor_mask']
        self._negative_anchor_mask__ = self._place_gt_result__['negative_anchor_mask']

        self._total_loss__ = self._output_loss__['total_loss']
        self._anchor_loss__ = self._output_loss__['anchor_loss']
        self._precision_loss__ = self._output_loss__['precision_loss']
        self._class_loss__ = self._output_loss__['class_loss']

        self._indicator_mean_iou = self._output_loss__['mean_iou']
        self._indicator_classify_top_one_acc = self._output_loss__['classify_top_one_acc']

        self._gt_iou__ = self._iou_result__
        pass

    @property
    def IndicatorClassifyTopOneAcc(self):
        return self._indicator_classify_top_one_acc

    @property
    def IndicatorIoU(self):
        return self._indicator_mean_iou

    @property
    def NewOutput(self):
        return self._net_output

    @property
    def ClassAmount(self):
        return self._class_amount

    @property
    def PriorHeight(self):
        return self._prior_height

    @property
    def PriorWidth(self):
        return self._prior_width

    @property
    def ClusterObjectAmount(self):
        return self._cluster_object_count

    @property
    def Scalar(self):
        return self._scalar

    @property
    def Dtype(self):
        return self._dtype

    @property
    def Pro(self):
        return self._output_tensor

    @property
    def AnchorPro(self):
        return self._anchor_pro__

    @property
    def PrecisionPro(self):
        return self._precision_pro__

    @property
    def ClassPro(self):
        return self._class_pro__

    @property
    def YPro(self):
        return self._y_pro__

    @property
    def XPro(self):
        return self._x_pro__

    @property
    def HPro(self):
        return self._h_pro__

    @property
    def WPro(self):
        return self._w_pro__

    @property
    def GtOneHotClass(self):
        return self._gt_one_hot_class__

    @property
    def GtClassFeed(self):
        return self._gt_feed_class__

    @property
    def GtYOffset(self):
        return self._gt_y_offset__

    @property
    def GtY(self):
        return self._gt_y__

    @property
    def GtYFeed(self):
        return self._gt_y_feed__

    @property
    def GtXOffset(self):
        return self._gt_x_offset__

    @property
    def GtX(self):
        return self._gt_x__

    @property
    def GtxFeed(self):
        return self._gt_x_feed__

    @property
    def GtH(self):
        return self._gt_h__

    @property
    def GtHFeed(self):
        return self._gt_h_feed__

    @property
    def GtW(self):
        return self._gt_w__

    @property
    def GtWFeed(self):
        return self.__gt_w_feed__

    @property
    def AnchorMask(self):
        return self._anchor_mask__

    @property
    def NegativateAnchorMask(self):
        return self._negative_anchor_mask__

    @property
    def TotalLoss(self):
        return self._total_loss__

    @property
    def AnchorLoss(self):
        return self._anchor_loss__

    @property
    def PrecisionLoss(self):
        return self._precision_loss__

    @property
    def ClassLoss(self):
        return self._class_loss__

    @property
    def GtIou(self):
        return self._gt_iou__

    def __check_prior(self, prior_h, prior_w):
        # check failed throw exception
        return True
        pass

    def GeneratePro(self):
        return gen_pro(self._net_output, self._class_amount, self._cluster_object_count, self._dtype)
        pass

    def AppendLoss(self):
        return append_yolo2_loss(self._pro__, self._class_amount, self._prior_height, self._prior_width, self._scalar,
                                 self._dtype)
        pass

    pass


def append_yolo2_loss(
        yolo2_net_feature,
        class_num,
        prior_h,
        prior_w,
        scalar,
        _dtype=0.32
):
    """

    :param yolo2_net_feature: feature from base net output
    :param class_num: the count of the class with background
    :param prior_h: prior height list or 1-D ndarray
    :param prior_w: prior width list or 1-D ndarray
    :param scalar: down sample scalar
    :param _dtype: model parameter dtype, default 0.32
    :return:
    """
    assert len(prior_w) == len(prior_h), Fore.RED + 'prior height should be same length with prior width'
    print(Fore.YELLOW + '-------generate yolo2 loss---------')
    print(Fore.GREEN + 'class_num : ', class_num)
    print(Fore.GREEN + 'prior_h : ', prior_h)
    print(Fore.GREEN + 'prior_w : ', prior_w)
    print(Fore.GREEN + 'scalar : ', scalar)
    cluster_object_count = len(prior_w)
    place_gt_result = __PlaceGT(cluster_object_count=cluster_object_count, _dtype=_dtype).Place
    place_process_result = __place_process(
        place_gt_result,
        class_num,
        prior_h,
        prior_w,
        scalar=scalar,
        _dtype=_dtype
    )
    pro_result_read_result = __pro_result_reader(
        split_pro_result=yolo2_net_feature)
    calc_iou_result = __calc_iou(
        pro_result_read_result=pro_result_read_result,
        place_process_result=place_process_result,
        scalar=scalar,
        prior_h=prior_h,
        prior_w=prior_w,
        _dtype=_dtype
    )
    loss = __calc_loss(
        split_pro_result=yolo2_net_feature,
        gt_process_result=place_process_result,
        calc_iou_result=calc_iou_result)
    print(Fore.YELLOW + '-------generate yolo2 loss done---------')
    return loss, place_process_result, calc_iou_result


# generator placeholder for total feed, designed to easy used and generate
# gt is the standard data
# 'class' : int include background and all kind of object
# 'p_mask' : set 1.0 in the cell location which has an object and set 0.0 for other
# 'n_mask' : set 1.0 in the cell location which does not contain any object and set 0.0 for other
# 'y': object center location y shift from the top left point int the cell, set 0.0 which cell does not contain object
# 'x': object center location x shift from the top left point int the cell, set 0.0 which cell does not contain object
# relationship between real (center_y, center_x, height, width) and (y_shift, x_shift, h_shift, w_shift):
class __PlaceGT:
    def __init__(self, cluster_object_count, _dtype):
        gt_place = dict()
        dtype = tfu.tf_type(_dtype).Type
        with tf.name_scope('GT'):
            gt_place['class'] = tf.placeholder(dtype=tf.int32, shape=[None, None, None, cluster_object_count],
                                               name='class')
            # set 0.0 in the cell which does not contain any object except background
            gt_place['y'] = tf.placeholder(dtype=dtype, shape=[None, None, None, cluster_object_count],
                                           name='y')
            gt_place['x'] = tf.placeholder(dtype=dtype, shape=[None, None, None, cluster_object_count],
                                           name='x')
            # !!!!important: because of the follow process in (__place_process), hw should not contain negative and zero
            # !!!!suggest fill prior value in the cell location which does not contain any object
            gt_place['h'] = tf.placeholder(dtype=dtype, shape=[None, None, None, cluster_object_count],
                                           name='h')
            gt_place['w'] = tf.placeholder(dtype=dtype, shape=[None, None, None, cluster_object_count],
                                           name='w')
            # the mask frequently used in calc loss
            gt_place['p_mask'] = tf.placeholder(dtype=dtype, shape=[None, None, None, 1], name='p_mask')
            gt_place['n_mask'] = tf.placeholder(dtype=dtype, shape=[None, None, None, 1], name='n_mask')
            # avoid learning illegal anchor
            gt_place['anchor_mask'] = tf.placeholder(
                dtype=dtype, shape=[None, None, None, cluster_object_count], name='anchor_mask')
            pass
        self._gt_place = gt_place
        pass

    @property
    def Place(self):
        return self._gt_place

    def __generate(self):
        return self._gt_place
        pass

    @property
    def Class(self):
        return self._gt_place['class']

    @property
    def Y(self):
        return self._gt_place['y']

    @property
    def X(self):
        return self._gt_place['x']

    @property
    def H(self):
        return self._gt_place['h']

    @property
    def W(self):
        return self._gt_place['w']

    @property
    def PMask(self):
        return self._gt_place['p_mask']

    @property
    def NMask(self):
        return self._gt_place['n_mask']

    @property
    def LegalAnchor(self):
        return self._gt_place['anchor_mask']

    pass


# : the pro tensor is not easy to used in calc loss, make same process in this function, this function should make
# : sure gradient can propagate directly
def __split_pro_ac(pro, class_num, cluster_object_count):
    """
    to split the pro of yolo2 into several part
    :param pro: the pro of gen_pro
    :param class_num: class amount
    :param cluster_object_count: prior anchor amount
    :return:
        {'pro': pro, 'anchor': anchor_pro, 'precision': precision_pro, 'class': class_pro,
            'y': y_pro, 'x': x_pro, 'h': h_pro, 'w': w_pro}
        pro: the input pro [y, x, h, w, precision, class_part, .., ..., ]
        anchor: take all anchor and concat then[batch, cell_height, cell_width, cluster_object_count, 4(include [y, x, h, w])]
        precision:[batch, cell_height, cell_width, cluster_object_count]
        class:[batch * cell_height * cell_width * cluster_object_count, class_amount]
        y: [batch, cell_height, cell_width, cluster_object_count]
        x: [batch, cell_height, cell_width, cluster_object_count]
        h: [batch, cell_height, cell_width, cluster_object_count]
        w: [batch, cell_height, cell_width, cluster_object_count]
    """
    with tf.name_scope('split_and_pro'):
        # generate all part y x: sigmoid; h w: None; precision: sigmoid; class: part softmax
        with tf.name_scope('total_split'):
            with tf.name_scope('y_part'):
                y_part = pro[:, :, :, 0: ((cluster_object_count - 1) * (4 + 1 + class_num) + 1): 4 + 1 + class_num]
                y_pro = y_part
                pass
            with tf.name_scope('x_part'):
                x_part = pro[:, :, :, 1: ((cluster_object_count - 1) * (4 + 1 + class_num) + 2): 4 + 1 + class_num]
                x_pro = x_part
                pass
            with tf.name_scope('h_part'):
                h_part = pro[:, :, :, 2: ((cluster_object_count - 1) * (4 + 1 + class_num) + 3): 4 + 1 + class_num]
                h_pro = h_part
                pass
            with tf.name_scope('w_part'):
                w_part = pro[:, :, :, 3: ((cluster_object_count - 1) * (4 + 1 + class_num) + 4): 4 + 1 + class_num]
                w_pro = w_part
                pass
            with tf.name_scope('precision_part'):
                precision_part = pro[:, :, :,
                                 4: ((cluster_object_count - 1) * (4 + 1 + class_num) + 5): 4 + 1 + class_num]
                precision_pro = precision_part
                pass
            with tf.name_scope('class_part'):
                class_part = tf.reshape(pro, [-1, 4 + 1 + class_num])
                class_part = class_part[:, 5::]
                class_pro = class_part
                pass
            pass
        with tf.name_scope('anchor_pro'):
            anchor_pro = tf.concat(
                [tf.expand_dims(y_pro, axis=-1), tf.expand_dims(x_pro, -1), tf.expand_dims(h_pro, -1),
                 tf.expand_dims(w_pro, -1)],
                axis=-1)

    return {'pro': pro, 'anchor': anchor_pro, 'precision': precision_pro, 'class': class_pro,
            'y': y_pro, 'x': x_pro, 'h': h_pro, 'w': w_pro}
    pass


# : this function is used to generate the standard pro in yolo-version2 network, which split into
# {'pro': pro, 'anchor': anchor_pro, 'precision': precision_pro, 'class': class_pro,
#            'y': y_pro, 'x': x_pro, 'h': h_pro, 'w': w_pro}
def gen_pro(other_new_feature, class_num, cluster_object_count, _dtype=0.32):
    """
    pro = {'pro': pro, 'anchor': anchor_pro, 'precision': precision_pro, 'class': class_pro,
            'y': y_pro, 'x': x_pro, 'h': h_pro, 'w': w_pro}
    :param other_new_feature: base net feature
    :param class_num:
    :param cluster_object_count:
    :return:
    """
    print(Fore.YELLOW + '-----------generate yolo2 base pro---------')
    print(Fore.GREEN + 'class_num : ', class_num)
    print(Fore.GREEN + 'cluster_object_count : ', cluster_object_count)
    feature_chanel = other_new_feature.shape.as_list()[-1]
    dtype = tfu.tf_type(_dtype).Type
    with tf.name_scope('yolo_pro'):
        weight = tf.get_variable(
            name='compress_w',
            shape=[1, 1, feature_chanel, cluster_object_count * (class_num + 4 + 1)],
            initializer=layers.variance_scaling_initializer(seed=0.5, mode='FAN_AVG'),
            dtype=dtype
        )
        # bias = tf.get_variable(
        #     name='compress_b',
        #     shape=[cluster_object_count * (class_num + 4 + 1)],
        #     initializer=layers.variance_scaling_initializer(seed=0.5, mode='FAN_AVG'),
        #     dtype=dtype
        # )
        conv = tf.nn.conv2d(other_new_feature, weight, [1, 1, 1, 1], padding='SAME', name='conv')
        # add = tf.nn.bias_add(conv, bias, name='bias_add')
        add = conv
        pass
    pro = __split_pro_ac(add, class_num, cluster_object_count)
    return pro
    pass


# : the result of place_gt are not easy to used to calc loss, make some process in the function
def __place_process(gt_place_result, class_num, prior_h, prior_w, scalar, _dtype):
    """
    process the placeholder for using in the network easier
    :param gt_place_result: the result of placeholder
    :param class_num: the count of the class type
    :param prior_h: prior height list
    :param prior_w: prior width list
    :param scalar: down sample scalar
    :return:
    """
    dtype = tfu.tf_type(_dtype).Type
    gt_process = dict()
    assert len(prior_h) == len(prior_w), Fore.RED + 'len of the prior_h and prior_w should be the same'
    with tf.name_scope('gt_place_process'):
        gt_process_one_hot = tf.one_hot(
            gt_place_result['class'],
            class_num,
            1.0,
            0.0,
            name='one_hot',
            dtype=dtype)
        gt_process['class'] = tf.reshape(gt_process_one_hot, [-1, class_num], name='one_hot_reshape')

        gt_process['feed_class'] = gt_place_result['class']
        gt_process['y_offset'] = tf.floormod(gt_place_result['y'], scalar)
        gt_process['y'] = tf.div(gt_process['y_offset'], scalar)
        gt_process['y_feed'] = gt_place_result['y']
        gt_process['x_offset'] = tf.floormod(gt_place_result['x'], scalar)
        gt_process['x'] = tf.div(gt_process['x_offset'], scalar)
        gt_process['x_feed'] = gt_place_result['x']
        gt_process['h'] = tf.log(tf.div(gt_place_result['h'] + 1.0e-32, prior_h))
        gt_process['h_feed'] = gt_place_result['h']
        gt_process['w'] = tf.log(tf.div(gt_place_result['w'] + 1.0e-32, prior_w))
        gt_process['w_feed'] = gt_place_result['w']

        gt_process['anchor_mask'] = gt_place_result['anchor_mask']
        gt_process['negative_anchor_mask'] = 1 - gt_place_result['anchor_mask']
        pass
    return gt_process


# : to read the pro result, avoid the gradient propagate from precision loss to the network twice
def __pro_result_reader(split_pro_result):
    """
    read the pro result, avoid the gradient propagate from precision loss to the network twice
    :param split_pro_result: __split_pro result
    :return:
    """
    pro_result_read = dict()
    pro_result_read['y'] = tf.identity(split_pro_result['y'], name='y_read')
    pro_result_read['x'] = tf.identity(split_pro_result['x'], name='x_read')
    pro_result_read['h'] = tf.identity(split_pro_result['h'], name='h_read')
    pro_result_read['w'] = tf.identity(split_pro_result['w'], name='w_read')
    return pro_result_read
    pass


# :use gt_anchor and anchor_pro to calc iou， output for calc precision loss
def __calc_iou(pro_result_read_result, place_process_result, scalar, prior_h, prior_w, _dtype):
    yt = place_process_result['y_offset']
    xt = place_process_result['x_offset']
    ht = place_process_result['h_feed']
    wt = place_process_result['w_feed']
    anchor_mask = place_process_result['anchor_mask']
    with tf.name_scope('calc_iou'):
        yp = pro_result_read_result['y'] * scalar
        xp = pro_result_read_result['x'] * scalar
        hp = tf.multiply(tf.exp(pro_result_read_result['h']), prior_h)
        wp = tf.multiply(tf.exp(pro_result_read_result['w']), prior_w)
        min_bottom = tf.reduce_min(
            tf.concat([tf.expand_dims(yp + 0.5 * hp, -1), tf.expand_dims(yt + 0.5 * ht, -1)], axis=-1), axis=-1)
        max_top = tf.reduce_max(
            tf.concat([tf.expand_dims(yp - 0.5 * hp, -1), tf.expand_dims(yt - 0.5 * ht, -1)], axis=-1), axis=-1)
        min_right = tf.reduce_min(
            tf.concat([tf.expand_dims(xp + 0.5 * wp, -1), tf.expand_dims(xt + 0.5 * wt, -1)], axis=-1), axis=-1)
        max_left = tf.reduce_max(
            tf.concat([tf.expand_dims(xp - 0.5 * wp, -1), tf.expand_dims(xt - 0.5 * wt, -1)], axis=-1), axis=-1)
        cross_area = tf.multiply(tf.nn.relu(min_right - max_left), tf.nn.relu(min_bottom - max_top), name='cross_area')
        pass
    all_iou = tf.div(
        cross_area,
        tf.subtract(tf.add(tf.multiply(ht, wt, name='gt_area'), tf.multiply(hp, wp, name='pre_area')), cross_area),
        name='all_iou')
    iou = tf.multiply(all_iou, anchor_mask, name='iou_apply_anchor_mask')
    return iou
    pass


# : generate the loss op
def __calc_loss(split_pro_result, gt_process_result, calc_iou_result, anchor_loss_weight=1.0, precision_loss_weight=1.0,
                class_loss_weight=1.0, lambda_obj=1.0, lambda_nobj=1.0):
    y_pro = split_pro_result['y']
    x_pro = split_pro_result['x']
    h_pro = split_pro_result['h']
    w_pro = split_pro_result['w']
    precision_pro = split_pro_result['precision']
    class_pro = split_pro_result['class']
    anchor_mask = gt_process_result['anchor_mask']
    negative_anchor_mask = gt_process_result['negative_anchor_mask']
    gt_y = gt_process_result['y']
    gt_x = gt_process_result['x']
    gt_h = gt_process_result['h']
    gt_w = gt_process_result['w']
    gt_class = gt_process_result['class']

    legal_anchor_amount = tf.add(tf.reduce_sum(anchor_mask, name='legal_anchor_amount'), 1.0e-32, name='avoid_zero')
    negative_anchor_amount = tf.add(tf.reduce_sum(negative_anchor_mask, name='negative_anchor_amount'), 1.0e-32,
                                    name='avoid_zero')

    with tf.name_scope('process'):
        anchor_mask_reshape = tf.reshape(anchor_mask, [-1])
        pass

    with tf.name_scope('indicator'):
        with tf.name_scope('iou'):
            iou = tf.div(tf.reduce_sum(tf.multiply(calc_iou_result, anchor_mask, name='apply_anchor_mask')),
                         legal_anchor_amount, name='average_iou')
            pass
        with tf.name_scope('top_one_classify_acc'):
            # important:
            # if pro_class or class_pro has all zero or equal data just like [[0, 0], ...]
            # it would make the top location mixed
            # so we must calculate the score to make it more sense:
            # correct_score_sum / legal_anchor_amount
            wrong_mask = tf.multiply(tf.cast(tf.subtract(tf.argmax(class_pro, axis=-1),
                                                         tf.argmax(gt_class, axis=-1)), dtype=anchor_mask.dtype),
                                     anchor_mask_reshape)
            correct_mask = tf.multiply(tf.subtract(1.0, wrong_mask), anchor_mask_reshape)
            # correct_count = tf.count_nonzero(correct_mask, dtype=legal_anchor_amount.dtype)
            correct_score_amount = tf.reduce_sum(tf.multiply(tf.reduce_max(tf.nn.softmax(class_pro, axis=-1)), correct_mask))
            # classify_top_one_acc = tf.multiply(tf.div(correct_count, legal_anchor_amount),
            #                                    tf.div(correct_score_amount, legal_anchor_amount))
            classify_top_one_acc = tf.div(correct_score_amount, legal_anchor_amount)
            pass
        pass

    with tf.name_scope('loss'):
        with tf.name_scope('anchor_loss'):
            # yx loss part
            with tf.name_scope('yx_loss'):
                yx_loss = tf.add(
                    tf.square(tf.subtract(y_pro, gt_y, name='y_sub') * anchor_mask, name='y_square'),
                    tf.square(tf.subtract(x_pro, gt_x, name='x_sub') * anchor_mask, name='x_square'),
                    name='y_x_add')
                pass
            # hw loss part
            with tf.name_scope('hw_loss'):
                hw_loss = tf.add(
                    tf.square(tf.subtract(tf.sqrt(h_pro * anchor_mask, name='h_pro_sqrt'),
                                          tf.sqrt(gt_h * anchor_mask, name='gt_h_sqrt'), name='h_sub'),
                              name='h_square'),
                    tf.square(tf.subtract(tf.sqrt(w_pro * anchor_mask, name='w_pro_sqrt'),
                                          tf.sqrt(gt_w * anchor_mask, name='gt_w_sqrt'), name='w_sub'),
                              name='w_square'),
                    name='hw_add')
                pass

            # anchor loss
            anchor_loss = tf.add(
                tf.multiply(
                    lambda_obj,
                    tf.div(
                        tf.reduce_sum(yx_loss, name='batch_sum'),
                        legal_anchor_amount,
                        name='yx_anchor_obj_mean'),
                    name='apply_lambda_weight'),
                tf.multiply(
                    lambda_obj,
                    tf.div(
                        tf.reduce_sum(hw_loss, name='batch_sum'),
                        legal_anchor_amount,
                        name='hw_anchor_obj_mean'),
                    name='apply_lambda_weight'),
                name='anchor_loss_sum'
            )
            anchor_loss = tf.multiply(anchor_loss, anchor_loss_weight, name='apply_anchor_loss_weight')
            # anchor_loss = gt_w
            pass
        with tf.name_scope('precision_loss'):
            precision_loss_all = tf.square(tf.subtract(precision_pro, calc_iou_result))
            p_precision_loss = lambda_obj * tf.div(
                tf.reduce_sum(tf.multiply(precision_loss_all, anchor_mask, name='apply_anchor_mask')),
                legal_anchor_amount)
            n_precision_loss = lambda_nobj * tf.div(
                tf.reduce_sum(tf.multiply(precision_loss_all, negative_anchor_mask, name='apply_negative_anchor_mask')),
                negative_anchor_amount)
            precision_loss = tf.add(p_precision_loss, n_precision_loss, name='sum')
            precision_loss = tf.multiply(precision_loss, precision_loss_weight, name='apply_precision_loss_weight')
            # precision_loss = tf.add(p_precision_loss, n_precision_loss, name='loss')
            pass
        with tf.name_scope('class_loss'):
            # class calc softmax entropy loss and multiply the anchor mask
            class_loss_whole = tf.multiply(
                tf.nn.softmax_cross_entropy_with_logits_v2(labels=gt_class, logits=class_pro),
                tf.reshape(anchor_mask, [-1]),
                name='class_loss')
            _class_loss = tf.multiply(
                lambda_obj,
                tf.div(tf.reduce_sum(class_loss_whole, name='batch_sum'), legal_anchor_amount,
                       name='class_anchor_obj_mean'),
                name='apply_lambda_weight')
            # _class_loss = class_loss_whole
            # _class_loss = legal_anchor_amount
            class_loss = tf.multiply(_class_loss, class_loss_weight, name='apply_class_loss_weight')
            pass
        total_loss = tf.add(anchor_loss, tf.add(precision_loss, class_loss), name='total_loss')
        pass
    return {'total_loss': total_loss, 'anchor_loss': anchor_loss, 'precision_loss': precision_loss,
            'class_loss': class_loss, 'mean_iou': iou, 'classify_top_one_acc': classify_top_one_acc}
    pass


import six
import abc


@six.add_metaclass(abc.ABCMeta)
class Yolo2GenerateI(object):
    """
    use normal information to generate the tensor feeding into the network build with above function
    generate: y, x, w, h, class, obj_mask, nobj_mask, anchor_mask
    """

    @abc.abstractmethod
    def _default_generate_feed_function(self, param):
        pass

    @abc.abstractmethod
    def CheckGenerateFeedParamFit(self, param):
        pass

    @abc.abstractmethod
    def _default_generate_result_function(self, param):
        pass

    @abc.abstractmethod
    def CheckGenerateResultParamFit(self, param):
        pass

    pass


@six.add_metaclass(abc.ABCMeta)
class Yolo2Generate(Yolo2GenerateI):
    def __init__(self):
        self._generate_feed_function = self._default_generate_feed_function
        self._generate_result_function = self._default_generate_result_function
        pass

    def GenerateFeed(self, param):
        Yolo2GenerateLogger.info('-->GenerateFeed')
        return self._generate_feed_function(param)
        pass

    def GenerateResult(self, param):
        return self._generate_result_function(param)
        pass

    pass


"""
StandardYolo2Generate: 
    the paper use:
        the center of prior anchor is locate at (i * scalar, j * scalar)

        anchor mask:[batch, cell_height, cell_width, prior_anchor_amount]
            every obj get one and only one nearest anchor to predict
            any anchor does not hold an obj would be rejected, place zero
            any anchor cross the edge of image was reject， place zero
*************************************important*************************************            
            (some conditions:
                if more than one prior anchor Iou gt_x, get the same maximum value,
                they would be hold to the gt_x at the same time
                if no more prior to provide gt_prediction this gt would be abandon)
#####################################important#####################################

        obj mask:[batch, cell_height, cell_width, prior_anchor_amount] 
            any cell does not hold any obj place zero
            any cell does hold any obj place one

        nobj mask:[batch, cell_height, cell_width, prior_anchor_amount]
            any cell does not hold any obj place one
            any cell does hold any obj place zero

        y:[batch, cell_height, cell_width, prior_anchor_amount]
            y = (real_center_y % scalar) / scalar

        x:[batch, cell_height, cell_width, prior_anchor_amount]
            x = (real_center_x % scalar) / scalar

        h:[batch, cell_height, cell_width, prior_anchor_amount]
            h = ln(real_height / prior_height)

        w:[batch, cell_height, cell_width, prior_anchor_amount]
            w = ln(real_width / prior_width)

        class:[batch, cell_height, cell_width, prior_anchor_amount]
            class = obj_represent_int
"""
import Putil.calc.estimate as es


class StandardYolo2Generate(Yolo2Generate):
    def __init__(self, prior_hw, scalar):
        Yolo2Generate.__init__(self)

        self.feed_height = None
        self.feed_width = None

        self.y = None
        self.x = None
        self.h = None
        self.w = None
        self.anchor_mask = None
        self.classify = None
        self.obj_mask = None
        self.nobj_mask = None

        self.scalar = scalar
        self._dtype = None
        self.prior_hw = prior_hw
        self.anchor_amount = len(prior_hw)
        pass

    def __update_feed_shape(self, feed_height, feed_width, anchor_amount, _dtype):
        """
        while any parameter include batch, feed_height, feed_width, anchor_amount, _dtype
        changed, the tensor shape or type should be changed
        this is the function for updating the tensor
        :return:
        """
        self._dtype = _dtype
        self.feed_height = feed_height
        self.feed_width = feed_width
        self.anchor_amount = anchor_amount
        dtype = npu.np_type(self._dtype).Type
        self.y = np.zeros(shape=[1, self.feed_height, self.feed_width, self.anchor_amount], dtype=dtype)
        self.x = np.zeros(shape=[1, self.feed_height, self.feed_width, self.anchor_amount], dtype=dtype)
        self.h = np.zeros(shape=[1, self.feed_height, self.feed_width, self.anchor_amount], dtype=dtype)
        self.w = np.zeros(shape=[1, self.feed_height, self.feed_width, self.anchor_amount], dtype=dtype)
        self.anchor_mask = np.zeros(shape=[1, self.feed_height, self.feed_width, self.anchor_amount], dtype=dtype)
        self.classify = np.zeros(shape=[1, self.feed_height, self.feed_width, self.anchor_amount], dtype=dtype)
        pass

    # unused
    def __cross_edge_anchor_reject(self):
        """
        process the anchor mask to make the anchor which cross the edge of image zero
        :param batch:
        :param feed_height:
        :param feed_width:
        :param anchor_amount:
        :param _dtype:
        :return:
        """
        anchor_mask_shape = self.anchor_mask.shape
        # calculate the allowed band for box to expand in the anchor mask[batch, feed_height, feed_width, anchor_amount, 4]
        # 4: [top_height_band, bottom_height_band, left_width_band, right_width_band]
        max_band_h = anchor_mask_shape[1]
        max_band_w = anchor_mask_shape[2]
        top_height_band = np.expand_dims(
            np.linspace(0, max_band_h - 1, num=max_band_h).repeat(max_band_w).reshape([max_band_h, max_band_w]), -1)
        bottom_height_band = np.expand_dims(
            np.linspace(0, max_band_h - 1, num=max_band_h)[::-1].repeat(max_band_w).reshape([max_band_h, max_band_w]),
            -1)
        left_width_band = np.expand_dims(
            np.linspace(0, max_band_w - 1, num=max_band_w).repeat(max_band_h).reshape([max_band_w, max_band_h]).T, -1)
        right_width_band = np.expand_dims(
            np.linspace(0, max_band_w - 1, num=max_band_w)[::-1].repeat(max_band_h).reshape([max_band_w, max_band_h]).T,
            -1)
        band_t_b_l_r = np.concatenate((top_height_band, bottom_height_band, left_width_band, right_width_band), -1)
        # calculate the prior wh expand in the anchor mask[batch, feed_height, feed_width, anchor_amount, 4]
        # subtract, replace negative by zero, multiply, and then concat
        prior_expand_t_b_1_r_list = []
        rejected = []
        for i in self.prior_hw:
            expand = np.array([0.5 * i[0], 0.5 * i[0], 0.5 * i[1], 0.5 * i[1]]).repeat(max_band_h * max_band_w).reshape(
                max_band_h, max_band_w, 4)
            expanded = band_t_b_l_r - expand
            expanded[expanded < 0] = 0
            rejected.append(expanded[:, :, 0] * expanded[:, :, 1] * expanded[:, :, 2] * expanded[:, :, 3])
            pass
        rejected = np.concatenate(rejected)
        # multiply the anchor mask
        return rejected
        pass

    def __find_same_cell_location(self, scalar, gt_box, classify):
        """
        use scalar and gt_box to generate same cell format
        [[gt_box, ...](the box in the same cell, [cell], [offset, ...]...]
        gt_box: [y, x, h, w]; cell: [cell_y=gt_box.y//scalar, cell_x=gt_box.x//scalar];
        offset: [offset_y=gt_box.y%scalar, offset_x=gt_box.x%scalar]
        :param scalar:
        :param gt_box:
        :return:
        """
        format = list()
        # sort by y**2 + x**2 get the index
        array_gt_box = np.array(gt_box)
        order = (array_gt_box[:, 0] ** 2 + array_gt_box[:, 1] ** 2).argsort()
        killed = []
        for i in zip(order, range(0, len(order))):
            index_ = i[0]
            order_index_ = i[1]
            if index_ in killed:
                continue
                pass
            cell_y = gt_box[index_][0] // scalar
            cell_x = gt_box[index_][1] // scalar
            offset_y = gt_box[index_][0] % scalar
            offset_x = gt_box[index_][1] % scalar
            format.append([[]])
            format[-1][0].append(gt_box[index_])
            format[-1].append([cell_y, cell_x])
            format[-1].append([])
            format[-1][2].append([offset_y, offset_x])
            format[-1].append([])
            format[-1][3].append(classify[index_])
            for j in order[order_index_ + 1:]:
                if (gt_box[index_][0] // scalar == gt_box[j][0] // scalar) & (
                        gt_box[index_][1] // scalar == gt_box[j][1] // scalar):
                    # add to the format and add to killed
                    offset_y = gt_box[j][0] % (scalar - 1)
                    offset_x = gt_box[j][1] % (scalar - 1)
                    format[-1][0].append(gt_box[j])
                    format[-1][2].append([offset_y, offset_x])
                    format[-1][3].append(classify[j])
                    killed.append(j)
                    pass
                else:
                    break
                    pass
                pass
            pass
        return format
        pass

    def _default_generate_feed_function(self, param):
        """

        :param param: dict
            gt_box: support batch [[obj_0_yxhwc, obj_1_yxhwc, ...obj_n_yxhwc..., ], sample_1, sample_2, ....]
            feed_height:
            feed_width:
            class:
            _dtype:
        :return:
        """
        StandardYolo2GenerateLogger.debug('-->_default_generate_feed_function')
        gt_box = param['gt_box']
        feed_height = param['feed_height']
        feed_width = param['feed_width']
        classify = param['class']

        _dtype = param['_dtype']

        if (feed_height != self.feed_height or feed_width != self.feed_width) \
                or (self.feed_height is None and self.feed_width is None) or (_dtype != self._dtype):
            self.__update_feed_shape(feed_height, feed_width, self.anchor_amount, _dtype)

        gt_format = self.__find_same_cell_location(scalar=self.scalar, gt_box=gt_box, classify=classify)

        for i in gt_format:
            ohw = np.concatenate([i[0], i[2]], -1)
            iou_matrix = es.calc_iou_matrix_ohw(
                self.prior_hw,
                ohw,
                group1_h_index=0,
                group1_w_index=1,
                group2_y_index=4,
                group2_x_index=5,
                group2_h_index=2,
                group2_w_index=3
            )

            box__ = i[0]
            cell__ = i[1]
            offset__ = i[2]
            classify__ = i[3]
            cell_obj_amount = len(i[0])
            cell_y__ = cell__[0]
            cell_x__ = cell__[1]

            for j in range(0, cell_obj_amount):
                max_iou = np.max(iou_matrix)

                location = np.where(iou_matrix == max_iou)
                for k in zip(location[0], location[1]):
                    anchor__ = k[0]
                    obj__ = k[1]
                    box_item__ = box__[obj__]
                    prior_box_ = self.prior_hw[anchor__]
                    offset_ = offset__[obj__]
                    self.anchor_mask[0, cell_y__, cell_x__, anchor__] = 1.0
                    self.y[0, cell_y__, cell_x__, anchor__] = box_item__[0]
                    self.x[0, cell_y__, cell_x__, anchor__] = box_item__[1]
                    self.h[0, cell_y__, cell_x__, anchor__] = box_item__[2]
                    self.w[0, cell_y__, cell_x__, anchor__] = box_item__[3]
                    self.classify[0, cell_y__, cell_x__, anchor__] = classify__[obj__]
                    # self.anchor_mask[]
                    pass
                pass
            pass
        return {'y': self.y, 'x': self.x, 'h': self.h, 'w': self.w, 'class': self.classify,
                'anchor_mask': self.anchor_mask}
        pass

    @property
    def FindSameCellLocation(self):
        return self.__find_same_cell_location
        pass

    def __divide_anchor(self, gt_format_item):
        """
        use the output of __find_same_cell_location to divide anchor's owner
        :param gt_format:
        :return:
        """

        pass

    def CheckGenerateFeedParamFit(self, param):
        return True
        pass

    def _default_generate_result_function(self, param):
        """
        :param param:
        :return:
        """
        threshold = param['threshold']
        y_pro__ = param['y']
        x_pro__ = param['x']
        h_pro__ = param['h']
        w_pro__ = param['w']
        shape = y_pro__.shape
        precision_pro__ = param['precision']
        class_pro__ = param['class']

        ret = list()

        cell_accept = np.where(precision_pro__ >= threshold)
        for location in zip(cell_accept[0], cell_accept[1], cell_accept[2], cell_accept[3]):
            batch_l = location[0]
            cell_height_l = location[1]
            cell_width_l = location[2]
            anchor_l = location[3]

            pre_l = precision_pro__[batch_l, cell_height_l, cell_width_l, anchor_l]
            y_l = self.scalar * (cell_height_l + y_pro__[batch_l, cell_height_l, cell_width_l, anchor_l])
            x_l = self.scalar * (cell_width_l + x_pro__[batch_l, cell_height_l, cell_width_l, anchor_l])
            h_l = self.prior_hw[anchor_l][0] * np.exp(h_pro__[batch_l, cell_height_l, cell_width_l, anchor_l])
            w_l = self.prior_hw[anchor_l][1] * np.exp(w_pro__[batch_l, cell_height_l, cell_width_l, anchor_l])
            class_get = class_pro__[
                        batch_l * (shape[0] * shape[1] * shape[2]) + cell_height_l * shape[2] + cell_width_l * shape[
                            3] + anchor_l, :]
            class_l = np.where(class_get == np.max(class_get))
            ret.append({'y': y_l, 'x': x_l, 'h': h_l, 'w': w_l, 'class': class_l, 'pre': pre_l})
            pass
        return ret
        pass

    def CheckGenerateResultParamFit(self, param):
        return True
        pass

    pass

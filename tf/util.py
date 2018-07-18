# coding = utf-8
import tensorflow as tf
from Putil.np import util

_tf_type = {
    0.32: tf.float32,
    32: tf.int32,
    0.64: tf.float64,
    64: tf.int64,
    8: tf.uint8,
    -8: tf.int8,
    0.16: tf.float16,
    16: tf.int16
}


class tf_type:
    def __init__(self, label):
        self._type = _tf_type[label]
        self._label = label
        pass

    @property
    def Type(self):
        return self._type

    def to_np(self):
        return util._np_type[self._label]
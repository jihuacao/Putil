# coding=utf-8
from abc import ABCMeta, abstractmethod, ABC


class Sample(ABC):
    def __init__(self):
        self._pdf_func = None
        pass

    def set_pdf_func(self, pdf_func):
        self._pdf_func = pdf_func
        pass

    @abstractmethod
    def sample(self):
        pass
    pass
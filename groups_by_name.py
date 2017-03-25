# coding=utf-8
# Copyright(c) 2017, Oleg Rezvov
# @PRSPKT, http://prspkt.ru
__author__ = "ООО АБ Проспект"

# region import
import clr

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager


def get_name(_list):
    for i in _list:
        _list_name = i.Name
        yield _list_name


def get_group_name(_list):
    _lst = []
    for i in set(get_name(_list)):
        sublist = []
        for k in _list:
            if k.Name == i:
                sublist.append(k)
        _lst.append(sublist)
    return _lst


def get_group_name1(_list):
    uniq = set((i.Name for i in _list))
    _lst = []
    for i in uniq:
        _lst.append([k for k in _list if k.Name == i])
    return _lst

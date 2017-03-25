# coding=utf-8
# Copyright(c) 2017, Oleg Rezvov
# @PRSPKT, http://prspkt.ru
__author__ = "ООО АБ Проспект"

# region import
import clr

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

# Import Element wrapper extension methods
clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)

# Import geometry conversion extension methods
clr.ImportExtensions(Revit.GeometryConversion)

# Import DocumentManager and TransactionManager
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

# Import RevitAPI
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *

import System
from System import Array
from System.Collections.Generic import *

import sys

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

# The inputs to this node will be stored as a list in the IN variable.
dataEnteringNode = IN
collector = FilteredElementCollector
rooms = collector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()

koef = 0.092903

def round2(d):
    return round(d * koef, 2)

def get_rooms(_list):
    for i in _list:
        yield i


def get_rooms_type_1_2():
    for i in get_rooms(rooms):
        room_type = i.LookupParameter('Тип помещения').AsValueString()
        if room_type == '1' or room_type == '2':
            yield i


def get_room_names(_list):
    for i in _list:
        yield i.LookupParameter('Имя').AsString()
"""
def typefloor(_list):
    lst = []
    for i in _list:
        room_level_name = i.Level.Name
        room_area = round2(i.Area)
        if room_level_name == 'Этаж 2':
            lst.append(room_area)
        elif room_level_name == 'Этаж 3':
            lst.append(room_area * 5)
        elif room_level_name == 'Этаж 8':
            lst.append(room_area * 5)
        elif room_level_name == 'Этаж 9':
            lst.append(room_area * 8)
        elif room_level_name == 'Этаж 11':
            lst.append(room_area)
        elif room_level_name == 'Этаж 1':
            lst.append(room_area)
        elif room_level_name == '(Э)_Этаж 1(1)':
            lst.append(room_area)

    return sum(lst)
"""

def typefloor(_list):
    list_floor = IN[1]
    lst = []
    for i, r in enumerate(list_floor[0]):
        for lvl in get_rooms_type_1_2():
            room_level_name = lvl.Level.Name
            room_area = round2(lvl.Area)
            if room_level_name == r:
                lst.append(room_area * int(list_floor[1][i]))
    return lst
    # return sum(lst)

_lst = []
for i in get_rooms(rooms):
    room_level = i.Level.Name
    room_area = i.LookupParameter('Площадь').AsValueString()
    room_type = i.LookupParameter('Тип помещения').AsValueString()
    if room_level != 'Этаж -1' and room_level != 'Тех.антресоль' and room_area > 0 and (room_type == '1' or room_type == '2'):
        _lst.append(room_level)

_type1_2 = []
for i in get_rooms_type_1_2():
    room_level = i.Level.Name
    room_area = i.LookupParameter('Площадь').AsValueString()
    if room_level != 'Тех.антресоль':
        _type1_2.append(i)


OUT = _type1_2

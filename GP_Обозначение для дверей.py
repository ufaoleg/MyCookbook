# Copyright(c) 2017, Oleg Rezvov
# @PRSPKT, http://prspkt.ru
__author__ = "Oleg Rezvov"

import clr

clr.AddReference('ProtoGeometry')
import Autodesk.DesignScript.Geometry

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
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
activeV = doc.ActiveView

# Import RevitAPI
clr.AddReference("RevitAPI")
from Autodesk.Revit.DB import *

import System
from System import Array
from System.Collections.Generic import *

import sys
clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)


def ConvertTo(_element, _data):
    if _element and _data:
        s = _element.Symbol.LookupParameter(_data).AsValueString()
    return int(s)

def DefineFireproof(_title):
    door_EI = _title[_title.find("EI"):_title.find("0") + 1]
    return door_EI

def MakeUnique(_list):
    make_set = set(_list)
    return list(make_set)

def DefineMark(_list, int_type):
    CleanTypeList = []
    int_type = int(int_type)
    newMark = []
    mark = int_type + 0.01
    elementList = []
    for i in _list:
        if i.Name not in CleanTypeList:
            CleanTypeList.append(i.Name)
            newMark.append(mark)
            elementList.append(i)
            mark += 0.01
        else:
            pass
    return newMark, elementList

def ConvertToFloatStringWithDefineMark(_list, _type):
    m = DefineMark(_list, _type)
    return map(lambda x: "{:.2f}".format(x), m[0]), m[1]


doorList = FilteredElementCollector(doc).OfCategory(
    BuiltInCategory.OST_Doors).WhereElementIsNotElementType().ToElements()
outList = []
door_1 = []
door_2 = []
door_3 = []
door_4 = []

for door in doorList:
    if door.LookupParameter("Учитывать в подсчете").AsValueString() == "Да":
        door_name = door.Name
        if "1." in door_name:
            door_1.append(door)
        if "2." in door_name:
            door_2.append(door)
        if "3." in door_name:
            door_3.append(door)
        if "4." in door_name:
            door_4.append(door)

# OUT = sorted(outList, key = lambda x: (ConvertTo(x, "Ширина"), ConvertTo(x, "Высота")))
door_1 = sorted(door_1, key = lambda x: (DefineFireproof(x.Name), ConvertTo(x, "Ширина"), ConvertTo(x, "Высота")))
door_2 = sorted(door_2, key = lambda x: (DefineFireproof(x.Name), ConvertTo(x, "Ширина"), ConvertTo(x, "Высота")))
door_3 = sorted(door_3, key = lambda x: (ConvertTo(x, "Ширина"), ConvertTo(x, "Высота")))
door_4 = sorted(door_4, key = lambda x: (ConvertTo(x, "Ширина"), ConvertTo(x, "Высота")))

doorMark_1 = ConvertToFloatStringWithDefineMark(door_1, 1)
doorMark_2 = ConvertToFloatStringWithDefineMark(door_2, 2)
doorMark_3 = ConvertToFloatStringWithDefineMark(door_3, 3)
doorMark_4 = ConvertToFloatStringWithDefineMark(door_4, 4)

SortedDoorTypes = doorMark_1[1] + doorMark_2[1] + doorMark_3[1] + doorMark_4[1]
SortedDoorMarkList = doorMark_1[0] + doorMark_2[0] + doorMark_3[0] + doorMark_4[0]

#SortedDoorList = door_1
#SortedDoorMarkList = doorMark_1


#OUT = SortedDoorList
OUT = SortedDoorTypes, SortedDoorMarkList
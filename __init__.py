# coding=utf-8
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

incoming = UnwrapElement(IN[0])

ParamGroupName = "П_Группа помещений"
ParamRoomName = "П_Имя помещения"


def get_group_name(_list):
    _lst = []
    for group in set(_list.Select(lambda x: x.LookupParameter(ParamGroupName).AsString())):
        group_list = []
        for number in set(_list.Select(lambda x: x.LookupParameter(ParamRoomName).AsString())):
            number_list = []
            for room in _list:
                if room.LookupParameter(ParamGroupName).AsString() == group:
                    if room.LookupParameter(ParamRoomName).AsString() == number:
                        number_list.append(room)
            group_list.append(number_list)
        _lst.append(group_list)
    return _lst


def filter_empty_group(_list):
    output = []
    for group in get_group_name(_list):
        for subgroup in group:
            if subgroup:
                output.append(subgroup)
    return output


OUT = filter_empty_group(incoming)

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

# The inputs to this node will be stored as a list in the IN variable.
level1 = IN[1]
level2 = IN[2]
search_word = IN[3]
parameter_number = IN[4]
parameter_group = IN[5]
level3 = IN[6]

ParameterRoomName = "П_Имя помещения"
ParameterStairRoomName = "Лестнична"
ParameterTypeRoom = "П_Тип помещения"


def unwrap(item):
    return UnwrapElement(item)


def room_param(_iter, _name):
    if _name != ParameterRoomName:
        return _iter.LookupParameter(_name).AsValueString()
    else:
        return _iter.LookupParameter(_name).AsString()


def is_stair_room(room):
    room_name = room.LookupParameter(ParameterRoomName).AsString()
    if room_name.startswith(ParameterStairRoomName):
        return True
    else:
        return False


def get_list(_list, parameter):
    for i in _list:
        _list_name = i.LookupParameter(parameter).AsString()
        yield _list_name


def is_level_ok(room_level):
    if room_level == level1:  # or room_level == level2 or room_level == level3:
        return True
    else:
        return False


def get_group_name(_list):
    output = []
    for group in set(get_list(_list, parameter_group)):  # получаем список уникальных групп (без сортировки)
        group_list = []
        for number in set(get_list(_list, parameter_number)):  # подсписок помещений по номерам (без сортировки)
            number_list = []
            for k in _list: # подподсписок по помещениям
                if k.LookupParameter(parameter_group).AsString() == group:
                    if k.LookupParameter(parameter_number).AsString() == number:
                        number_list.append(k)
            group_list.append(number_list)
        output.append(group_list)
    return output


rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms)
rooms = rooms.Where(lambda x: is_level_ok(x.Level.Name))
rooms = rooms.Where(lambda x: not is_stair_room(x))
rooms = rooms.Where(lambda x: x.Area > 0)
rooms = rooms.Where(lambda x: x.LookupParameter(ParameterTypeRoom).AsValueString() == "5")
rooms = rooms.Select(lambda x: x)


walls = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Walls).WhereElementIsNotElementType().ToElements()
finishwalls = []
for el in walls:
    el_name = el.Name
    el_level = el.LookupParameter("Базовая зависимость")
    if search_word in el_name and is_level_ok(el_level.AsValueString()):
        finishwalls.append(el)
#OUT = [x.Level.Name for x in rooms]
OUT = [[[t for t in i if t != []] for i in get_group_name(rooms)], finishwalls]

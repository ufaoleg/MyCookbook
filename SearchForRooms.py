# Copyright(c) 2017, Oleg Rezvov
# @PRSPKT, http://prspkt.ru
__author__ = "ООО АБ Проспект"

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


def ProcessList(_func, _list):
    return map(lambda x: ProcessList(_func, x) if type(x) == list else _func(x), _list)


def ProcessListArg(_func, _list, _arg):
    return map(lambda x: ProcessListArg(_func, x, _arg) if type(x) == list else _func(x, _arg), _list)


def ProcessParallelLists(_func, *lists):
    return map(lambda *xs: ProcessParallelLists(_func, *xs) if all(type(x) is list for x in xs) else _func(*xs), *lists)


def Unwrap(item):
    return UnwrapElement(item)


# Convert single element to list
def ToList(x):
    if hasattr(x, '__iter__'):
        return x
    else:
        return [x]


def RoomParam(_iter, _pName):
    if _pName != "Имя":
        return _iter.LookupParameter(_pName).AsValueString()
    else:
        return _iter.LookupParameter(_pName).AsString()


def CheckStatus(_p1, _Lvl, _p2):
    if _p1 and _p1 == _Lvl:
        if _p2 and _p2 > 0.0:
            return True


res = []
lvl = IN[1]

# Создаем группы помещений
apartGroup = []  # Группа помещений квартиры
bathGroup = []  # Группа помещений ванн и санузлов
lodzhGroup = []  # Группа помещений лоджии
conditionGroup = []  # Группа помещений кондиционерной
balconyGroup = []  # Группа помещений балконов

try:
    errorReport = None
    rooms = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Rooms).ToElements()
    for room in rooms:
        roomName = RoomParam(room, "Имя")
        roomArea = RoomParam(room, "Площадь")
        roomLevel = RoomParam(room, "Уровень")
        roomType = RoomParam(room, "Тип помещения")
        if CheckStatus(roomLevel, lvl, roomArea):
            if roomType != "" and roomType:
                if int(roomType) < 3 and "конд" not in roomName:
                    if ("Ванная" != roomName) and ("Санузел" != roomName):
                        apartGroup.append(room)
                    elif ("Ванная" == roomName) or ("Санузел" == roomName):
                        bathGroup.append(room)
                elif int(roomType) != 5:
                    if roomName == "Лоджия":
                        lodzhGroup.append(room)
                    elif "конд" in roomName:
                        conditionGroup.append(room)
                    elif roomName == "Балкон":
                        balconyGroup.append(room)
                else:
                    res.append(room)


except:
    # if error accurs anywhere in the process catch it
    import traceback

    errorReport = traceback.format_exc()

# Assign your output to the OUT variable
if errorReport == None:
    OUT = [apartGroup, bathGroup, lodzhGroup, conditionGroup, balconyGroup, res]
else:
    OUT = errorReport
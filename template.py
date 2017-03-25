import clr

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

import sys

# sys.path.append(r"C:\Program Files\Dynamo 0.8")
pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

import os.path

import math

from operator import itemgetter, attrgetter
import string
import re

clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *

import System
from System import Array
from System.Collections.Generic import *
import Autodesk.DesignScript as ds

clr.AddReferenceByName(
    'Microsoft.Office.Interop.Excel, Version=11.0.0.0, Culture=neutral, PublicKeyToken=71e9bce111e9429c')
from Microsoft.Office.Interop import Excel

System.Threading.Thread.CurrentThread.CurrentCulture = System.Globalization.CultureInfo("en-US")
from System.Runtime.InteropServices import Marshal

clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)
from Revit.Elements import *

clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.GeometryReferences)

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

clr.AddReference("System.Core")
clr.ImportExtensions(System.Linq)

doc = DocumentManager.Instance.CurrentDBDocument
uidoc = DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

view = doc.ActiveView


def U(elem):  # короткая функция, чтобы каждый раз не писать UnwrapElement(), вместо этого достаточно U()
    return UnwrapElement(elem)


# пример для получения типа стены
walltypes = []
if isinstance(IN[0], list):  # если на входе лист
    for i in IN[0]:
        walltypes.append(U(i).WallType)
else:  # в противном случае (это означает, что на входе 1 элемент)
    walltypes = U(IN[0]).WallType

OUT = walltypes

# array = ModelCurveArray() # создание массива Array
# array.Append(UnwrapElement(i)) # положить элементы в массив

# Ids=List[ElementId]() #Icollection в данном случае для ElementId
# Ids.Add(UnwrapElement(i).Id) # добавить элементы в Icollection

# получение всех элементов категории OST_Wire кроме их типов
"""
wires = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Wire).WhereElementIsNotElementType().ToElements()
dstype=[]
for i in wires:
    dstype.append(i.ToDSType(True))
"""

# OUT = IN[0].split(‘/’) # разделить данные типа String по символу '/'

# ModelCurve to Line Dynamo
# UnwrapElement(IN[0]).GeometryCurve.ToProtoType()

# Line Dynamo to ModelLine
# ModelCurve.ByCurve(IN[0])

# получение параметра по его BuiltIn значению
# OUT = UnwrapElement(IN[0]).get_Parameter(BuiltInParameter.ELEM_FAMILY_PARAM).AsValueString()
# в зависимости от параметра окончание может быть также AsString() AsDouble()


TransactionManager.Instance.EnsureInTransaction(doc)

TransactionManager.Instance.TransactionTaskDone()

# new.ToDSType(False)

# coding=utf-8
# Copyright(c) 2017, Oleg Rezvov
# @PRSPKT, http://prspkt.ru
__author__ = "ООО АБ Проспект"

# region import
import clr

clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

clr.AddReference("RevitNodes")
import Revit

clr.ImportExtensions(Revit.Elements)
from Revit.Elements import *

clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

items = UnwrapElement(IN[0])
elementlist = []
for item in items:
    itemlist = []
    for wall in item:
        for insert in wall.FindInserts(True, 0, 0, 0):
            itemlist.append(wall.Document.GetElement(insert).ToDSType(True))
    elementlist.append(itemlist)
OUT = elementlist

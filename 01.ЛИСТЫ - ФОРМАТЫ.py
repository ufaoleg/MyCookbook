# coding=utf-8
# Copyright(c) 2018, Oleg Rezvov
# @PRSPKT Architects, http://prspkt.ru
__author__ = "ООО АБ Проспект"

# region import
import clr
# Import ProtoGeometry library
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
# Import Element wrapper extension methods
clr.AddReference('RevitNodes')
import Revit
# Import DocumentManager and TransactionManager
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

# Import RevitAPI
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *

from System.Collections.Generic import *

clr.ImportExtensions(Revit.Elements)
import System
from System import Array
from System.Collections.Generic import *

import sys

pyt_path = r'C:\Program Files (x86)\IronPython 2.7\Lib'
sys.path.append(pyt_path)

doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

input_razdel = IN[1]
list_ok, list_error = [], []

sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).ToElements()
title_blocks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsNotElementType().ToElements()

def is_not_edit(doc, e):
	flag = False
	if doc.IsWorkshared:
		name = e.LookupParameter("Редактирует").AsString()
		if name == "" or name == app.Username:
			flag = True
	else: flag = True
	return flag

def try_get_parameter(e, name, start = 0):
	"""
	 Проверить, существует ли такой параметр, и если да, то получить
	 значение в текстовом виде. Иначе - None
	"""
	param = e.LookupParameter(name)
	if param:
		return e.LookupParameter(name).AsString()[start:]
	return None

def get_titleblock_on_sheet(doc, sheet):
	"""
	Выборка всех элементов, принадлежащих FamilyInstance на каждом листе
	"""
	col = FilteredElementCollector(doc)
	out = col.OfClass(FamilyInstance).OwnedByView(sheet.Id).ToElements()[0]
	return out.Name

try:
	errorReport = None
	# Start Transaction
	TransactionManager.Instance.EnsureInTransaction(doc)
	for index, sheet in enumerate(sheets):
		if is_not_edit(doc, sheet):
			razdel = try_get_parameter(sheet, "Раздел проекта")
			number = try_get_parameter(sheet, "SH_Номер листа")
			new_number = try_get_parameter(sheet, "Номер листа", 1)
			titlebl = get_titleblock_on_sheet(doc, sheet)
			if razdel is not None and razdel == input_razdel:
				sheet.LookupParameter("Формат листа").Set(titlebl)
				list_ok.append(sheet)
		else:
			list_error.append(sheet)
	else:
		list_error.append(sheet)
	TransactionManager.Instance.TransactionTaskDone()
except:  # if error accurs anywhere in the process catch it
	import traceback
	errorReport = traceback.format_exc()
	# End Transaction
	TransactionManager.Instance.TransactionTaskDone()
if errorReport == None:
    OUT = list_ok, list_error
else:
	OUT = errorReport

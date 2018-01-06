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


def ProcessList(_func, _list):
    return map(lambda x: ProcessList(_func, x) if type(x) == list else _func(x), _list)

def ConvertDim(_length):
    if _length == 2070:
        return 21
    elif _length < 1000:
        return int(str(_length / 100)[:1])
    else:
        return int(str(_length / 100)[:2])

def ConvertBalconyDoor(_length):
    if not _length < 1000:
        return "ПО-СБ"
    else:
        return "РО"

koef = 304.8

if isinstance(IN[0], list):
    elements = []
    for i in IN[0]:
        elements.append(UnwrapElement(i))
else:
    elements = [UnwrapElement(IN[0])]

output = []
output_elements = []

try:
    errorReport = None
    for element in elements:
        el_width = element.Symbol.LookupParameter('Ширина').AsDouble() * koef
        el_height = element.Symbol.LookupParameter('Высота').AsDouble() * koef
        el_mark = element.Symbol.LookupParameter('GP_Марка').AsString()
        el_left_right = "Л" if element.Symbol.LookupParameter('Левая').AsValueString() == "Да" else ""
        el_type_name = element.Name
        el_EI = el_type_name[el_type_name.find("EI"):el_type_name.find("0 ")+1]
        if el_type_name.startswith("Тип 1."):
            output.append("ДПД {} {} ({:.0f}-{:.0f}(h))".format(el_EI, el_left_right, el_height, el_width))
            output_elements.append(element)
        if el_type_name.startswith("Тип 2."):
            output.append("ДПМ {} {} ({:.0f}-{:.0f}(h)) ГОСТ 53307-2009"\
                              .format(el_EI, el_left_right, el_height, el_width))
            output_elements.append(element)
        if el_type_name.startswith("Тип 3."):
            if "Дус" in el_type_name:
                output.append("ДУС {} {:.0f}-{:.0f} Серия 5.904-4"\
                              .format(el_left_right, el_height, el_width))
                output_elements.append(element)
            elif "Люк" in el_type_name:
                output.append("Люк металлический {} ({:.0f}-{:.0f}(h)) ГОСТ 31173-2003"\
                              .format(el_left_right, el_height, el_width))
                output_elements.append(element)
            else:
                output.append("ДСВ {} ({:.0f}-{:.0f}(h)) ГОСТ 31173-2003"\
                              .format(el_left_right, el_height, el_width))
                output_elements.append(element)
        if el_type_name.startswith("Тип 4."):
            output.append("ДГ {}-{}{} ГОСТ 6629-88".format(ConvertDim(el_height), ConvertDim(el_width), el_left_right))
            output_elements.append(element)
        if "оджи" in el_type_name:
            output.append("ДАН О Оп {} БПР Р {:.0f}х{:.0f}, ГОСТ 23747-2015" \
                .format(el_left_right, el_height, el_width))
            output_elements.append(element)
        """
        ОСП - одинарная конструкция со стеклопакетом
        Р - раздельная конструкция с листовыми стеклами
        О - одинарная конструкция с листовым стеклом
        ПО - поворотно-откидное открывание
        """
        if "БД" in el_type_name:
            if element.Symbol.LookupParameter('Левая').AsValueString() == 'Да':
                el_left_right = "Л"
            else:
                el_left_right = "П"
            output.append("БП ОСП {}-{}{} {} ГОСТ 23166-99".format(ConvertDim(el_width), ConvertDim(el_height), el_left_right, ConvertBalconyDoor(el_width)))
            output_elements.append(element)



except:  # if error accurs anywhere in the process catch it
    import traceback

    errorReport = traceback.format_exc()  # End Transaction
    TransactionManager.Instance.TransactionTaskDone()

# Assign your output to the OUT variable
if errorReport == None:
    OUT = [output_elements, output]
else:
    OUT = errorReport

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


def process_list(_func, _list):
    return map(lambda x: process_list(_func, x) if type(x) == list else _func(x), _list)


input_ = IN
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
        el_mark = element.Symbol.LookupParameter('Маркировка типоразмера').AsString()
        el_left_right = "Л" if element.Symbol.LookupParameter('Левая').AsValueString() == "Да" else ""
        el_type_name = element.Name
        el_EI = el_type_name[el_type_name.find("EI"):el_type_name.find("0") + 1]
        if el_type_name.startswith("Д.Мет") or el_type_name.startswith("ДП.Мет"):
            """
            Выборка металлических дверей
            """
            if "Люк" in el_type_name:
                """
                Если в названии встречается слово Люк,
                то записываем как люк
                """
                output.append("Люк металлический {} ({:.0f}-{:.0f}(h)) ГОСТ 31173-2003" \
                              .format(el_left_right, el_height, el_width))
                output_elements.append(element)
            elif "Дус" in el_type_name:
                """
                Если в названии встречается Дус,
                то записываем как Дверь стальная утепленная
                Обозначение: ДУС
                Серия 5.904-4
                """
                output.append("ДУС {} {:.0f}-{:.0f} Серия 5.904-4" \
                              .format(el_left_right, el_height, el_width))
                output_elements.append(element)
            elif "EI" not in el_type_name:
                """
                Обычные металлические двери
                Обозначение: ДСВ
                ГОСТ 31173-2003
                """
                output.append("ДСВ {} ({:.0f}-{:.0f}(h)) ГОСТ 31173-2003" \
                              .format(el_left_right, el_height, el_width))
                output_elements.append(element)
            else:
                """
                Если "EI" в названии, то записываем как противопожарные
                двери
                Обозначение: ДПМ
                ГОСТ 53307-2009
                """
                output.append("ДПМ {} {} ({:.0f}-{:.0f}(h)) ГОСТ 53307-2009" \
                              .format(el_EI, el_left_right, el_height, el_width))
                output_elements.append(element)
        if el_type_name.startswith("Д.Дер") or el_type_name.startswith("ДП.Дер"):
            if "EI" not in el_type_name:
                """
                Выборка деревянных дверей без "EI", то есть обычные
                Обозначение: ДГ
                Используется ГОСТ 6629-88
                """
                output.append("ДГ {}-{}{} ГОСТ 6629-88".format("21" if el_height == 2070 else str(el_height / 100)[:2],
                                                               str(el_width / 100)[:1] if el_width < 1000 else str(
                                                                   el_width / 100)[:2], el_left_right))
                output_elements.append(element)
            else:
                # output.append("ДПМ " + el_EI + " (" + str(el_width) + "x" + str(el_height) + "(h)")
                output.append("ДПД {} {} ({:.0f}-{:.0f}(h))".format(el_EI, el_left_right, el_height, el_width))
                output_elements.append(element)
        if "оджи" in el_type_name:
            """
            Поиск дверей для лоджий (переходная лоджия)
            Обозначение: ДГ
            Используется ГОСТ 23747-2015
            """
            output.append("ДАН О Оп {} БПР Р {:.0f}х{:.0f}, ГОСТ 23747-2015" \
                          .format(el_left_right, el_height, el_width))
            output_elements.append(element)


except:  # if error occurs anywhere in the process catch it
    import traceback

    errorReport = traceback.format_exc()  # End Transaction
    TransactionManager.Instance.TransactionTaskDone()

# Assign your output to the OUT variable
if errorReport is None:
    OUT = [output_elements, output]
else:
    OUT = errorReport

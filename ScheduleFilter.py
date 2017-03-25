# Copyright(c) 2017, Oleg Rezvov
# @PRSPKT, http://prspkt.ru
# -*- coding: utf-8 -*-
__author__ = "ООО АБ Проспект"

"""
Условия:
ScheduleFilterType.Equal - равно
LessThan - менее чем
BeginsWith - начинается с
EndsWith - заканчивается на
Contains - содержит ?
GreaterThan - больше чем
GreaterThanOrEqual - больше чем или равно
LessThanOrEqual - меньше чем или равно
Invalid
HasParameter
NotBeginsWith
NotContains
NotEndsWith
NotEqual

"""



inc = 304.8

TransactionManager.Instance.EnsureInTransaction(doc)

value = 10000 / inc # если фильтр по цифрам, например, длина, то перевод мм в футы
unit = schedule.Definition.GetField(0) # наименование колонки

filter = ScheduleFilter(unit.FieldId,
                        ScheduleFilterType.GreaterThanOrEqual, value) # создание фильтра
schedule.Definition.AddFilter(filter) # применить фильтр к спецификации

value = "АР" # наименование марки
unit = schedule.Definition.AddFilter(filter) # применить фильтр к спецификации

TransactionManager.Instance.TransactionTaskDone()
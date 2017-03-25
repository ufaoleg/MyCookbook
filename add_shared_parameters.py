# coding=utf-8
# Copyright(c) 2017, Oleg Rezvov
# @PRSPKT, http://prspkt.ru
__author__ = "ООО АБ Проспект"

import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
clr.AddReference("RevitServices")
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
doc = DocumentManager.Instance.CurrentDBDocument
uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application
from System.Collections.Generic import *
clr.AddReference("RevitNodes")
import Revit
clr.ImportExtensions(Revit.Elements)
import System
_paramName = []
_groupName = []
_paramType = []
_paramType2 = []
_category = []
_category2 = []
_paramGroup = []
_paramGroup2 = []
_instance = []
parameters = IN[0].split(";")
for parameter in parameters:
	paramName = parameter[:parameter.find("(")]
	_paramName.append(paramName)
	attrib = parameter[parameter.find("(")+1:parameter.find(")")+1]
	groupName = attrib[:attrib.find(",")]
	attrib = attrib[attrib.find(",")+1:]
	_groupName.append(groupName)
	paramType = attrib[:attrib.find(",")]
	attrib = attrib[attrib.find(",")+1:]
	_paramType2.append(paramType)
	#doc.Settings.Categories.Item(
	category = attrib[:attrib.find(",")]
	attrib = attrib[attrib.find(",")+1:]
	_category2.append(category)
	paramGroup = attrib[:attrib.find(",")]
	attrib = attrib[attrib.find(",")+1:]
	_paramGroup2.append(paramGroup)
	instance = attrib[:attrib.find(",")]
	attrib = attrib[attrib.find(",")+1:]
	_instance.append(int(float(instance)))
types=System.Enum.GetValues(ParameterType)
for i in _paramType2:
	for type in types:
		j = type.ToString()
		if i==j:
			_paramType.append(type)
categs = doc.Settings.Categories
for i in _category2:
	if "/" in i:
		_category3 = []
		i1 = i.split("/")
		for i2 in i1:
			for cat in categs:
				j = cat.Name.ToString()
				if i2 in j:
					_category3.append(cat)
		_category.append(_category3)
	else:
		for cat in categs:
			j = cat.Name.ToString()
			if i==j:
				_category.append(cat)
groups=System.Enum.GetValues(BuiltInParameterGroup)
name=[]
for i in _paramGroup2:
	for group in groups:
		j = group.ToString()
		if j==i:
			_paramGroup.append(group)
def ParamBindingExists(_doc, _paramName, _paramType):
	map = doc.ParameterBindings
	iterator = map.ForwardIterator()
	iterator.Reset()
	while iterator.MoveNext():
		if iterator.Key != None and iterator.Key.Name == _paramName and iterator.Key.ParameterType == _paramType:
			paramExists = True
			break
		else:
			paramExists = False
	return paramExists

def RemoveParamBinding(_doc, _paramName, _paramType):
	map = doc.ParameterBindings
	iterator = map.ForwardIterator()
	iterator.Reset()
	while iterator.MoveNext():
		if iterator.Key != None and iterator.Key.Name == _paramName and iterator.Key.ParameterType == _paramType:
			definition = iterator.Key
			break
	message = None
	if definition != None:
		map.Remove(definition)
		message = "Success"
	return message

def addParam(doc, _paramName, _visible, _instance, _groupName, _paramGroup,k):
	message = None
	if ParamBindingExists(doc, _paramName, _paramType):
		if not RemoveParamBinding(doc, _paramName, _paramType) == "Success":
			message = "Param Binding Not Removed Successfully"
		else:
			message = None
	group = file.Groups.get_Item(_groupName)
	if group == None:
		group = file.Groups.Create(_groupName)
	if group.Definitions.Contains(group.Definitions.Item[_paramName]):
		_def = group.Definitions.Item[_paramName]
	else:
   		_def = group.Definitions.Create(opt)
	param = doc.ParameterBindings.Insert(_def, bind, _paramGroup)
	return message
#"Start" the transaction
TransactionManager.Instance.EnsureInTransaction(doc)

try:
	file = app.OpenSharedParameterFile()
except:
	message = "No Shared Parameter file found."
	pass
k=0
while k<_paramName.Count:
	cats = app.Create.NewCategorySet()
	if isinstance(_category[k],list):
		for i in _category[k]:
			cats.Insert(i)
	else:
		cats.Insert(_category[k])
	if _instance[k]:
		bind = app.Create.NewInstanceBinding(cats)
	else:
		bind = app.Create.NewTypeBinding(cats)
	opt = ExternalDefinitionCreationOptions(_paramName[k], _paramType[k])
	opt.Visible = True
	message = addParam(doc, _paramName[k], True, _instance[k], _groupName[k], _paramGroup[k],k)
	k=k+1
TransactionManager.Instance.TransactionTaskDone()

if message == None:
	OUT = "Success"
else:
	OUT = message
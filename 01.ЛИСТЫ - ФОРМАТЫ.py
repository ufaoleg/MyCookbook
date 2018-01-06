import clr
clr.AddReference('ProtoGeometry')
from Autodesk.DesignScript.Geometry import *
#Введенные в этом узле данные сохраняется в виде списка в переменных IN.
clr.AddReference('RevitServices')
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager
clr.AddReference('RevitAPI')
import Autodesk
from Autodesk.Revit.DB import *
from System.Collections.Generic import *
clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.Elements)
import System
doc = DocumentManager.Instance.CurrentDBDocument

uiapp = DocumentManager.Instance.CurrentUIApplication
app = uiapp.Application

sheets = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_Sheets).WhereElementIsNotElementType().ToElements()
title_blocks = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_TitleBlocks).WhereElementIsNotElementType().ToElements()

list_ok, list_error = [], []
text = IN[1]

def is_not_edit(e):
	flag = False
	name = e.LookupParameter("Редактирует").AsString()
	if name == "" or name == app.Username:
		flag = True
	return flag
# j=0

"""
TODO: Реализовать выборку листов и блоков несмотря на отсеивание
private IList<Element> m_alltitleblocks = new List<Element>();
private IList<Element> ElementsOnSheet = new List<Element>();
private FamilySymbol MyTitleBlock;

foreach (Element e in new FilteredElementCollector(doc).OwnedByView(vs.Id))
{
ElementsOnSheet.Add(e);
}

        public void GetAllTitleBlocks(Document doc)
        {
            //get all titleblocks
            FilteredElementCollector collector = new FilteredElementCollector(doc);
            collector.OfClass(typeof(FamilySymbol));
            collector.OfCategory(BuiltInCategory.OST_TitleBlocks);

            m_alltitleblocks = collector.ToElements();
        }

        private void GetTitleSheet(IList<Element> ElementsOnSheet)
        {
            foreach (Element el in ElementsOnSheet)
            {
                foreach (FamilySymbol Fs in m_alltitleblocks)
                {
                    if (el.GetTypeId().IntegerValue == Fs.Id.IntegerValue)
                    {
                        MyTitleBlock = Fs;
                    }
                }
            }
        }

"""

TransactionManager.Instance.EnsureInTransaction(doc)
# for index, title_block in enumerate(title_blocks):
for index, sheet in enumerate(sheets):
	if is_not_edit(sheet):
		razdel = sheet.LookupParameter("Раздел проекта").AsString()
		formt = sheet.LookupParameter("Формат листа").AsString()
		number = sheet.LookupParameter("SH_Номер листа").AsString()
		new_number = sheet.LookupParameter("Номер листа").AsString()[1:]
		if razdel == text:
			sheet.LookupParameter("Формат листа").Set(title_blocks[index].ToDSType(True).ToString())
			sheet.LookupParameter("SH_Номер листа").Set(new_number)
			list_ok.append(sheet)
			# j=j+1
	else:
		list_error.append(sheet)

TransactionManager.Instance.TransactionTaskDone()

OUT = list_ok, list_error

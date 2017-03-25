# Copyright(c) 2017, Oleg Rezvov
# @PRSPKT, http://prspkt.ru
__author__ = "ООО АБ Проспект"

input = IN[0]
name, number = [], []
j = 0
dup, uniq = [], []
room = []


def fname(kek):
    UnwrapElement(kek).LookupParameter("Имя").AsString()


for i in input:
    nm = UnwrapElement(i).LookupParameter("Имя").AsString()
    num = UnwrapElement(i).LookupParameter("Номер").AsString()
    number.append(num)
    name.append(nm)
    room.append(i)
    j = +1
k = 0
for i in name:
    if name.count(i) > 1:
        dup.append(room[k])
    else:
        uniq.append(room[k])
    k += 1

OUT = [dup, uniq]



OUT = [str(round((x-y)/1000, 2) for x,y in zip(IN[1], IN[0]))]

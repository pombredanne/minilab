#!/usr/bin/python
from Histogram import Histogram

his = Histogram(10, 10, 110)
his.add(10)
his.add(19)
his.add(20)
his.add(29)
his.add(30)
his.add(39)
his.add(40)
his.add(49)
his.add(50)
his.add(59)
his.add(60)
his.add(69)
his.add(70)
his.add(79)
his.add(80)
his.add(89)
his.add(90)
his.add(99)
his.add(100)
his.add(109)

print his.bins

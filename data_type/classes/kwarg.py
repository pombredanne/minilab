# -*- coding: utf-8 -*-
from copy import deepcopy as copy

class Field():
    value = None

class Model():
    def __init__(self, **data):
        if 'reflection' in self.__class__.__dict__:
            setattr(self.__class__, 'day', Field())
            
        for item in data:
            if (
                item not in self.__class__.__dict__ and
                item not in self.__dict__
            ): 
                raise AttributeError("A instance has no attribute '%s'" % item)
                
            if item in self.__dict__:
                if not isinstance(self.__dict__[item], Field):
                    continue
                self.__dict__[item].value = data[item]
            else:
                field = copy(self.__class__.__dict__[item])
                field.value = data[item]
                setattr(self, item, field)
        
                
class A1(Model):
    data = Field()

class A2(Model): 
    data = Field()
    reflection = True

          
def main():
    t = A1(data=1)
    t2 = A2(data=1, day=10)
    print(t2.day.value)
    
if __name__ == '__main__':
    main()
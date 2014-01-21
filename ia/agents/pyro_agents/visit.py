# -*- coding: utf-8 -*-

# This is the code that runs this example.
from ia.agents.pyro_agents.warehouse import Warehouse
from ia.agents.pyro_agents.person import Person

warehouse = Warehouse()
janet = Person("Janet")
henry = Person("Henry")
janet.visit(warehouse)
henry.visit(warehouse)
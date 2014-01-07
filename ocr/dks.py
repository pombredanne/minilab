# -*- coding: utf-8 -*-
# busca de modelos de vehículos por la matrícula
from dk_car_scraper import scraper

license_plate = 'AB44887'
print(scraper.get_car_details(license_plate))

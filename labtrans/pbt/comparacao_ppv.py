# -*- coding: utf-8 -*-
"""
Created on Fri Oct 11 14:51:29 2013

Observações entre o arquivo do PPV e o arquivo do WIM (Labview)

No arquivo do PPV considera a pesagem até do grupo de eixos 6
enquanto no arquivo do WIM (Labview) permite a pesagem até o grupo de eixos 7.

Na tabela de classificação existe apenas um caminhão com 7 grupos de eixos, o
caminhão 3D6 (pbt até 80T de 25 a 30 metros).

Por se tratar de um caso isolado deve ter sido excluído da consideração do PPV.

Assim o retorno desse algoritmo tratará até o 6o grupo de eixos.

"""
import sys

sys.path.append('../')
from db.connection import db_connect, db_cursor

from collections import defaultdict
import settings


def acquisition__license_plate(cursor, initial_date, final_date):
    sql = '''
      SELECT
      TO_CHAR(
        static_weigh.datetime, 'YYYY-MM-DD HH24:MI:SS'
      ) as ws_datetime,
      wim_datetime,
      total_weight,
      weight_group_1,
      weight_group_2,
      weight_group_3,
      weight_group_4,
      weight_group_5,
      weight_group_6,
      license_plate,
      ws_class_name
    FROM (
      SELECT
        weigh_station_data.*,
        vehicle.license_plate AS ws_license_plate,
        vehicle_class.name AS ws_class_name
      FROM weigh_station_data
        INNER JOIN vehicle
          ON (weigh_station_data.vehicle = vehicle.id)
        INNER JOIN vehicle_class
          ON (weigh_station_data.vehicle_class=vehicle_class.id)
      ) AS static_weigh
      INNER JOIN (
        SELECT
          TO_CHAR(
            acquisition.date_time, 'YYYY-MM-DD HH24:MI:SS') as wim_datetime,
          acquisition.id,
          license_plate AS license_plate
        FROM acquisition
          INNER JOIN vehicle
            ON (acquisition.vehicle = vehicle.id)
        WHERE
          date_time BETWEEN
            '%s 00:00:00' AND '%s 22:59:59'
          AND license_plate <> ''
        ORDER BY date_time
      ) AS wim
        ON (ws_license_plate = license_plate)
    ''' % (initial_date, final_date)

    cursor.execute(sql, ())

    return cursor.fetchall()


# configura conexao
conn = db_connect(settings)

# consulta adquisición
cursor_acq = db_cursor(conn, settings)

# inicia as consultas
lista_acq = acquisition__license_plate(cursor_acq, '2013-06-26', '2013-06-27')

acq_processada = defaultdict(list)
acq_processada_h = [
    'Linha',  # 0
    'Timestamp',  # 1
    'Validade',  # 2
    'PBT',  # 19
    'Massa Grupo 1',  # 29
    'Massa Grupo 2',  # 30
    'Massa Grupo 3',  # 31
    'Massa Grupo 4',  # 32
    'Massa Grupo 5',  # 33
    'Massa Grupo 6',  # 34
    # 'Massa Grupo 7',  # 35 ## removido
]

acq_pbt = defaultdict(dict)
acq_grupo = defaultdict(dict)

# gera dicionário com os dados necessários
for l in open('data/dadosprocessados.csv').readlines()[1:]:
    TAB_L = l.count('\t')
    P_C_L = l.count(';')

    SEP = '\t' if TAB_L > P_C_L else ';'

    line = l.split(SEP)

    acq_processada[line[1]].append(
        [line[i] for i in [0, 1, 2, 19, 29, 30, 31, 32, 33, 34, 35]]
    )


acq_grupo = defaultdict(dict)

# gera a estrutura dos dados organizados
for acq in lista_acq:
    acq_pbt[acq.ws_datetime] = {
        'wim_datetime': acq.wim_datetime,
        'datetime': acq.ws_datetime,
        'classification': acq.ws_class_name,
        'license_plate': acq.license_plate,
        'ppv': acq.total_weight
    }

    # GRUPO
    # armazena dados por grupo de eixos
    # o peso para todas as linhas vao ser os mesmo
    # pois se trata do peso caculado pelo ppv que será usado como comparativo
    # para todas as linhas da pesagem em movimento
    for i in range(1, 7):
        acq_grupo[i][acq.ws_datetime] = {
            'wim_datetime': acq.wim_datetime,
            'datetime': acq.wim_datetime,
            'ppv': acq.__dict__['weight_group_%s' % i],
            'license_plate': acq.license_plate,
            'classification': acq.ws_class_name
        }

    # PBT por linha e por grupo
    for line in acq_processada[acq.wim_datetime]:
        # PBT LINHA
        acq_pbt[acq.ws_datetime]['l_%s' % line[0]] = line[3]

        # GRUPO
        for i in range(1, 7):
            # i + n -> deslocamento dentro da lista para encontrar o valor
            # correspondente ao grupo
            acq_grupo[i][acq.ws_datetime]['l_%s' % line[0]] = \
                line[i + 3]

# cria arquivo de peso total
SEP = '\t'
f = open('data/pbt.csv', 'w')
text = 'datetime\tclasse\tplaca\tppv\t'
text += '\t'.join(['%s' % l for l in range(1, 18)])
text += '\n'

for i in acq_pbt:
    text += acq_pbt[i]['datetime'] + SEP
    text += acq_pbt[i]['classification'] + SEP
    text += acq_pbt[i]['license_plate'] + SEP
    text += str(acq_pbt[i]['ppv']).replace('.', ',') + SEP

    for l in range(1, 18):
        text += acq_pbt[i]['l_%s' % l] + SEP

    text += '\n'  # final da linha

f.write(text)
f.close()

# cria arquivo de peso por grupo
for i in acq_grupo:
    f = open('data/grupo_%s.csv' % i, 'w')

    text = 'grupo %s\n' % i
    text += 'datetime\tclasse\tplaca\tppv\t'
    text += '\t'.join(['%s' % l for l in range(1, 18)])

    for acq in acq_grupo[i]:
        text += '\n'
        text += acq_grupo[i][acq]['datetime'] + SEP
        text += acq_grupo[i][acq]['classification'] + SEP
        text += acq_grupo[i][acq]['license_plate'] + SEP
        text += str(acq_grupo[i][acq]['ppv']).replace('.', ',') + SEP
        for l in range(1, 18):
            text += acq_grupo[i][acq]['l_%s' % l] + SEP

    f.write(text)
    f.close()
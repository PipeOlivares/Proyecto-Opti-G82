import csv
from data import dias

alimentos = []
volAlimento = {}
qInicialAlimento = {}
costoAlimento = {}
vencimientoPeriodo = {}
qNutrientesAlimentos = {}

# instanciar diccionario
qRescatado = {}
for i in range(0, 15):
    qRescatado[i] = {}


with open("csvs/Datos.csv") as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=",")
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            (
                alimento,
                unidad,
                prote,
                carbo,
                grasa,
                calorias,
                volumen,
                costo,
                i_inicial,
                dias_porvencer,
                cantidad_paq,
                t_1,
                t_2,
                t_3,
                t_4,
                t_5,
                t_6,
                t_7,
                t_8,
                t_9,
                t_10,
                t_11,
                t_12,
                t_13,
                t_14,
            ) = row
            alimento = alimento.strip()
            lista_dias = [
                0,
                t_1,
                t_2,
                t_3,
                t_4,
                t_5,
                t_6,
                t_7,
                t_8,
                t_9,
                t_10,
                t_11,
                t_12,
                t_13,
                t_14,
            ]
            alimentos.append(alimento)
            volAlimento[alimento] = float(volumen)
            qInicialAlimento[alimento] = float(i_inicial)
            costoAlimento[alimento] = float(costo)
            vencimientoPeriodo[alimento] = float(dias_porvencer)

            # qNutrientesAlimentos
            x = {
                "proteinas": float(prote),
                "carbohidratos": float(carbo),
                "grasas": float(grasa),
                "calorias": float(calorias),
            }
            qNutrientesAlimentos[alimento] = x

            # qRescatado
            for dia in dias:
                if dia != 0:
                    qRescatado[dia][alimento] = float(lista_dias[dia])
        line_count += 1


with open("csvs/Datos - cantidad-productos.csv") as productos:
    reader_productos = csv.reader(productos, delimiter=",")
    line = 0
    for r in reader_productos:
        if line != 0:
            (
                min_prod,
                max_prod,
                max_cajas,
                max_prod_caja,
                maxProductosCajaUnitario,
                vol_bodega,
                personas,
                vol_caja,
            ) = r
            minProductos = float(min_prod)
            maxProductos = float(max_prod)
            M_T = float(max_prod_caja)
            M_P = float(maxProductosCajaUnitario)
            maxCajas = float(max_cajas)
            volBodega = float(vol_bodega)
            qPersonas = float(personas)
            volCaja = float(vol_caja)
        line += 1
minNutriente = {}


with open("csvs/Datos - nutricion.csv") as nutri:
    nutr = csv.reader(nutri, delimiter=",")
    line_nutri = 0
    for r_nutri in nutr:
        if line_nutri != 0:
            nutriente, al = r_nutri
            minNutriente[nutriente] = float(al)
        line_nutri += 1

# instanciar diccionario
vencimientoAlimento = {}
for i in range(0, 15):
    vencimientoAlimento[i] = {}


with open("csvs/Datos - C_it.csv") as vencimientos:
    venc = csv.reader(vencimientos, delimiter=",")
    line_ven = 0
    for r_venc in venc:
        if line_ven != 0:
            (
                al,
                _,
                v1,
                v2,
                v3,
                v4,
                v5,
                v6,
                v7,
                v8,
                v9,
                v10,
                v11,
                v12,
                v13,
                v14,
                v15,
                v16,
                _,
                _,
                _,
                _,
                _,
            ) = r_venc
            lista_venc = [
                0,
                v1,
                v2,
                v3,
                v4,
                v5,
                v6,
                v7,
                v8,
                v9,
                v10,
                v11,
                v12,
                v13,
                v14,
            ]
            al = al.strip()
            for dia in dias:
                if dia != 0:
                    vencimientoAlimento[dia][al] = float(lista_venc[dia])

        line_ven += 1

# print(vencimientoAlimento)


qDonaciones = {}
with open("csvs/Datos - Dinero.csv") as dinero:
    din = csv.reader(dinero, delimiter=",")
    line_dinero = 0
    for row_dinero in din:
        if line_dinero != 0:
            (
                _,
                d0,
                d1,
                d2,
                d3,
                d4,
                d5,
                d6,
                d7,
                d8,
                d9,
                d10,
                d11,
                d12,
                d13,
                d14,
                inicial,
            ) = row_dinero
            qInicialDinero = float(inicial)
            lista_dinero = [
                d0,
                d1,
                d2,
                d3,
                d4,
                d5,
                d6,
                d7,
                d8,
                d9,
                d10,
                d11,
                d12,
                d13,
                d14,
            ]
            for dia in dias:
                if dia != 0:
                    qDonaciones[dia] = float(lista_dinero[dia])
        line_dinero += 1

# print(qDonaciones)


qTrabajadores = {}
with open("csvs/Datos - Trabajadores.csv") as trabajador:
    wor = csv.reader(trabajador, delimiter=",")
    wokr = 0
    for row_w in wor:
        if wokr != 0:
            (
                _,
                d1,
                d2,
                d3,
                d4,
                d5,
                d6,
                d7,
                d8,
                d9,
                d10,
                d11,
                d12,
                d13,
                d14,
            ) = row_w
            lista_trabajdores = [
                0,
                d1,
                d2,
                d3,
                d4,
                d5,
                d6,
                d7,
                d8,
                d9,
                d10,
                d11,
                d12,
                d13,
                d14,
            ]
            for dia in dias:
                qTrabajadores[dia] = float(lista_trabajdores[dia])
        wokr += 1

# print(qTrabajadores)

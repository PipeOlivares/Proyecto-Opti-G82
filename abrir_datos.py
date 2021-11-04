import csv
alimentos = []
volAlimento = {}
qInicialAlimento = {}
costoAlimento = {}
vencimientoPeriodo = {}
qNutrientesAlimentos = {}


with open('csvs/Datos - Alimentos.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            alimento , unidad ,prote , carbo, grasa ,calorias , volumen, costo, i_inicial, dias_porvencer = row
            alimento = alimento.strip()
            alimentos.append(alimento)
            volAlimento[alimento]        = float(volumen)
            qInicialAlimento[alimento]   = float(i_inicial)
            costoAlimento[alimento]      = float(costo)
            vencimientoPeriodo[alimento] = float(dias_porvencer) 
            x = {"proteinas": float(prote),"carbohidratos": float(carbo),"grasas": float(grasa), "calorias": float(calorias)}
            qNutrientesAlimentos[alimento] = x

        line_count += 1

# kcal = 0
# for key,value in qNutrientesAlimentos.items():
#     for key2, value2 in qNutrientesAlimentos[key].items():
#         print("{} {} {}".format(key,key2, value2))
#         kcal += qNutrientesAlimentos[key]["calorias"]

print(alimentos)


with open('csvs/Datos - cantidad-productos.csv') as productos:
    reader_productos = csv.reader(productos, delimiter=',')
    line = 0
    for r in reader_productos :
        if line != 0:
            min_prod , max_prod, max_cajas, vol_bodega, personas, vol_caja = r
            minProductos = float(min_prod)
            maxProductos = float(max_prod)
            maxCajas     = float(max_cajas)
            volBodega    = float(vol_bodega)
            qPersonas    = float(personas)
            volCaja      = float(vol_caja)
        line += 1

minNutriente = {}
with open('csvs/Datos - nutricion.csv') as nutri:
    nutr = csv.reader(nutri, delimiter=',')
    line_nutri = 0
    for r_nutri in nutr :
        if line_nutri != 0:
            nutriente, al = r_nutri
            minNutriente[nutriente] = float(al)
        line_nutri += 1

print(minNutriente)
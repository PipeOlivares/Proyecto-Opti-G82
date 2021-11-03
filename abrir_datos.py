import csv
alimentos = []
volAlimento = {}
qInicialAlimento = {}
costoAlimento = {}
vencimientoPeriodo = {}
qNutrientesAlimentos = {}


with open('Datos - Alimentos.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count != 0:
            alimento , unidad ,prote , carbo, grasa ,calorias , volumen, costo, i_inicial, dias_porvencer = row
            alimento = alimento.strip()
            alimentos.append(alimento)
            volAlimento[alimento]       = float(volumen)
            qInicialAlimento[alimento]  = float(i_inicial)
            costoAlimento[alimento]     = float(costo)
            vencimientoPeriodo[alimento]= float(dias_porvencer) 
            x = {"proteinas": float(prote),"carbohidratos": float(carbo),"grasas": float(grasa), "calorias": float(calorias)}
            qNutrientesAlimentos[alimento] = x

        line_count += 1


######################
#### PROYECTO G82 ####
######################
from gurobipy import GRB, Model, quicksum


#### PARAMETROS ####
from abrir_datos import (
    alimentos,
    volAlimento,
    qInicialAlimento,
    costoAlimento,
    vencimientoPeriodo,
    qNutrientesAlimentos,
)

from data import (
    alimentos,
    dias,
    cajas,
    nutrientes,
    qNutrientesAlimentos,
    volCaja,
    minNutriente,
    qPersonas,
    minProductos,
    maxProductos,
    vencimientoAlimento,
    volAlimento,
    qRescatado,
    qInicialAlimento,
    qDonaciones,
    qInicialDinero,
    costoAlimento,
    volBodega,
    maxCajas,
    crearCajaDia,
    tarifa,
    distanciaCaja,
    cDistancia,
)


#### MODELO ####
model = Model("Produccion de Cajas")


#### VARIABLES ####
qAlimentoCaja = model.addVars(alimentos, cajas, dias, vtype=GRB.INTEGER, name="X_ijt")
bAlimentoCaja = model.addVars(alimentos, cajas, vtype=GRB.BINARY, name="I_ij")
bCaja = model.addVars(cajas, dias, vtype=GRB.BINARY, name="Y_jt")
qAlmacenado = model.addVars(alimentos, dias, vtype=GRB.INTEGER, name="B_it")
qAlimentoComprar = model.addVars(cajas, dias, vtype=GRB.INTEGER, name="F_it")

#tiene un error, le fata una variable? porque dice que no pueden ser listas
qPresupuesto = model.addVar(dias, vtype=GRB.INTEGER, name="Z_t")
 
model.update()


#### FUNCION OBJETIVO ####
objective = quicksum(quicksum(bCaja for caja in cajas) for dia in dias)


#######################
#### RESTRICCIONES ####
#######################

## R1 ## Inventario (flujo)
model.addConstrs(
    (
        qAlmacenado[alimento][dia]
        == qAlmacenado[alimento][dia - 1]
        + qRescatado[alimento][dia]
        + qAlimentoComprar[alimento][dia]
        - quicksum(qAlimentoCaja for caja in cajas)
        for alimento in alimentos
        for dia in dias[1:]
    ),
    name="Inventario (flujo)",
)

## R2 ## Inventario inicial
model.addConstrs(
    (qAlmacenado[alimento][0] == qInicialAlimento[alimento] for alimento in alimentos)
)

## R3 ## Almacenamiento Maximo (tamaño bodega)
model.addConstrs(
    (
        volBodega
        >= quicksum(
            qAlmacenado[alimento][dia] * volAlimento[alimento] for alimento in alimentos
        )
        + quicksum(bCaja[caja][dia] * volCaja for caja in cajas)
        for dia in dias
    ),
    name="Almacenamiento maximo",
)

## R4 ## Capacidad de producción
## Kt >= sum de j (Y j,t)
model.addConstrs(
    (maxCajas >= quicksum(crearCajaDia[dia][caja] for caja in cajas) for dia in dias),
    name="Capacidad de producción",
)

## R5 ## Presupuesto dinero
model.addConstrs(
    (
        qPresupuesto[dia]
        == qPresupuesto[dia - 1]
        + qDonaciones[dia]
        - tarifa * ParametroNoDefinido  #### definir parametro 1 cuando es multiplo de 7, 0 cuando no.
        - quicksum(
            qAlimentoComprar[alimento][dia] * costoAlimento[alimento]
            for alimento in alimentos
        )
        for dia in dias[1:]
    ),
    name="Presupuesto dinero",
)

## R6 ## Dinero inicial en t = 0
model.addConstrs((qPresupuesto[0] == qInicialDinero), name="Presupuesto inicial")

## R7 ## Valor nutricional de los alimentos
#  Revisar
model.addConstrs(
    (
        (
            (
                (
                    (
                        quicksum(qAlimentoCaja[alimento][caja][dia])
                        * qNutrientesAlimentos[alimento][nutriente]
                    )
                    >= minNutriente[nutriente] * qPersonas
                    for alimento in alimentos
                )
                for nutriente in nutrientes
            )
            for caja in cajas
        )
        for dia in dias
    ),
    name="Valor nutricional de los alimentos",
)


## R8 ## Cantidad de alimentos en una caja (variabilidad) , no unitario
model.addConstrs(
    (
        (
            (quicksum(bAlimentoCaja[alimento][caja]) >= minProductos)
            for alimento in alimentos
        )
        for caja in cajas
    ),
    name="Cantidad de alimentos en una caja 1",
)

model.addConstrs(
    (
        (
            (quicksum(bAlimentoCaja[alimento][caja]) <= maxProductos)
            for alimento in alimentos
        )
        for caja in cajas
    ),
    name="Cantidad de alimentos en una caja 2",
)

## R9 ## Vencimiento de los alimentos
##Enit   Ii, j      
model.addConstrs(
    (
        vencimientoAlimento[dia][alimento] >= bAlimentoCaja[alimento][caja]
        for alimento in alimentos
        for caja in cajas
        for dia in dias
    ),
    name="Vencimiento alimentos",
)


## R10 ##  Capacidad de la caja
## Revisar
model.addConstrs(
    (
        (
            (
                volCaja
                >= quicksum(
                    qAlimentoCaja[alimento][caja][dia] * volAlimento[alimento]
                    for alimento in alimentos
                )
            )
            for caja in cajas
        )
        for dia in dias
    ),
    name=" Capacidad de la caja ",
)

## R11 ## Una caja se genera cuando se le entregan alimentos
##
model.addConstrs(
    (
        quicksum(qAlimentoCaja[alimento][caja][dia] for alimento in alimentos)
        <= bCaja[caja][dia] * float("inf")  ## BigM lo deje como máximo
        for caja in cajas
        for dia in dias
    ),
    name="se genera caja cuando se le dan alimentos -- 1",
)

model.addConstrs(
    (
        quicksum(qAlimentoCaja[alimento][caja][dia] for alimento in alimentos)
        >= bCaja[caja][dia]
        for caja in cajas
        for dia in dias
    ),
    name="se genera caja cuando se le dan alimentos -- 2",
)

## R12 ## Relacion de variable I_ij con X_ijt
model.addConstrs(
    (
        bAlimentoCaja[alimento][caja] * float("inf")
        >= qAlimentoCaja[alimento][caja][dia]
        for alimento in alimentos
        for caja in cajas
        for dia in dias
    ),
    name="Relacion con multiplicador de I_ij con X_ijt",
)
model.addConstrs(
    (
        qAlimentoCaja[alimento][caja][dia] >= bAlimentoCaja[alimento][caja]
        for alimento in alimentos
        for caja in cajas
        for dia in dias
    ),
    name="Relacion sin multiplicador de I_ij con X_ijt",
)

# N1 ## Naturaleza X_ijt
model.addConstrs(
    (
        qAlimentoCaja[alimento][caja][dia] >= 0
        for alimento in alimentos
        for caja in cajas
        for dia in dias
    ),
    name="Naturaleza X_ijt",
)

## N2 ## Naturaleza I_ij
## COMO ES BINARIA, NO NECESITA RESTRICCION DE NATURALEZA

## N3 ## Naturaleza Y_jt
## COMO ES BINARIA< NO NECESITA NATURALEZA


## N4 ## Naturaleza B_it
model.addConstrs(
    (qAlmacenado[alimento][dia] >= 0 for alimento in alimentos for dia in dias),
    name="Naturaleza B_it",
)

## N5 ## Naturaleza F_it
model.addConstrs(
    (qAlimentoComprar[alimento][dia] >= 0 for alimento in alimentos for dia in dias),
    name="Naturaleza X_ijt",
)

## N6 ## Naturaleza Z_t
model.addConstrs(
    (qPresupuesto[dia] >= 0 for dia in dias),
    name="Naturaleza Z_t",
)


#### RESULTADO ####
model.printAttr("SOLUCION")
print("\n -------------------- \n")


#### HOLGURAS ####
for constr in model.getConstrs():
    print(constr, constr.getAttr("slack"))

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
    qRescatado,
    minProductos,
    maxProductos,
    maxProductosCaja,
    maxCajas,
    volBodega,
    qPersonas,
    volCaja,
    minNutriente,
    vencimientoAlimento,
    qDonaciones,
    qInicialDinero,
)

from data import (
    # alimentos,
    dias,
    cajas,
    nutrientes,
    # qNutrientesAlimentos,
    # volCaja,
    # minNutriente,
    # qPersonas,
    # minProductos,
    # maxProductos,
    # vencimientoAlimento,
    # volAlimento,
    # qRescatado,
    # qInicialAlimento,
    # qDonaciones,
    # qInicialDinero,
    # costoAlimento,
    # volBodega,
    # maxCajas,
    # crearCajaDia,
    tarifa,
    # distanciaCaja,
    # cDistancia,
)


#### MODELO ####
model = Model("Produccion de Cajas")


#### VARIABLES ####
qAlimentoCaja = model.addVars(alimentos, cajas, dias, vtype=GRB.INTEGER, name="X_ijt")
bAlimentoCaja = model.addVars(alimentos, cajas, vtype=GRB.BINARY, name="I_ij")
bCaja = model.addVars(cajas, dias, vtype=GRB.BINARY, name="Y_jt")
qAlmacenado = model.addVars(alimentos, dias, vtype=GRB.INTEGER, name="B_it")
qAlimentoComprar = model.addVars(alimentos, dias, vtype=GRB.INTEGER, name="F_it")
qPresupuesto = model.addVars(dias, vtype=GRB.INTEGER, name="Z_t")

model.update()


#######################
#### RESTRICCIONES ####
#######################

## R1 ## Inventario inicial
model.addConstrs(
    (qAlmacenado[alimento, 0] == qInicialAlimento[alimento] for alimento in alimentos),
    name="Inventario inicial",
)

## R2 ## Inventario (flujo)
model.addConstrs(
    (
        qAlmacenado[alimento, dia]
        == qAlmacenado[alimento, dia - 1]
        + qAlimentoComprar[alimento, dia]
        + qRescatado[dia][alimento]
        - quicksum(qAlimentoCaja[alimento, caja, dia] for caja in cajas)
        for alimento in alimentos
        for dia in dias[1:]
    ),
    name="Inventario (flujo)",
)

## R2 ## Inventario inicial
model.addConstrs(
    (qAlmacenado[alimento, 0] == qInicialAlimento[alimento] for alimento in alimentos)
)

## R3 ## Almacenamiento Maximo (tamaño bodega)
model.addConstrs(
(
volBodega
>= quicksum(
qAlmacenado[alimento, dia] * volAlimento[alimento] for alimento in alimentos
)
+ quicksum(bCaja[caja, dia] * volCaja for caja in cajas)
for dia in dias
),
name="Almacenamiento maximo",
)

# R4 ## Capacidad de producción
## Kt >= sum de j (Y j,t)
model.addConstrs(
    (maxCajas >= quicksum(bCaja[caja, dia] for caja in cajas) for dia in dias),
    name="Capacidad de producción",
)

## R5 ## Presupuesto dinero
model.addConstrs(
    (
        qPresupuesto[dia]
        == qPresupuesto[dia - 1]
        + qDonaciones[dia]
        - tarifa
        - quicksum(
            qAlimentoComprar[alimento, dia] * costoAlimento[alimento]
            for alimento in alimentos
        )
        for dia in dias[1:]
    ),
    name="Presupuesto dinero",
)

## R6 ## Dinero inicial en t = 0
model.addConstrs(
    (qPresupuesto[dia] == qInicialDinero for dia in dias if dia == 0),
    name="Presupuesto inicial",
)
## R7 ## Valor nutricional de los alimentos
#  Revisar
model.addConstrs(
    (
        quicksum(
            qAlimentoCaja[alimento, caja, dia]
            * qNutrientesAlimentos[alimento][nutriente]
            for alimento in alimentos
        )
        >= minNutriente[nutriente]
        for nutriente in nutrientes
        for caja in cajas
        for dia in dias
    ),
    name="Valor nutricional de los alimentos",
)
## R8 ## Cantidad de alimentos en una caja (variabilidad) , no unitario
model.addConstrs(
    (
        (
            quicksum(bAlimentoCaja[alimento, caja] for alimento in alimentos)
            >= minProductos
        )
        for caja in cajas
    ),
    name="Cantidad de alimentos en una caja 1",
)

model.addConstrs(
    (
        quicksum(bAlimentoCaja[alimento, caja] for alimento in alimentos)
        <= maxProductos
        for caja in cajas
    ),
    name="Cantidad de alimentos en una caja 2",
)

## R16 ## Vencimiento de los alimentos
model.addConstrs(
    (
        quicksum(qAlimentoCaja[alimento, caja, dia] for alimento in alimentos)
        <= maxProductosCaja
        for caja in cajas
        for dia in dias
    ),
    name="Maxima cantidad de unidades por caja",
)

## R9 ## Vencimiento de los alimentos
##Enit   Ii, j
model.addConstrs(
    (
        vencimientoAlimento[dia][alimento] >= bAlimentoCaja[alimento, caja]
        for alimento in alimentos
        for caja in cajas
        for dia in dias[1:]
    ),
    name="Vencimiento alimentos",
)

## R10 ## Priorizar los alimentos por vencer
# model.addConstrs(
#     (
#         vencimientoAlimento[dia][alimento] - vencimientoAlimento[dia + 1][alimento]
#         <= qAlimentoCaja[alimento, caja, dia] + qAlimentoCaja[alimento, caja, dia+1]
#         for alimento in alimentos
#         for caja in cajas
#         for dia in dias[1:-1]
#     ),
#     name="Priorizar alimentos por vencer",
# )


## R11 ##  Capacidad de la caja
## Revisar
model.addConstrs(
    (
        volCaja
        >= quicksum(
            qAlimentoCaja[alimento, caja, dia] * volAlimento[alimento]
            for alimento in alimentos
        )
        for caja in cajas
        for dia in dias
    ),
    name=" Capacidad de la caja ",
)

## R12 ## Una caja se genera cuando se le entregan alimentos
##
model.addConstrs(
    (
        quicksum(qAlimentoCaja[alimento, caja, dia] for alimento in alimentos)
        <= bCaja[caja, dia] * 1000000000  ## BigM lo deje como máximo
        for caja in cajas
        for dia in dias
    ),
    name="se genera caja cuando se le dan alimentos -- 1",
)
model.addConstrs(
    (
        quicksum(qAlimentoCaja[alimento, caja, dia] for alimento in alimentos)
        >= bCaja[caja, dia]
        for caja in cajas
        for dia in dias
    ),
    name="se genera caja cuando se le dan alimentos -- 2",
)

# ## R13 ## Relacion de variable I_ij con X_ijt
# model.addConstrs(
#     (
#         bAlimentoCaja[alimento, caja] * 1000000000 >= qAlimentoCaja[alimento, caja, dia]
#         for alimento in alimentos
#         for caja in cajas
#         for dia in dias
#     ),
#     name="Relacion con multiplicador de I_ij con X_ijt",
# )
# model.addConstrs(
#     (
#         qAlimentoCaja[alimento, caja, dia] >= bAlimentoCaja[alimento, caja]
#         for alimento in alimentos
#         for caja in cajas
#         for dia in dias
#     ),
#     name="Relacion sin multiplicador de I_ij con X_ijt",
# )

## R18 ## Cajas armadas en un mismo dia seran iguales
model.addConstrs(
    (
        qAlimentoCaja[alimento, caja, dia] == qAlimentoCaja[alimento, caja + 1, dia]
        for alimento in alimentos
        for caja in cajas[:-1]
        for dia in dias
    ),
    name="Cajas iguales en el mismo dia",
)

# N1 ## Naturaleza X_ijt
model.addConstrs(
    (
        qAlimentoCaja[alimento, caja, dia] >= 0
        for alimento in alimentos
        for caja in cajas
        for dia in dias
    ),
    name="Naturaleza X_ijt",
)

## N2 ## Naturaleza I_ij
## COMO ES BINARIA, NO NECESITA RESTRICCION DE NATURALEZA

## N3 ## Naturaleza Y_jt
## COMO ES BINARIA, NO NECESITA NATURALEZA


## N4 ## Naturaleza B_it
model.addConstrs(
    (qAlmacenado[alimento, dia] >= 0 for alimento in alimentos for dia in dias),
    name="Naturaleza B_it",
)

## N5 ## Naturaleza F_it
model.addConstrs(
    (qAlimentoComprar[alimento, dia] >= 0 for alimento in alimentos for dia in dias),
    name="Naturaleza F_it",
)

## N6 ## Naturaleza Z_t
model.addConstrs(
    (qPresupuesto[dia] >= 0 for dia in dias),
    name="Naturaleza Z_t",
)


##########################
#### FUNCION OBJETIVO ####
##########################

objective = quicksum(bCaja[caja, dia] for caja in cajas for dia in dias)
model.setObjective(objective, GRB.MAXIMIZE)

model.optimize()


#### RESULTADO ####
model.printAttr("X")
# print("\n -------------------- \n")

# # # #### HOLGURAS ####
# for constr in model.getConstrs():
#     print(constr, constr.getAttr("slack"))
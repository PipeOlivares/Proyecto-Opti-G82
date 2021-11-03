######################
#### PROYECTO G82 ####
######################
from gurobipy import GRB, Model, quicksum


#### PARAMETROS ####
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
    vencimiento,
    volAlimento,
    qRescatado,
    qInicialAlimento,
    qDonaciones,
    qInicialDinero,
    costoAlimento,
    vencimientoPeriodo,
    volBodega,
    maxCajas,
)


#### MODELO ####
model = Model("Produccion de Cajas")


#### VARIABLES ####
qAlimentoCaja = model.addVars(alimentos, cajas, dias, vtype=GRB.INTEGER, name="X_ijt")
bAlimentoCaja = model.addVars(alimentos, cajas, vtype=GRB.BINARY, name="I_ij")
bCaja = model.addVars(cajas, dias, vtype=GRB.BINARY, name="Y_jt")
qAlimentoComprar = model.addVars(cajas, dias, vtype=GRB.INTEGER, name="F_it")
qPresupuesto = model.addVar(dias, vtype=GRB.INTEGER, name="Z_t")

model.update()


#### FUNCION OBJETIVO ####
objective = quicksum(quicksum(bCaja for caja in cajas) for dia in dias)


#######################
#### RESTRICCIONES ####
#######################

## N1 ## Naturaleza X_ijt


#### RESULTADO ####
model.printAttr("SOLUCION")
print("\n -------------------- \n")


#### HOLGURAS ####
for constr in model.getConstrs():
    print(constr, constr.getAttr("slack"))

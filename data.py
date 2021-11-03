##############
#### DATA ####
##############
from abrir_datos import (
    alimentos,
    volAlimento,
    qInicialAlimento,
    costoAlimento,
    vencimientoPeriodo,
    qNutrientesAlimentos,
)

# qNutrientesAlimentos, volCaja, minNutriente, qPersonas, minProductos, maxProductos,
# vencimiento, volAlimento, qRescatado, qInicialAlimento, qDonaciones, qInicialDinero,
# costoAlimento, vencimientoPeriodo, volBodega, maxCajas

#### CONJUNTOS ####

print(alimentos)

dias = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]

## considerar parametro K_t para el numero de cajas posibles en un dia
cajas = [1, 2, 3, 4, 5, "etc"]

## caso de nutrientes que no esten en un alimentos sera 0
nutrientes = ["proteinas", "carbohidratos", "grasas", "calorias"]

####################
#### PARAMETROS ####
####################

## U_ik ## Valor nutricional del alimento i con respecto al nutriente k
print(qNutrientesAlimentos)

## M ## Volumen caja
volCaja = int(0)

## N_k ## Cantidad minima nutriente k en caja por persona
minNutriente = {
    nutrientes[0]: 100,
    nutrientes[1]: 13223,
    nutrientes[2]: 245,
    nutrientes[3]: "ETC",
}

## P_n ## Cantidad de personas destinadas en una caja
qPersonas = int(0)  # 4

## H ## Minimo de productos distintos por caja
minProductos = int(0)

## S ## Maximo de productos distintos por caja
maxProductos = int(0)

## C_i ## Maximo de dias que alimento i puede ser enviado en caja
## Dias hasta que la caja va a ser enviada??
vencimiento = int(0)  #### NOT SURE WHAT IT IS ####

## A_i ## Volumen de alimento i
volAlimento = {alimentos[0]: int(10), alimentos[1]: int(39), alimentos[2]: "ETC"}

## R_it ## Cantidad de alimento i rescatado en dia t
qRescatado = {
    dias[0]: {alimentos[0]: int(10), alimentos[1]: int(39), alimentos[2]: "ETC"},
    dias[1]: {alimentos[0]: int(10), alimentos[1]: int(39), alimentos[2]: "ETC"},
    dias[2]: {"ETC"},
}

## R_i0 ## Inventario inicial alimento i
qInicialAlimento = {alimentos[0]: int(10)}

## G_t ## Cantidad de dinero guardado en dia t
qDinero = {dias[0]: int(0)}

## D_t ## Cantidad dinero donado en dia t
qDonaciones = {dias[0]: int(0)}  # int del dinero

## L_0 ## Cantidad dinero inicial
qInicialDinero = int(0)

## W_i ## Costo comprar alimento i
costoAlimento = {alimentos[0]: "costo"}  # valor

## V_it ## Dias desde el periodo t hasta que venza alimento i
vencimientoPeriodo = {alimentos[0]: int(10), alimentos[1]: int(39), alimentos[2]: "ETC"}

## J ## Volumen util de bodega
volBodega = int(5)  # valor

## K_t ## Maxima cantidad de cajas generadas por trabajadores en un dia
maxCajas = int(10)

## ?? ## NOSE SI ES EXACTAMENTE UN PARAMETRO, pero es el orden de importacion
crearCajaDia = {
    dias[0]: {cajas[0]: 1, cajas[1]: 1, cajas[2]: 0, cajas[3]: 0, cajas[4]: "ETC"},
    dias[1]: {cajas[0]: 0, cajas[1]: 0, cajas[2]: 1, cajas[3]: 0, cajas[4]: "ETC"},
}

## T ## Tarifa inicial segun numero de repartidores
tarifa = int(12)

## Km_j ## Distancia (km) que recorre caja j antes de llegar a su destino
distanciaCaja = {cajas[0]: int(2), cajas[1]: int(5), cajas[2]: "ETC"}

## Q ## Costo por kilometro recorrido
cDistancia = int(5)

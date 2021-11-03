##############
#### DATA ####
##############

# qNutrientesAlimentos, volCaja, minNutriente, qPersonas, minProductos, maxProductos,
# vencimiento, volAlimento, qRescatado, qInicialAlimento, qDonaciones, qInicialDinero,
# costoAlimento, vencimientoPeriodo, volBodega, maxCajas

#### CONJUNTOS ####

alimentos = {}

dias = {}

cajas = {}

nutrientes = {}

####################
#### PARAMETROS ####
####################

## U_ik ## Valor nutricional del alimento i con respecto al nutriente k
qNutrientesAlimentos = {}

## M ## Volumen caja
volCaja = {}

## N_k ## Cantidad minima nutriente k en caja por persona
minNutriente = {}

## P_n ## Cantidad de personas destinadas en una caja
qPersonas = {}

## H ## Minimo de productos distintos por caja
minProductos = {}

## S ## Maximo de productos distintos por caja
maxProductos = {}

## C_i ## Maximo de dias que alimento i puede ser enviado en caja
vencimiento = {}

## A_i ## Volumen de alimento i
volAlimento = {}

## R_it ## Cantidad de alimento i rescatado en dia t
qRescatado = {}

## R_i0 ## Inventario inicial alimento i
qInicialAlimento = {}

## G_t ## Cantidad de dinero guardado en dia t
qDinero = {}

## D_t ## Cantidad dinero donado en dia t
qDonaciones = {}

## L_0 ## Cantidad dinero inicial
qInicialDinero = {}

## W_i ## Costo comprar alimento i
costoAlimento = {}

## V_it ## Dias desde el periodo t hasta que venza alimento
vencimientoPeriodo = {}

## J ## Volumen util de bodega
volBodega = {}

## K_t ## Maxima cantidad de cajas generadas por trabajadores en un dia
maxCajas = {}

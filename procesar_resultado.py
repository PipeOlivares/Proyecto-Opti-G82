from gurobipy import GRB, Model, quicksum
X_ijt = []
dias = [i for i in range(15)]
I_ij = []
Y_jt = []
B_it = []
F_it = []
Z_t = []

## ojo que hay periodos vacios

file = open("results.csv", "r")
for line in file:
    if "X_ijt" in line: 
        var , valor = line.strip().split("=+=")
        var = var[6:-1]
        producto,caja,periodo = var.strip().split(",")
        if len(periodo) == 0:
            periodo = ""
        else :
            periodo = int(periodo)
        X_ijt.append((producto,int(caja),periodo,float(valor)))

    elif "I_ij" in line:
        var , valor = line.strip().split("=+=")
        var = var[5:-1]
        producto,caja = var.strip().split(",")
        if len(caja) == 0:
                    caja = ""
        else :
            caja = int(caja)
        I_ij.append((producto, caja ,float(valor)))

    elif "Y_jt" in line:
        var , valor = line.strip().split("=+=")
        var = var[5:-1]
        caja,periodo = var.strip().split(",")
        if len(caja) == 0:
                    caja = ""
        else :
            caja = int(caja)
        Y_jt.append((caja, periodo ,float(valor)))

    elif "B_it" in line:
        var , valor = line.strip().split("=+=")
        var = var[5:-1]
        producto, periodo = var.strip().split(",")
        if len(periodo) == 0:
            periodo = ""
        else :
            periodo = int(periodo)
        B_it.append((producto, periodo ,float(valor)))

    elif "F_it" in line:
        var , valor = line.strip().split("=+=")
        var = var[5:-1]
        producto, periodo = var.strip().split(",")
        if len(periodo) == 0:
            periodo = ""
        else :
            periodo = int(periodo)
        F_it.append((producto, periodo ,float(valor)))
    
    
    #presupuesto
    elif "Z_t" in line:
        var , valor = line.strip().split("=+=")
        var = var[4:-1]
        var = int(var)
        Z_t.append((var ,float(valor)))

cajas_prod_dia = {}
#print(X_ijt)
for i in range(15):
    general = []
    for caja in range(56):
        cajass = []
        productos = []
        productos.append(f"caja {caja}")
        for producto in X_ijt:
            if producto[2] == i and producto[1] == caja and producto[3]!= 0.0:
                #print(producto)
                par = [producto[0], producto[3]]
                productos.append(par)
        #     if "caja" in item:
        #         print("si")
        #     else: 
        #         print("no")
        #         print(item)
            #if len(productos[item]) == 1:
        general.append(productos)
    cajas_prod_dia[i] = general


#todos los dias, todas las cajas
# for key,value in cajas_prod_dia.items():
#     print (f"---------------- DIA {key}-----------------")
#     if key != 0:
#         for item in value:
#             print (f"\n--------{item[0]}----------------")
#             print ("{:<20} {:<21} ".format("PRODUCTOS","CANTIDAD"))
#             for i in range(1,len(item)):
#                 print(f"producto: {item[i][0]}, cantidad: {item[i][1]}")
#                 print ("{:<20} {:<21} ".format(item[i][0],item[i][1]))

## mostrar cajas por dia
# f = 0
# while f==0:
#     diias = input("ingrese el dia a revisar (0-14): ")
#     try: 
#         diias = int(diias)
#         if   not (int(diias) in dias):
#             print("haga un input correcto")
#             pass
#         else: 
#             if int(diias) in dias:
#                 f = 1
#                 print (f"---------------- DIA {diias}-----------------")
#                 for item in cajas_prod_dia[int(diias)]:
#                     if len(item)>1:
#                         print("-----------------------------")
#                         print ("\n{:>17}".format(item[0]))
#                         print ("{:<20} {:<21} ".format("PRODUCTO","CANTIDAD"))
#                         for prod in item: 
#                             if prod != item[0]:   
#                                 print ("{:<25} {:<26} ".format(prod[0],prod[1]))
#     except ValueError:
#         print("Intenta de nuevo")


## presupuesto
# print ("\n{:>20} \n".format("PRESUPUESTO"))
# for i in range(len(Z_t)):
#     print ("DIA: {:<10} PRESUPUESTO: {:<12} ".format(Z_t[i][0],Z_t[i][1]))


# Bodegas
Qalimento = {}
for producto_bodega in B_it:
    if producto_bodega[0] not in Qalimento.keys():
        Qalimento[producto_bodega[0]] = []
        par = [producto_bodega[1],abs(producto_bodega[2])]
        Qalimento[producto_bodega[0]].append(par)
    else:
        par = [producto_bodega[1],abs(producto_bodega[2])]
        Qalimento[producto_bodega[0]].append(par)


#mostrar inventario por dias
# days = ""
# print ("\n{:>20} \n".format("INVENTARIO PRODUCTOS"))
# valores_dias = [f"dia {i}" for i in range(15)]
# for day in valores_dias:
#     days += "{:<8}".format(day)
# print("{:<20} {:<11}".format("PRODUCTO",days))
# filas = []
# for key,value in Qalimento.items():
#     fila_v = ""
#     for vals in value:
#         fila_v += "{:<8}".format(str(int(vals[1])))
#     filaa = "{:<20} {:<11}".format(key,fila_v)
#     print (filaa)

Qalimento_comprar = {}
for producto_comprar in F_it:
    if producto_comprar[0] not in Qalimento_comprar.keys():
        Qalimento_comprar[producto_comprar[0]] = []
        par = [producto_comprar[1],abs(producto_comprar[2])]
        Qalimento_comprar[producto_comprar[0]].append(par)
    else:
        par = [producto_comprar[1],abs(producto_comprar[2])]
        Qalimento_comprar[producto_comprar[0]].append(par)


Qalimentos_usados = {}
for alimentos_usado in X_ijt:
    if alimentos_usado[0] not in Qalimentos_usados.keys():
        Qalimentos_usados[alimentos_usado[0]] = [0 for i  in range(15)]
        # print(Qalimentos_usados[alimentos_usado[0]][alimentos_usado[2]])
        Qalimentos_usados[alimentos_usado[0]][alimentos_usado[2]] += int(alimentos_usado[3])
    else:
        Qalimentos_usados[alimentos_usado[0]][alimentos_usado[2]] += alimentos_usado[3]

# dias_c = ""
# print ("\n{:>20} \n".format("INVENTARIO PRODUCTOS"))
# valores_dias = [f"dia {i}" for i in range(15)]
# for day in valores_dias:
#     dias_c += "{:<8}".format(day)
# print("{:<20} {:<11}".format("PRODUCTO",dias_c))
# filas = []
# for key,value in Qalimento_comprar.items():
#     fila_v = ""
#     for vals in value:
#         fila_v += "{:<8}".format(str(int(vals[1])))
#     filaa = "{:<20} {:<11}".format(key,fila_v)
#     print (filaa)


def menus_principal():
    f = 0
    while f == 0:
        print("\n MENU")
        print("1 - Ver todas las cajas por dia")
        print("2 - Ver cajas en dia especifico")
        print("3 - Ver presupuestos por dia")
        print("4 - Ver inventario de productos por dia")
        print("5 - Ver alimentos comprados")
        print("6 - Ver alimentos usados por dia")
        print("7 - Salir")
        oopcion = input("Selecciones una opcion: ")
        try:
            oopcion = int(oopcion)
            if oopcion == 1:
                cantidadmax = 0
                cantidadmin = 1000
                prod__por_caja = []
                sumas = []
                for key,value in cajas_prod_dia.items():
                    print (f"---------------- DIA {key}-----------------")
                    if key != 0:
                        for item in value:
                            if len(item) > 1:
                                sum_caja = 0
                                cont_caja = 0
                                print (f"\n--------{item[0]}----------------")
                                print ("{:<20} {:<21} ".format("PRODUCTOS","CANTIDAD"))
                                for i in range(1,len(item)):
                                    print ("{:<20} {:<21} ".format(item[i][0],item[i][1]))
                                    sum_caja += int(item[i][1])
                                    cont_caja +=1
                                prod__por_caja.append(cont_caja)
                                max_produ = max(prod__por_caja)
                                min_produ = min(prod__por_caja)
                                avg_prod = sum(prod__por_caja)/len(prod__por_caja)
                                sumas.append(sum_caja)
                                cantidadmax = max(sumas)
                                cantidadmin = min(sumas)
                                prom = sum(sumas)/len(sumas)
                print(f"maximo : {max_produ}  minimo : {min_produ} promedio: {avg_prod}")
                print(f"la caja con mas productos tiene: {cantidadmax} y la con minimo tiene: {cantidadmin} y el promedio es {prom}")
            elif oopcion == 2:
                g = 0
                while g == 0:
                    diias = input("ingrese el dia a revisar (0-14): ")
                    sumas = []
                    prod__por_caja = []
                    try: 
                        diias = int(diias)
                        if   not (int(diias) in dias):
                            print("haga un input correcto")
                            pass
                        else: 
                            if int(diias) in dias:
                                g = 1
                                print (f"---------------- DIA {diias}-----------------")
                                for item in cajas_prod_dia[int(diias)]:
                                    if len(item)>1:
                                        sum_caja = 0
                                        cont_caja =0
                                        print("-----------------------------")
                                        print ("\n{:>17}".format(item[0]))
                                        print ("{:<20} {:<21} ".format("PRODUCTO","CANTIDAD"))
                                        for prod in item: 
                                            if prod != item[0]:   
                                                print ("{:<25} {:<26} ".format(prod[0],prod[1]))
                                                sum_caja += int(prod[1])
                                                cont_caja +=1
                                        prod__por_caja.append(cont_caja)
                                        max_produ = max(prod__por_caja)
                                        min_produ = min(prod__por_caja)
                                        avg_prod = sum(prod__por_caja)/len(prod__por_caja)
                                        sumas.append(sum_caja)
                                        cantidadmax = max(sumas)
                                        cantidadmin = min(sumas)
                                        prom = sum(sumas)/len(sumas)
                        print(f"maximo : {max_produ}  minimo : {min_produ} promedio: {avg_prod}")
                        print(f"la caja con mas productos tiene: {cantidadmax} y la con minimo tiene: {cantidadmin} y el promedio es {prom}")


                    except ValueError:
                        print("Intenta de nuevo")

            elif oopcion == 3:
                print ("\n{:>20} \n".format("PRESUPUESTO"))
                for i in range(len(Z_t)):
                    print ("DIA: {:<10} PRESUPUESTO: {:<12} ".format(Z_t[i][0],int(Z_t[i][1])))


            elif oopcion == 4:
                days = ""
                print ("\n{:>20} \n".format("INVENTARIO PRODUCTOS"))
                valores_dias = [f"dia {i}" for i in range(15)]
                for day in valores_dias:
                    days += "{:<8}".format(day)
                print("{:<20} {:<11}".format("PRODUCTO",days))
                filas = []
                for key,value in Qalimento.items():
                    fila_v = ""
                    for vals in value:
                        fila_v += "{:<8}".format(str(int(vals[1])))
                    filaa = "{:<20} {:<11}".format(key,fila_v)
                    print (filaa)
            
            elif oopcion == 5:
                dias_c = ""
                print ("\n{:>20} \n".format("INVENTARIO PRODUCTOS"))
                valores_dias = [f"dia {i}" for i in range(15)]
                for day in valores_dias:
                    dias_c += "{:<8}".format(day)
                print("{:<20} {:<11}".format("PRODUCTO",dias_c))
                filas = []
                for key,value in Qalimento_comprar.items():
                    fila_v = ""
                    for vals in value:
                        fila_v += "{:<8}".format(str(int(vals[1])))
                    filaa = "{:<20} {:<11}".format(key,fila_v)
                    print (filaa)

            elif oopcion == 6:
                days = ""
                print ("\n{:>20} \n".format("PRODUCTOS USADOS POR DIA"))
                valores_dias = [f"dia {i}" for i in range(15)]
                for day in valores_dias:
                    days += "{:<8}".format(day)
                print("{:<20} {:<11}".format("PRODUCTO",days))
                filas = []
                for key,value in Qalimentos_usados.items():
                    fila_v = ""
                    for vals in value:
                        fila_v += "{:<8}".format(str(int(vals)))
                    filaa = "{:<20} {:<11}".format(key,fila_v)
                    print (filaa)




            elif oopcion == 7:
                f = 1

        except ValueError : 
            print("Intenta de nuevo")
# menus_principal()
# print(F_it)


# print (Z_t)
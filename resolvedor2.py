
# Lo deje global para poder acceder a esta informacion en todo el modulo
# def lector_problema():

my_file = open("segundo_problema.txt", "r")
content = my_file.read()
content_list = content.split("\n")
    
_incompatibilidades = []
tiempos = {}

for e in content_list:
    elemento =  e.split(" ")
        
    if(elemento[0] == 'e'):
        _incompatibilidades.append([int(elemento[1]), int(elemento[2])])

    if(elemento[0] == 'n'):
        tiempos[int(elemento[1])] = int(elemento[2])

incompatibilidades = {}
for prenda in tiempos.keys():
    nuevas_incompatibilidades = []
    incompatibilidades[prenda] = nuevas_incompatibilidades

for prenda in tiempos.keys():
    incompatibilidadesPrenda = incompatibilidades[prenda]
    for i in _incompatibilidades:
        if prenda in i:

            prendaIncompatible = i[0] if i[0] !=prenda else i[1]

            if(prendaIncompatible not in incompatibilidadesPrenda):
                incompatibilidadesPrenda.append(prendaIncompatible)
            
            incompatibilidadesPrendaIncompatible = incompatibilidades[prendaIncompatible]
            if(prenda not in incompatibilidadesPrendaIncompatible):
                incompatibilidadesPrendaIncompatible.append(prenda)


    incompatibilidades[prenda] = incompatibilidadesPrenda


def ordenar_prendas(tiempos):
    # Esta linea comentada es la que ordena por tiempos
    return list({k: v for k, v in sorted(tiempos.items(), key=lambda x: x[1], reverse=True)}.keys())
    return list(tiempos.keys())


all_prendas =  ordenar_prendas(tiempos)
    # return incompatibilidades_, tiempos

def generador_solucion0(incompatibilidades, prendas_ordenadas):
    lavados = []

    while len(prendas_ordenadas):
        prenda_principal = prendas_ordenadas.pop(0)
        nuevo_lavado = [prenda_principal]
        for prenda in prendas_ordenadas:
            if(prenda_compatible_con_lavado(prenda, nuevo_lavado, incompatibilidades)):
                nuevo_lavado.append(prendas_ordenadas.pop(prendas_ordenadas.index(prenda)))
        lavados.append(nuevo_lavado)
    
    return lavados


def generador_solucion(_prendas_ordenadas):
    lavados = []
    #esto es para que no se copie la referencia.
    prendas_ordenadas = _prendas_ordenadas[:]
    if(len(prendas_ordenadas)<=1):
        return [prendas_ordenadas]

    while len(prendas_ordenadas):
        prenda_principal = prendas_ordenadas.pop(0)

        compatibilidades_con_prenda =  compatibilidades(prenda_principal, prendas_ordenadas)
        lavados_con_compatibles = generador_solucion(compatibilidades_con_prenda) 

        nuevo_lavado = elegir_lavado(lavados_con_compatibles)
        
        for p in nuevo_lavado:
            prendas_ordenadas.pop(prendas_ordenadas.index(p))

        nuevo_lavado.append(prenda_principal)
        lavados.append(nuevo_lavado)

    return lavados

def elegir_lavado(lavados):
    return lavados[0]
    #  Aca queria probar algo pero no hizo falta, pero lo dejo por si lo quiero retomar en otro momento
    # lavado_mas_largo = []
    # for l in lavados_con_compatibles:
    #     t_actual = calcular_tiempo_total(l)
    #     if calcular_tiempo_total(lavado_mas_largo) < t_actual:
    #         lavado_mas_largo = l
        

   
def calcular_tiempo_total(lavados):
    tiempo_total = 0

    for l in lavados:
        max = 0
        for p in l:

            if tiempos[p] > max:
                max = tiempos[p]
        tiempo_total += max

    return tiempo_total

def prendas_son_compatibles(prenda1, prenda2):
    return not prenda2 in incompatibilidades[prenda1]

def prenda_compatible_con_lavado(prenda, lavado):
    for p in lavado:
        if not prendas_son_compatibles(prenda, p):
            return False

    return True

def generador_solcion2(prendas):
    lavados_posibles = generar_todos_lavados_posibles(prendas[0])
    mejor_solucion= []
    mejor_puntaje= 10000
    puntajes = {}
    soluciones = {}
    for lavado in lavados_posibles:
        score_lavado, solucion = puntear_lavado(lavado)

        if score_lavado < mejor_puntaje:
            mejor_puntaje = score_lavado
            mejor_solucion = solucion
            
    
    return mejor_solucion, mejor_puntaje

def puntear_lavado(lavado):
    prendas_restantes = restar_conjuntos(all_prendas, lavado)

    solucion = generador_solucion(prendas_restantes)

    solucion.append(lavado)
    score = calcular_tiempo_total(solucion)
    print("lavado, restantes, score", lavado, prendas_restantes, score)
    return score, solucion


def generar_todos_lavados_posibles(prenda):
    compats = compatibilidades(prenda, all_prendas)
    trivial = [prenda]
    lavados = _generar_todos_lavados_posibles(trivial, compats)
    lavados.append(trivial)
    return lavados

def _generar_todos_lavados_posibles(lavado, prendas_restantes):
    if(len(prendas_restantes) == 1):
        if prenda_compatible_con_lavado(prendas_restantes[0], lavado):
            nuevo_lavado = lavado[:]
            nuevo_lavado.append(prendas_restantes[0])
            return [nuevo_lavado]
        else:
            return [lavado[:]]
    elif len(prendas_restantes) == 0:
        return [lavado[:]]
    
    lavados = []
    
    for p in prendas_restantes:
        nuevo_lavado = lavado[:]
        if(not prenda_compatible_con_lavado(p,nuevo_lavado)):
            if(not nuevo_lavado in lavados):
                lavados.append(nuevo_lavado) 
            continue
            
        nuevo_lavado.append(p)
        nuevos_lavados_posibles = _generar_todos_lavados_posibles(nuevo_lavado,  restar_conjuntos(prendas_restantes, [p]) )
        #lavados.append(nuevos_lavados_posibles)
        for n_l in nuevos_lavados_posibles:
            if not lavado_ya_existe(n_l, lavados):
                lavados.append(n_l)
        
    print(lavados)
    return lavados

def lavado_ya_existe(lavado, lavados):
    for l in lavados:
        if len(l) != len(lavado):
            continue
        not_equal = False
        for prenda in lavado:
            if prenda not in l:
                not_equal = True
                break
        if not_equal:
            continue
        
        return True
        
    return False
    
def restar_conjuntos(A, B):
    return list(set(A) - set(B))
    
def exportador_resultado(lavados):
    file = open("solucion.txt", "w")
    lavado_nro = 1
    for lavado in lavados:

        for prenda in lavado:
            file.write("" + str(prenda) + " " + str(lavado_nro) + "\n")
        lavado_nro += 1


def compatibilidades(prenda, prendas_ordenadas):
    compatibilidades = []
    incompatibilidades_prenda = incompatibilidades[prenda]

    for p in prendas_ordenadas:
        if p == prenda:
            continue
        if p not in incompatibilidades_prenda:
            compatibilidades.append(p)
    return compatibilidades


def analizador_problema():
    # Realmente ya no se ordenan por tiempo, pero lo dejo asi por si quiero cambiar el orden en otro momento.
    prendas_ordenadas_por_tiempo = ordenar_prendas(tiempos)
    solucion, score =  generador_solcion2(prendas_ordenadas_por_tiempo) 
    exportador_resultado(solucion)

    # for i in range(len(solucion)):
    #     print(i, solucion[i])

    return solucion, score


#analizador_problema()
#print(analizador_problema())

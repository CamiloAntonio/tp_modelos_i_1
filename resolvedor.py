# def lector_problema():
my_file = open("primer_problema.txt", "r")
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
    incompatibilidadesPrenda = []
    for i in _incompatibilidades:
        if prenda in i:

            prendaIncompatible = i[0] if i[0] !=prenda else i[1]

            if(prendaIncompatible not in incompatibilidadesPrenda):
                incompatibilidadesPrenda.append(prendaIncompatible)


    incompatibilidades[prenda] = incompatibilidadesPrenda
        

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


def generador_solucion(incompatibilidades, prendas_ordenadas):
    lavados = []
     
    if(len(prendas_ordenadas)<=1):
        return [prendas_ordenadas]

    while len(prendas_ordenadas):
        prenda_principal = prendas_ordenadas.pop(0)

        compatibilidades_con_prenda =  compatibilidades(prenda_principal, incompatibilidades, prendas_ordenadas)
        
        lavados_con_compatibles = generador_solucion(incompatibilidades,compatibilidades_con_prenda) 
 
        lavado_mas_largo = []
        # for l in lavados_con_compatibles:
        #     t_actual = calcular_tiempo_total(l)
        #     if calcular_tiempo_total(lavado_mas_largo) < t_actual:
        #         lavado_mas_largo = l
        nuevo_lavado = lavados_con_compatibles[0]
        for p in nuevo_lavado:
            prendas_ordenadas.pop(prendas_ordenadas.index(p))

        nuevo_lavado.append(prenda_principal)
        lavados.append(nuevo_lavado)

    
    return lavados
        
def ordenar_tiempos(tiempos):
    # return list({k: v for k, v in sorted(tiempos.items(), key=lambda x: x[1], reverse=True)}.keys())
    return list(tiempos.keys())



        
def calcular_tiempo_total(lavados):
    tiempo_total = 0

    for l in lavados:
        max = 0
        for p in l:

            if tiempos[p] > max:
                max = tiempos[p]
        tiempo_total += max

    return tiempo_total

def prendas_son_compatibles(prenda1, prenda2, incompatibilidades):
    return not prenda2 in incompatibilidades[prenda1]

def prenda_compatible_con_lavado(prenda, lavado, incompatibilidades):
    for p in lavado:
        if not prendas_son_compatibles(prenda, p, incompatibilidades):
            return False
    return True

def analizador_problema():
    # incompatibilidades, tiempos = lector_problema()
    prendas_ordenadas_por_tiempo = ordenar_tiempos(tiempos)
    solucion =  generador_solucion(incompatibilidades, prendas_ordenadas_por_tiempo) 
    exportador_resultado(solucion)
    return solucion, calcular_tiempo_total(solucion)

def exportador_resultado(lavados):
    file = open("solucion.txt", "w")
    lavado_nro = 1
    for lavado in lavados:

        for prenda in lavado:
            file.write("" + str(prenda) + " " + str(lavado_nro) + "\n")
        lavado_nro += 1

def compatibilidades(prenda, incompatibilidades, prendas_ordenadas):
    compatibilidades = []
    incompatibilidades_prenda = incompatibilidades[prenda]

    for p in prendas_ordenadas:
        if p not in incompatibilidades_prenda:
            compatibilidades.append(p)
    return compatibilidades

print(analizador_problema())

# Lo deje global para poder acceder a esta informacion en todo el modulo

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

# Divisor
def generador_solucion3(_prendas_ordenadas):
    lavados = []
    prendas_ordenadas = _prendas_ordenadas
    
    while len(prendas_ordenadas):
        prenda_principal1 = prendas_ordenadas.pop(0)
        nuevo_lavado1 = [prenda_principal1]
        
        if(len(prendas_ordenadas)>0):
            prenda_principal2 = prendas_ordenadas.pop(0)
            nuevo_lavado2 = [prenda_principal2]

        
        for prenda in prendas_ordenadas:
            if(prenda_compatible_con_lavado(prenda, nuevo_lavado2)):
                nuevo_lavado2.append(prendas_ordenadas.pop(prendas_ordenadas.index(prenda)))

            
            elif(prenda_compatible_con_lavado(prenda, nuevo_lavado1)):
                nuevo_lavado1.append(prendas_ordenadas.pop(prendas_ordenadas.index(prenda)))
            
        lavados.append(nuevo_lavado1 )
        lavados.append(nuevo_lavado2)
    
    return lavados, calcular_tiempo_total(lavados)
    
def exportador_resultado(lavados):
    file = open("solucion.txt", "w")
    lavado_nro = 1
    for lavado in lavados:

        for prenda in lavado:
            file.write("" + str(prenda) + " " + str(lavado_nro) + "\n")
        lavado_nro += 1

def analizador_problema():
    solucion, score =  generador_solucion3(all_prendas) 
    exportador_resultado(solucion)
    return solucion, score


#analizador_problema()
print(analizador_problema())
def lector_problema():
    my_file = open("primer_problema.txt", "r")
    content = my_file.read()
    content_list = content.split("\n")
    
    incopatibilidades = []
    tiempos = {}
    for e in content_list:
        elemento =  e.split(" ")
        
        if(elemento[0] == 'e'):
            incopatibilidades.append([int(elemento[1]), int(elemento[2])])

        if(elemento[0] == 'n'):
            tiempos[int(elemento[1])] = int(elemento[2])

    incopatibilidades_ = {}

    for prenda in tiempos.keys():
        incopatibilidadesPrenda = []
        for i in incopatibilidades:
            if prenda in i:

                prendaIncopatible = i[0] if i[0] !=prenda else i[1]

                if(prendaIncopatible not in incopatibilidadesPrenda):
                    incopatibilidadesPrenda.append(prendaIncopatible)


        incopatibilidades_[prenda] = incopatibilidadesPrenda
        

    return incopatibilidades_, tiempos

def analizador_problema():
    incopatibilidades, tiempos = lector_problema()
    return generador_solucion(incopatibilidades, tiempos)

def generador_solucion(incopatibilidades, tiempos):
    lavados = []


    for prenda in tiempos.keys():
        lavadoPrenda= None
        for lavado in lavados:
            if prenda in lavado:
                lavadoPrenda = lavado
        if not lavadoPrenda:
            lavados.append([prenda])
            continue
    
    # print(lavados)
    return lavados
        
            
        
    

print(analizador_problema())
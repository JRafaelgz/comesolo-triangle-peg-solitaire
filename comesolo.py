"""
Solución de problemas con expansión de árboles / Comesolo / Triangle Peg Solitaire
Autor: JRafaelgz

Código basado en: 
Solución del 8-puzle expandiendo un árbol de movimientos
Autor: jpiramirez https://github.com/jpiramirez

Curso IA, UG
"""

class Triangle5():
    def __init__(self, inicio):
        self.referencia = ( 'a1','a0','a0','a0','a0',
                            'a2','b2','a0','a0','a0',
                            'a3','b3','c3','a0','a0',
                            'a4','b4','c4','d4','a0',
                            'a5','b5','c5','d5','e5') #Se usará este arreglo para poder ubicar de manera simbólica cada posición
        self.root =[1,2,2,2,2,
                    1,1,2,2,2,
                    1,1,1,2,2,
                    1,1,1,1,2,
                    1,1,1,1,1] #Plantilla de tablero con todos los peg   
        pos = self.referencia.index(inicio) #Según la posición inicial elegida se colocará un cero
        self.root[pos] = 0 #Guardaremos la configuración inicial donde 1 = Hay poste, 0 = No hay poste, 2 = Ignorar casilla (solo se usa para completar el arreglo)
        self.stree = {0 : [set(), self.root, -1]} #Diccionario con el árbol que contendrá a todos los nodos
        self.nnodes = 1 #numero de nodos hasta el momento
        self.gnode = -100 #Guardará la ubicación del nodo donde estará la solución
        
    def genmoves(self,b): #Función que generará los posibles movimientos del tablero
        lmov = [] #Lista que contendrá los posibles movimientos
        Ceros = [i for i in range(len(b)) if b[i] == 0] #Se crea una lista con la posición/índice de los ceros del tablero/lista
        for c in Ceros: #Conforme el juego avance habrá varios ceros, por lo que se tendrá que pasar por todos los ceros que pueden generar movimientos
            i = c // 5 # se está encontrando la fila y columna donde está la posición como si estuviéramos viendo una matriz de 4x4 contando al cero
            j = c % 5 #Donde i son columnas y j son las filas, por ejemplo a1 seria 0,0 y b3 seria 2,1 (i,j)
            #Todos estos movimientos son considerando el tablero como triangulo rectángulo(TR), los cuales equivalen a los posibles movimientos del tablero original (O)
            if i < 3: #Los siguientes dos movimientos solo se pueden hacer hasta la altura 2, porque a mayor altura al calcular las ubicaciones ya nos salimos del arreglo
                #La fórmula 5*i+j se encontró haciendo la ecuación de dos puntos conocidos y resolviendo el sistema de ecuaciones encontrando 5 y 1 
                #La fórmula anterior convierte los valores de i,j en el índice de la lista b, básicamente nos da la posición en esa lista
                if (b[5*(i+2)+j] == 1) and ((b[5*(i+1)+j] == 1)):#Genera movimientos verticales abajo (TR) o Diagonal hacia arriba derecha (O), ejemplo a3->a1  
                    lmov.append(b.copy()) #mete una copia de todo el tablero al final de la lista
                    lmov[-1][5*(i+2)+j] = 0 #(TR) Los dos elementos debajo del cero pasan de ser unos a ceros
                    lmov[-1][5*(i+1)+j] = 0 #y el elemento que era cero pasa a ser uno
                    lmov[-1][5*(i)+j] = 1 
                if (b[5*(i+2)+j+2] == 1) and ((b[5*(i+1)+j+1] == 1)): #Genera movimientos diagonal Abajo-derecha (TR) o Diagonal hacia arriba izquierda (O), ejemplo c3->a1
                    lmov.append(b.copy()) 
                    lmov[-1][5*(i+2)+j+2] = 0 #(TR) Los elementos en diagonal abajo derecha pasan de ser unos a ceros 
                    lmov[-1][5*(i+1)+j+1] = 0 #y el elemento que era cero pasa a ser uno
                    lmov[-1][5*(i)+j] = 1   
            if i > 1:
                if (b[5*(i-2)+j] == 1) and ((b[5*(i-1)+j] == 1)):#Genera movimientos verticales arriba (TR) o Diagonal hacia abajo izquierda (O), ejemplo a1->a3
                    lmov.append(b.copy()) 
                    lmov[-1][5*(i-2)+j] = 0
                    lmov[-1][5*(i-1)+j] = 0
                    lmov[-1][5*(i)+j] = 1
                if j < 3:
                    if (b[5*(i)+j+2] == 1) and (b[5*(i)+j+1] == 1): #Genera movimiento horizontal derecha a izquierda (TR y O), ejemplo c3->a3
                        lmov.append(b.copy()) 
                        lmov[-1][5*(i)+j+2] = 0
                        lmov[-1][5*(i)+j+1] = 0
                        lmov[-1][5*(i)+j] = 1
                if j > 1:
                    if (b[5*(i)+j-2] == 1) and (b[5*(i)+j-1] == 1): #Genera movimiento horizontal de izquierda a derecha (TR y O), ejemplo a3->b3
                        lmov.append(b.copy()) 
                        lmov[-1][5*(i)+j-2] = 0
                        lmov[-1][5*(i)+j-1] = 0
                        lmov[-1][5*(i)+j] = 1
                    if (b[5*(i-2)+j-2] == 1) and ((b[5*(i-1)+j-1] == 1)): #Genera movimientos diagonal Arriba-izquierda (TR) o Diagonal hacia abajo izquierda (O), ejemplo a1->c3
                        lmov.append(b.copy()) 
                        lmov[-1][5*(i-2)+j-2] = 0
                        lmov[-1][5*(i-1)+j-1] = 0
                        lmov[-1][5*(i)+j] = 1       
        return lmov #regresa todos ls movimientos en forma de lista        

    def gentree(self, goal, sdepth): #Función que genera el árbol con todos los nodos y sus respectivos padres e hijos
        depth = 0
        self.gnode = -100
        gfound = False
        while depth < sdepth and gfound == False: #Este while se repetira hasta que se encuentre la meta o se pase la profundidad limite
            print('Buscando en profundidad '+str(depth))
            ntree = dict()
            for id in self.stree: #Se hará este for para cada padre del árbol
                if len(self.stree[id][0]) < 1 and gfound == False: 
                    lmov = self.genmoves(self.stree[id][1]) #Se generan los posibles movimientos para el tablero cargado
                    for mv in lmov:
                        if depth > 0:
                            if mv == self.stree[self.stree[id][2]][1]:
                                continue
                        self.stree[id][0].add(self.nnodes)
                        ntree[self.nnodes] = [set(), mv, id]
                        #---------- Comprobacion de meta ---------------
                        Ceros = [i for i in range(len(mv)) if mv[i] == 0] #Se usarán para ver si el tablero ha sido completado con la cantidad de ceros y unos de un juego terminado
                        Unos = [i for i in range(len(mv)) if mv[i] == 1]
                        if goal == '*': #Si se escogio * significa que no importa donde termine el tablero
                            if len(Ceros) == 14 and len(Unos) == 1: #Comprobamos que solo queden 14 ceros y un uno (el tablero cuenta con 15 posiciones)
                                print('Objetivo encontrado en la profundidad '+str(depth))
                                self.gnode = self.nnodes #Guardamos el número de nodo donde esta el objetivo
                                gfound = True #Cambiamos la bandera de objetivo 
                                break
                        else:    
                            meta = self.referencia.index(goal) #Buscamos el índice de la meta para después comprobar si se encuentra en el tablero
                            if len(Ceros) == 14 and mv[meta] == 1: #Comprobamos que solo queden 14 ceros y un uno en la meta escogida
                                print('Objetivo encontrado en la profundidad '+str(depth))
                                self.gnode = self.nnodes
                                gfound = True
                                break
                        self.nnodes = self.nnodes + 1 #Incrementamos el nodo en uno
            for key in ntree: #Una vez cargados todos los movimientos con sus respectivos padres e hijos, estos se cargarán al árbol
                self.stree[key] = ntree[key]
            depth = depth + 1 #Incrementamos la profundidad hasta dar con la meta
        return self.gnode
    
    def printsolution(self):
        if self.gnode < -1: #gnode solo cambia su valor a positivo cuando se encontró el objetivo
            print('Aun no se ha encontrado una solucion...')
            return
        sol = [] #Contendra todos los pasos hasta llegar al objetivo
        cnode = self.gnode
        while cnode != -1: #cnode más adelante ira tomando el número de los padres empezando por el final e ira disminuyendo hasta encontrar a la raíz o primer nodo
            sol.append(self.stree[cnode][1]) #Se irán agregando desde el último movimiento hasta el primero en la lista sol
            cnode = self.stree[cnode][2] #Se va guardando el nombre de los padres

        sol.reverse() #Como se fueron guardando del final al inicio hay que invertir el orden con reverse
        print('Numero de pasos requeridos: '+str(len(sol)-1))
        print('Pasos para llegar a la solucion:')
        count = 0
        for n in sol:
            print('Paso: #'+str(count)) #Se irán contando los pasos
            self.printMov(self.convtab(n)) #Primero se convierte el tablero de unos, ceros y dos en la configuración original para después ser impresos con la función printMov
            print(self.convtab(n))#Por cada tablero de sol se manda a llamar a la función convtab que básicamente convierte el tablero
            print('')
            count +=1
    
    def convtab(self,b): #Funcion que convertirá el tablero numérico al tablero de referencia además de eliminar a los números 2
        aux = [0,5,6,10,11,12,15,16,17,18,20,21,22,23,24] #Estos valores son los índices de donde debería de haber ceros o unos
        aux2 = []
        for i in aux:
            if b[i] == 1:#Si hay un 1 significa que hay una casilla por lo que se busca en la referencia esa casilla para reemplazar el 1 por una casilla, por ejemplo, b2
                aux2.append(self.referencia[i]) 
            else:
                aux2.append(0)
        return aux2 #Aux solo contendra ceros y nombres de casillas

    def printMov(self,b):#Esta función permite imprimir el tablero con forma la forma original triangular
        print('    '+str(b[0]))
        print('   '+str(b[1]),b[2])
        print('  '+str(b[3]),b[4],b[5])
        print(' '+str(b[6]),b[7],b[8],b[9])
        print(b[10],b[11],b[12],b[13],b[14])             

#Ejecución del programa-------------------------
print('Solución del juego Comesolo de 15 posiciones:')
print('    a1')
print('   a2 b2')
print('  a3 b3 c3')
print(' a4 b4 c4 d4')
print('a5 b5 c5 d5 e5')
print('Escriba el poste que comenzara vacio (usando la notación anterior):') 
inicio = input()
print('Escriba la posicion final del poste (si no importa escriba: *):')
final = input()

a = Triangle5(inicio) #Se carga la posición inicial donde se quitará el poste
g = a.gentree(final, 25)#El segundo elemento indica a la profundidad limite de busqueda 

if g < 0:
    print('Objetivo no encontrado')

a.printsolution()

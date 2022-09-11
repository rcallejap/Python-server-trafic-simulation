#Equipo 6

#Programa principal para proyecto de Sistemas multiagentes que
# 1.Llena un grafo con nodos y pesos representando las calles cercanas a la zona Tec
# 2.Crea una lista de rutas traduciendo los nodos a calles
# 3.Genera un arreglo con datos de prueba de carros con inicio y fin predeterminados
# 4.Se utiliza el algoritmo de dijkstra para encontrar el camino más rápido entre inicio y fin
# 5.Se transforman los nodos resultantes de dijkstra a sus números de calle
# 6. Inicia la simulación con los coches
#

#import numpy as np
from unittest import result
import networkx as nx
#import matplotlib.pyplot as plt
#import math
#import matplotlib.animation as animation
from trafficSimulator import *

from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import matplotlib.pyplot as plt


#es importante descargar la libreria de pygames y la de networkx para poder usar el programa


#El primer paso es crear un grafo con tadas las posibles rutas que puede tomar el vehiculo 
# y les asigna un peso dependiendo de la hora y el trafico que puede haber en esa hora

#para este grafo nos apoyamos en el siguiente video de youtube https://www.youtube.com/watch?v=PouhDHfssYA 
# y esta pagina #https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.weighted.dijkstra_path.html 
#En cuanto a los pesos, se hizo una estimación manual considerando el tráfico que hay por hora de acuerdo a Google Maps
hora = 6
G = nx.DiGraph()
if hora <= 6 or hora >= 22:
  G.add_edge("1,1", "2,7", weight=200)
  G.add_edge("2,7", "6.7,7.5", weight=347*1.5)
  G.add_edge("6.7,7.5", "6.3,10", weight=158)
  G.add_edge("6.7,7.5", "7.5,4", weight= 231.5)
  G.add_edge("7.5,4", "8,1.6", weight=231.5)
  G.add_edge("8,1.6", "9,1.8", weight=96)
  G.add_edge("8,1.6", "1,1", weight=200)
  G.add_edge("9,1.8", "12,2.3", weight=202)
elif hora >= 7 or hora == 8 or hora == 10 or hora == 16 or hora == 21:
  G.add_edge("1,1", "2,7", weight=200)
  G.add_edge("2,7", "6.7,7.5", weight=347*1.5)
  G.add_edge("6.7,7.5", "6.3,10", weight=158)
  G.add_edge("6.7,7.5", "7.5,4", weight= 231.5*1.5)
  G.add_edge("7.5,4", "8,1.6", weight=231.5)
  G.add_edge("8,1.6", "9,1.8", weight=96)
  G.add_edge("8,1.6", "1,1", weight=156)
  G.add_edge("9,1.8", "12,2.3", weight=202)
elif hora == 9 or hora == 11 or hora == 12 or hora == 17 or hora == 18 or hora == 19 or hora == 20:
  G.add_edge("1,1", "2,7", weight=200)
  G.add_edge("2,7", "6.7,7.5", weight=347*2)
  G.add_edge("6.7,7.5", "6.3,10", weight=158*1.5)
  G.add_edge("6.7,7.5", "7.5,4", weight= 231.5*2)
  G.add_edge("7.5,4", "8,1.6", weight=231.5)
  G.add_edge("8,1.6", "9,1.8", weight=96)
  G.add_edge("8,1.6", "1,1", weight=156)
  G.add_edge("9,1.8", "12,2.3", weight=202)
elif hora == 13 or hora == 14 or hora == 15:
  G.add_edge("1,1", "2,7", weight=200)
  G.add_edge("2,7", "6.7,7.5", weight=347*2.5)
  G.add_edge("6.7,7.5", "6.3,10", weight=158*2)
  G.add_edge("6.7,7.5", "7.5,4", weight= 231.5*2.5)
  G.add_edge("7.5,4", "8,1.6", weight=231.5)
  G.add_edge("8,1.6", "9,1.8", weight=96)
  G.add_edge("8,1.6", "1,1", weight=156)
  G.add_edge("9,1.8", "12,2.3", weight=202)

  nx.draw_networkx(G, with_labels = True)



#Por cada cambio de nodo a nodo que hay, se adjunta al arreglo lista_rutas un número correspondiente a la calle que se cruza
def ListaRutas(lista):
    lista_rutas = []
    for i in range(len(lista)-1):
        if (str(lista[i]))== '1,1' and (str(lista [i+1])) == '2,7':
            lista_rutas.append(0)
        elif (str(lista[i]))== '2,7' and (str(lista [i+1])) == '6.7,7.5':
            lista_rutas.append(1)
        elif (str(lista[i]))== '6.7,7.5' and (str(lista [i+1])) == '6.3,10':
            lista_rutas.append(2)
        elif (str(lista[i]))== '6.7,7.5' and (str(lista [i+1])) == '7.5,4':
            lista_rutas.append(3)
        elif (str(lista[i]))== '7.5,4' and (str(lista [i+1])) == '8,1.6':
            lista_rutas.append(4)
        elif (str(lista[i]))== '8,1.6' and (str(lista [i+1])) == '9,1.8':
            lista_rutas.append(5)
        elif (str(lista[i]))== '9,1.8' and (str(lista [i+1])) == '12,2.3':
            lista_rutas.append(6)
        elif (str(lista[i]))== '12,2.3' and (str(lista [i+1])) == '1,1':
            lista_rutas.append(7)
    return lista_rutas



#Este arreglo contiene las rutas que tienen los autos, cada elemento de la lista contiene un par cordenadas que representan donde empezo y donde termino la ruta
#En otras palabras, son datos de prueba
entradas=[('1,1','6.7,7.5'),
            ('1,1','6.3,10'),
            ('1,1','7.5,4'),
            ('7.5,4','12,2.3'),

          
]

#En arreglo_cordenadas se guardan todos los puntos por los que tienen que pasar cada vehiculo para llegar a la meta, utilizando el grafo que se creo anteriormente y el algoritmo de dijkstra
arreglo_cordenadas = []
for i in range(len(entradas)):
    lista_cordenadas = nx.dijkstra_path(G, source=str(entradas[i][0]), target=str(entradas[i][1]))
    arreglo_cordenadas.append(lista_cordenadas)


#En este arreglo se guarda el numero de calle por el que tiene que pasar cada vehiculo para llegar a la meta
#utiliza el arreglo de arreglo_cordenadas 
arreglo_rutas = []
for i in range(len(arreglo_cordenadas)):
    arreglo_rutas.append(ListaRutas(arreglo_cordenadas[i]))



#Inicia la simulacion de las calles y los vehiculos 
#basamos este modelo en el de la pagina https://towardsdatascience.com/simulating-traffic-flow-in-python-ee1eab4dd20f


sim = Simulation()

sim.create_roads([
    #conseguimos estas cordenadas usando la herrramienta de desmos y geogebra, 
    #insertando una imagen del mapa del campus y asignando puntos en cada inicio de una calle 
    ((-3, 73),(25, 22)),                # Road 0
    ((25, 22),(-6, -5.5)),              # Road 1
    ((-6, -5.5),(0.75, -12.5)),         # Road 2
    ((-6, -5.5),(-30, 16.5)),           # Road 3
    ((-30, 16.5), (-48.25, 34.8)),      # Road 4
    ((-48.25, 34.8), (-3, 73)),         # Road 5
    ((-48.25, 34.8), (-56, 28.25)),     # Road 6
    ((-56, 28.25), (-66, 20))           # Road 7

])

#se crean los agentes que van a simular el movimiento de los vehiculos
sim.create_gen({
    'vehicle_rate': 30,   #velocidad de generacion de vehiculos
    'vehicles': [
        [1, {'path': arreglo_rutas[0]}],    #Se utiliza el arreglo de rutas para que cada vehiculo se mueva en una ruta diferente
        [1, {'path': arreglo_rutas[1]}],
        [1, {'path': arreglo_rutas[2]}], 
        [1, {'path': arreglo_rutas[3]}] ,
        [1, {'path': [4,5]}], 
        [1, {'path': [4,6,7]}] 
    ]
})



'''
temp = 10; 
sim.create_signal([[0], [1]], temp)


temp2 = 8; 
sim.create_signal([[4], [5]], temp2)
'''

def run_sim(time, sim = Simulation()):
    simCopy=deepcopy(sim)
    simCopy.create_signal([[0,4], [1,5]], time)
    sim1=deepcopy(simCopy) 
    sim2=deepcopy(simCopy)  
    sim3=deepcopy(simCopy)  
    sim4=deepcopy(simCopy)  
    sim5=deepcopy(simCopy)  
    for i in range (0, 18000): 
        sim1.update()
        sim2.update()
        sim3.update()
        sim4.update()
        sim5.update()
    
    return (sim1.AvgTime+sim2.AvgTime+sim3.AvgTime+sim4.AvgTime+sim5.AvgTime)/5


''' 

tiempos = [6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20]

resultados = []

for i in tiempos:
    valor = run_sim(i, sim)
    print("tiempos" )
    print (i)
    print("valor")
    print (valor)
    resultados.append(valor)


print ("_______________________________________________________________")
plt.plot(tiempos,resultados)
plt.show()
print ("_______________________________________________________________")

'''
sim.create_signal([[0,4], [1,5]], 8)

#for i in range (0, 18000): 
    #sim.update()


#_______________________________________________________________________________________________________________________
#Server


def updatePositions():
    global sim
    sim.update()

    positions = sim.listPos
    return positions

def positionsToJSON(ps):
    posDICT = []
    sem = {
        "estatus":  sim.traffic_signals[0].current_cycle_index
    }
    posDICT.append(sem)
    for p in ps:
        pos = {
            "id" : p[0],
            "x" : p[1],
            "y" : .35,
            "z" : p[2]
        }
        posDICT.append(pos)
    return json.dumps(posDICT)


class Server(BaseHTTPRequestHandler):
    
    def _set_response(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        
    def do_GET(self):
        logging.info("GET request,\nPath: %s\nHeaders:\n%s\n", str(self.path), str(self.headers))
        self._set_response()
        self.wfile.write("GET request for {}".format(self.path).encode('utf-8'))

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        #post_data = self.rfile.read(content_length)
        post_data = json.loads(self.rfile.read(content_length))
        #logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     #str(self.path), str(self.headers), post_data.decode('utf-8'))
        logging.info("POST request,\nPath: %s\nHeaders:\n%s\n\nBody:\n%s\n",
                     str(self.path), str(self.headers), json.dumps(post_data))
        
        '''
        x = post_data['x'] * 2
        y = post_data['y'] * 2
        z = post_data['z'] * 2
        
        position = {
            "x" : x,
            "y" : y,
            "z" : z
        }

        self._set_response()
        #self.wfile.write("POST request for {}".format(self.path).encode('utf-8'))
        self.wfile.write(str(position).encode('utf-8'))
        '''
        
        positions = updatePositions()
        #print(positions)
        self._set_response()
        resp = "{\"data\":" + positionsToJSON(positions) + "}"
        #print(resp)
        self.wfile.write(resp.encode('utf-8'))


def run(server_class=HTTPServer, handler_class=Server, port=8585):
    logging.basicConfig(level=logging.INFO)
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    logging.info("Starting httpd...\n") # HTTPD is HTTP Daemon!
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:   # CTRL+C stops the server
        pass
    httpd.server_close()
    logging.info("Stopping httpd...\n")

if __name__ == '__main__':
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()

#_______________________________________________________________________________________________________________________








# Start simulation
'''
win = Window(sim)
win.zoom = 8
win.run(steps_per_update=1)

'''

import json
import sys

# egesz program szimulalasat vegzo osztaly
class Circuit:
    def __init__(self, fileName):
        self.fileName = fileName
        self.data = self.readFile()

    def printData(self):
        print(self.data)

    #file beolvasasa 
    def readFile (self):
        with open (self.fileName, "r") as read_file:
            self.data = json.load(read_file)

        return self.data

    def simulationOfDemands(self):
        graph = Graph(self.data)
        self.graph = graph.createVertices()
        graph.findPath()

# iranyitatlan graf szimulalasat vegzo osztaly
class Graph:
    def __init__(self, data):
        self.data = data
        self.graph_elements = self.createVertices()
    
    # dict letrehozasa
    def createVertices(self):
        tmp_vertices = self.data['end-points'] + self.data['switches']
        self.graph_elements = {}

        for i in range(len(tmp_vertices)):
            tmp_ver = []
            self.graph_elements[tmp_vertices[i]] = {}

            for j in self.data['links']:
                if tmp_vertices[i] in j['points']:
                    tmp_ver.append(j)
            self.graph_elements[tmp_vertices[i]]['links'] = tmp_ver
            
            tmp_circ = []
            for k in self.data['possible-circuits']:
                if tmp_vertices[i] == k[0]:
                    tmp_circ.append(k)
            self.graph_elements[tmp_vertices[i]]['circuits'] = tmp_circ

        return self.graph_elements

    def findPath(self):
        timer = 1   # kor szamlalasahoz seged valtozo
        event_counter = 1   # esemenyek sorszamanak nyilvantartasat vegzo seged valtozo
        available_switches = self.data['switches'].copy()
        available_resources = {}
        # egy kor szimulalasa
        for x in range(timer, self.data['simulation']['duration']+1):

            for i in self.data['simulation']['demands']:

                if i['end-time'] == timer:
                    for z in available_resources[i['end-points'][0]]:
                        # az eddig foglalt eroforrasokat visszarakom, hogy ujra elerhetoek legyenek
                        if z not in available_switches:
                            available_switches.append(z)
                    print("{0}. igény felszabadítás: {1}<->{2} st:{3}".format(event_counter, i['end-points'][0], i['end-points'][1], timer))
                    event_counter += 1

                if i['start-time'] == timer:
                    demand = i['demand']
                    is_available = True
                    enough_capacity = True
                    
                    for j in self.graph_elements[i['end-points'][0]]['circuits']:
                        tmp_len = len(j)
                        tmp_counter = 0

                        # keresem az elso megfelelo utat a listabol, seged szamlalokat hasznalok hozza
                        for k in range(1, tmp_len-1):
                            if j[k] in available_switches:
                                tmp_counter += 1
                        if tmp_counter == tmp_len - 2:
                            available_resources[i['end-points'][0]] = j
                            for g in self.data['links']:
                                for z in range(0, len(j) - 1 ):
                                    if j[z] == g['points'][0] and j[z+1] == g['points'][1] and g['capacity'] < demand:
                                        enough_capacity = False

                            # kiveszem az elerheto switch-ek kozul azt, ami az adott utat erinti
                            for y in j:
                                if y in available_switches:
                                    available_switches.remove(y)
                            break
                        else:
                            is_available = False
                    
                    if is_available and enough_capacity:
                        print("{0}. igény foglalás: {1}<->{2} st:{3} - sikeres".format(event_counter, i['end-points'][0], i['end-points'][1], timer))
                        event_counter += 1
                    else:
                        print("{0}. igény foglalás: {1}<->{2} st:{3} - sikertelen".format(event_counter, i['end-points'][0], i['end-points'][1], timer))
                        event_counter += 1

            timer += 1
        return 
  
circuit = Circuit(sys.argv[1])
circuit.simulationOfDemands()
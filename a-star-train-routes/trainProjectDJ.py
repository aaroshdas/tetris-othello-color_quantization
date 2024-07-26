from math import pi , acos , sin , cos
import heapq
from time import perf_counter
import tkinter as tk
start = perf_counter()

allNodes = set()
with open("rrNodes.txt") as f:
    allNodes = [line.strip() for line in f]
node_locations = {}
root = tk.Tk() #creates the frame

canvas = tk.Canvas(root, height=1000, width=1000, bg='white')
for node in allNodes:
    node_locations[node[:7]] = (float(node[8:17]), float(node[18:28]))


#UNNESCARY
with open("rrNodeCity.txt") as f:
    cities = [line.strip() for line in f]
cityDict= {}
for i in cities:
    cityDict[i[8:]] = i[:7]


intersects= []
with open("rrEdges.txt") as f:
    intersects = [line.strip() for line in f]


def calcd(node1, node2):
   # y1 = lat1, x1 = long1
   # y2 = lat2, x2 = long2
   # all assumed to be in decimal degrees
   y1, x1 = node1
   y2, x2 = node2

   R   = 3958.76 # miles = 6371 km
   y1 *= pi/180.0
   x1 *= pi/180.0
   y2 *= pi/180.0
   x2 *= pi/180.0

   # approximate great circle distance with law of cosines
   return acos( sin(y1)*sin(y2) + cos(y1)*cos(y2)*cos(x2-x1) ) * R

node_dict = {}
lines= {}
for nodes in intersects:
    loc1 =nodes[:7]
    loc2 = nodes[8:]

    line = canvas.create_line([(1000/70 * node_locations[loc1][1] + 1000/70*130, 1000/-46*node_locations[loc1][0] + 60000/46), (1000/70 * node_locations[loc2][1] + 1000/70*130, 1000/-46*node_locations[loc2][0] + 60000/46)], tag='grid_line')
    #c.create_line([(0, 0), (400, 400)], tag = 'grid_line')
    canvas.pack(expand=True) 
    lines[(loc1, loc2)] = line
    lines[(loc2, loc1)] = line

    if(loc1 not in node_dict):
        node_dict[loc1] = list()
    node_dict[loc1].append((loc2, calcd(node_locations[loc1], node_locations[loc2])))
    if(loc2 not in node_dict):
        node_dict[loc2] = list()
    node_dict[loc2].append((loc1, calcd(node_locations[loc1], node_locations[loc2])))
    
    

def GetChildren(node_number):
    return node_dict[node_number]

def DijkstrasAlg(start_node, goal_node):
    fringe = []
    closed = set()
    depth = 0
    history = []
    history.append(start_node)
    starting_node = (depth, start_node, history)
    heapq.heappush(fringe, starting_node)
    while len(fringe) > 0:
        #print(fringe)
        node = heapq.heappop(fringe)
        #print(node)
        if(node[1] == goal_node):
            return node
        if(node[1] not in closed):
            closed.add(node[1])
            solutionList = GetChildren(node[1])
            for c in solutionList:
                if(c[0] not in closed):
                    nodeNum = c[0]
                    # print(c)
                    distance = float(c[1]) + node[0]
                    historyList = node[2].copy()
                    historyList.append(nodeNum)
                    new_node = (distance, nodeNum, history)
                    canvas.itemconfig(lines[new_node[1], node[1]], fill="green")
                    root.update()
                    heapq.heappush(fringe, new_node)
    return "No solution", "No solution", "No solution"


end = perf_counter()
print("Time to create data structure:", end - start)
print("")
print("Alburquerque to Atlanta")
start = perf_counter()
distance, num, history = DijkstrasAlg(cityDict["Albuquerque"], cityDict["Atlanta"])
for i in range(len(history)-1):
    canvas.itemconfig(lines[history[i], history[i+1]], fill="red")
    root.update()
end = perf_counter()
print("Time to find solution:", end - start)
print(num)
print("Distance: " + str(distance))
print("")


print("Leon to Tuscon")
start = perf_counter()
distance, num, history = DijkstrasAlg(cityDict["Leon"], cityDict["Tucson"])
for i in range(len(history)-1):
    canvas.itemconfig(lines[history[i], history[i+1]], fill="red")
    root.update()
end = perf_counter()
print("Time to find solution:", end - start)
print(num)
print("Distance: " + str(distance))
print("")

input1 = input("")
print("Ciudad Juarez to Montreal")
start = perf_counter()
distance, num, history = DijkstrasAlg(cityDict["Ciudad Juarez"], cityDict["Montreal"])
for i in range(len(history)-1):
    canvas.itemconfig(lines[history[i], history[i+1]], fill="red")
    root.update()
end = perf_counter()
print("Time to find solution:", end - start)
print(num)
print("Distance: " + str(distance))

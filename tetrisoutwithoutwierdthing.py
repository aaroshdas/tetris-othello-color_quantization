import random
import json

RUN_PER_STRATEGY = 5
POPULATION_SIZE = 500
NUM_CLONES = 75
TOURNAMENT_SIZE = 40
TOURNAMENT_WIN_PROBABILITY = 0.7
MUTATION_RATE = 0.1
MUTATION_AMNT = 0.1



#0 = y cord
#1 = x cord

I0 = [(0,0), (0,1), (0,2), (0,3)]
I1 = [(0,0), (1,0),(2,0),(3,0)]

O0 = [(0,0),(0,1),(1,0),(1,1)]

T0 = [(0,0), (0,1),(0,2), (1,1)]
T1= [(0,0),(1,0),(2,0),(1,1)]
T2 = [(0,1),(1,1),(1,0),(1,2)]
T3 = [(0,1),(1,1),(1,0),(2,1)]

S0 = [(0,0),(0,1),(1,1),(1,2)]
S1 = [(1,0),(1,1),(0,1),(2,0)]

Z0 = [(1,0),(1,1),(0,1),(0,2)]
Z1 = [(0,0),(1,0),(1,1),(2,1)]


J0 = [(0,0),(1,0),(0,1),(0,2)]
J1 = [(0,0),(1,0),(2,0),(2,1)]
J2 =[(1,0),(1,1),(1,2),(0,2)]
J3 = [(0,0),(0,1),(1,1),(2,1)]

L0 = [(0,0),(0,1),(0,2),(1,2)]
L1 = [(0,0),(1,0),(2,0),(0,1)]
L2 = [(0,0),(1,0),(1,1),(1,2)]
L3 = [(0,1),(1,1),(2,0),(2,1)]

I0B = [0,0,0,0]
I1B = [0]

O0B = [0,0]

T0B = [0,0,0]
T1B = [0,-1]
T2B= [-1, 0,-1]
T3B = [-1,0]

S0B = [0,0, -1]
S1B = [-1, 0]

Z0B = [-1,0,0]
Z1B= [0,-1]

J0B = [0, 0, 0]
J1B = [0, -2]
J2B = [-1,-1,0]
J3B= [0,0]

L0B = [0,0,0]
L1B = [0,0]
L2B = [0,-1,-1]
L3B = [-2,0]

pieceDict = {
    "L":[(L0, L0B), (L1, L1B),(L2, L2B),(L3, L3B)],
    "J":[(J0,J0B),(J1, J1B),(J2, J2B), (J3, J3B)],
    "Z":[(Z0, Z0B),(Z1, Z1B)],
    "S":[(S0,S0B),(S1, S1B)],
    "T":[(T0, T0B), (T1, T1B),(T2, T2B),(T3, T3B)],
    "O":[(O0, O0B)],
    "I":[(I0, I0B), (I1, I1B)]
}

test = "          #         #         #      #  #      #  #      #  #     ##  #     ##  #     ## ##     ## #####  ########  ######### ######### ######### ######### ########## #### # # # # ##### ###   ########"

def ReformatStringToStartInBottomLeft(board):
    boardLists = []
    for i in range(0, len(board), 10):
        boardLists.append(board[i:i+10])
    newBoard = ''.join(reversed(boardLists))
    return newBoard
def PrintBoard(board):
    boardLists = []    
    for i in range(0, len(board), 10):
        newStr = ""
        for i in board[i:i+10]:
            newStr += i
            newStr += " "
        boardLists.append(newStr)
    newBoard = ''.join(reversed(boardLists))
    for i in range(0, len(newBoard),20):
        print("|" + newBoard[i:i+20]+ "| " + str(int(i/20)))
    print("---------------------")
    print(" 0 1 2 3 4 5 6 7 8 9 ")
    print("---------------------") 
def GetPeaks(board):
    peaks = []
    for c in range(0,10):
        peakFound =False
        for r in range(19,-1, -1):
            if(board[c+10*r] == "#"):
                peaks.append(r+1)
                peakFound = True
                break
        if(peakFound ==False):
            peaks.append(1)
    return peaks

def GetFallingPiecePos(peaks, column, pieceB):
    highestPointToFallOn = 0
    for i in range(len(pieceB)):
        if(peaks[column+i] + pieceB[i] > highestPointToFallOn):
            highestPointToFallOn = peaks[column+i] + pieceB[i]
    return highestPointToFallOn

def PlacePiece(rowToPlacePiece, column, board, piece):
        boardList = list(board)
        for pieceR, pieceC in piece:
            if((rowToPlacePiece + pieceR)*10 + (column+pieceC) >199):
                return None, None
            boardList[(rowToPlacePiece + pieceR)*10 + (column+pieceC)] = "#"    
        #after loop, GET SCORE BY USING FILLED ROWS
        filledRows = []
        #DONT BREAK OUT OF LOOP JUST IN CASE WE NEED TO CHECK SCORE LATER
        for i in range(0, len(boardList), 10):
            cutRow = boardList[i:i+10]
            if(" " not in cutRow):
                filledRows.append(i)
        for row in reversed(filledRows):
            boardList[row:row+10] = []
            #PrintBoard(''.join(boardList))
            for t in range(0,10):
                boardList.append(" ")
        #check if any rows are complete, shift every piece above it 10 indexs to the left (down a row). append 10 spaces to end of string
        return ''.join(boardList), len(filledRows)
test = ReformatStringToStartInBottomLeft(test)
# with open("tetrisout.txt", "w") as f:
#     for i in pieceDict:
#         for piece in pieceDict[i]:
#             for column in range(0, 11-len(piece[1])):
#                 returnedBoard, rowCleared = PlacePiece(GetFallingPiecePos(GetPeaks(test), column, piece[1]), column, test, piece[0])
#                 if(returnedBoard != None):
#                     new_board = ''.join([returnedBoard[x:x+10] for x in range(190,-1,-10)])
#                     f.write(new_board + "\n")
#                 else:
#                     f.write("GAME OVER" + "\n")


def get_score(strategy, board, rowsCleared, peaks):
    #rows cleared
    score = 0
    score += rowsCleared * strategy[0]
    
    #get holes:
    holes = 0
    for i in range(len(peaks)):
        for piece in range(peaks[i]*10-10 + i, -1, -10):
            if(board[piece] == " "):
                holes +=1
    score += holes * strategy[1]
    
    #highest peak
    score += max(peaks) * strategy[2]

    #difference in max/min peaks
    score += (max(peaks)-min(peaks)) * strategy[3]
    
    #wells:
    minDifferenceToBeWell =3
    wells = 0
    for i in range(1, len(peaks)-1):
        if(peaks[i-1]-minDifferenceToBeWell > peaks[i] and peaks[i+1]-minDifferenceToBeWell > peaks[i]):
            wells +=1
    score+= wells*strategy[4]
    

    #roughness:
    totalRoughness = 0
    for i in range(len(peaks)-1):
        totalRoughness += abs(peaks[i]-peaks[i+1])
    score += strategy[5]*totalRoughness
    return score

def get_board_score(numOfRowsCleared):
    if(numOfRowsCleared == 1):
        return 40
    elif(numOfRowsCleared == 2):
        return 100
    elif(numOfRowsCleared == 3):
        return 300
    elif(numOfRowsCleared == 4):
        return 1200
    else:
        return 0

sampleBoard =""
for i in range(0,200):
    sampleBoard += " "
    
def play_game(strategy):
    score = 0
    board = sampleBoard
    #PrintBoard(board)
    bestBoard = board
    keys = list(pieceDict.keys())
    while True:
        bestScore = -1000000000
        bestBoardScore = 0
        pieceKey = random.choice(keys)
        peaks = GetPeaks(board)
        for orientation in pieceDict[pieceKey[0]]:
            for column in range(0, 11-len(orientation[1])):
                #print(orientation)
                returnedBoard, clearedRows  =PlacePiece(GetFallingPiecePos(peaks, column, orientation[1]), column, board, orientation[0])
                #print(None)
                if(returnedBoard != None):
                    #PrintBoard(returnedBoard)
                    returnedScore = get_score(strategy, returnedBoard, clearedRows, GetPeaks(returnedBoard))
                    if(returnedScore > bestScore):
                        bestScore = returnedScore
                        bestBoard = returnedBoard
                        bestBoardScore = get_board_score(clearedRows)
        if(bestScore == -1000000000):
            break
        else:
            board = bestBoard
            score += bestBoardScore
    return score
def fitness_score(strategy):
    score = 0
    for i in range(RUN_PER_STRATEGY):
        score += play_game(strategy)
    return score
def generate_random_strategy():
    strat = []
    for i in range(6):
        strat.append(random.random()*2-1)
    return strat
def selection_process(oldPop):
    popGroup =  random.sample(oldPop, TOURNAMENT_SIZE*2)
    tournament1 = sorted(popGroup[0:TOURNAMENT_SIZE], key = lambda x:-1*x[1])
    tournament2 = sorted(popGroup[TOURNAMENT_SIZE:len(popGroup)], key = lambda x:-1*x[1])
    parent1 = []
    i = 0
    while len(parent1) ==0:
        if(random.random() < TOURNAMENT_WIN_PROBABILITY):
            parent1 = tournament1[i][0]
        i+=1
    parent2 = []
    k = 0
    while len(parent2) ==0:
        if(random.random() < TOURNAMENT_WIN_PROBABILITY):
            parent2 = tournament2[k][0]
        k+=1
    return parent1, parent2

def breeding_process(oldPop):
    newPop = []
    seenStrats = set()
    num = 1
    for clone in range(NUM_CLONES):
        newScore = fitness_score(oldPop[clone][0])
        print(str(num) + ": " + str(newScore))
        num+=1
        newPop.append((oldPop[clone][0], newScore))
        seenStrats.add(tuple(oldPop[clone][0]))

    while len(newPop) < POPULATION_SIZE:
        child = []
        p1, p2 = selection_process(oldPop)
        for i in range(6):
            if(random.random() <= 0.5):
                # if(random.random() <= MUTATION_RATE):
                #     child.append(p1[i]+random.uniform(-MUTATION_AMNT, MUTATION_AMNT))
                # else:
                    child.append(p1[i])
            else:
                # if(random.random() <= MUTATION_RATE):
                #     child.append(p2[i]+random.uniform(-MUTATION_AMNT, MUTATION_AMNT))
                # else:
                    child.append((p2[i]))
        if random.random() <= MUTATION_RATE:
            child[random.randint(0, 5)] += random.uniform(-MUTATION_AMNT, MUTATION_AMNT)
        if tuple(child) not in seenStrats:
            newScore = fitness_score(child)
            print(str(num) + ": " + str(newScore))
            num+=1
            newPop.append((child, newScore))

            seenStrats.add(tuple(child))
    
    newPop = sorted(newPop, key = lambda x:-1*x[1])
    print("Best strategy: " + str(newPop[0][0]))
    print("The best score was: " + str(newPop[0][1]))
    sum1 = 0
    for i in newPop:
        sum1 += i[1]
    print("Avg score was: " + str(sum1/POPULATION_SIZE))
    return newPop, sum1, newPop[0][1]




oldPop = []
loadFromFile = input("Load From File (only if file already exists) Y/N? ")
if(loadFromFile.upper() == "Y"):
    with open('saved_gen.json', 'r') as file1:
        oldPop = json.load(file1)


while len(oldPop) < POPULATION_SIZE:
    strat = generate_random_strategy()
    stratScore = fitness_score(strat)
    if((strat,stratScore) not in oldPop):
        print(str(len(oldPop)+1) + ": " + str(stratScore))
        oldPop.append((strat, stratScore))

oldPop = sorted(oldPop, key = lambda x:-1*x[1])

print("Results of generation 0 (random generation):")
print("Best strategy: " + str(oldPop[0][0]))
print("The best score in this generation was: " + str(oldPop[0][1]))
sum1 = 0
for i in oldPop:
    sum1 += i[1]
oldAverage = sum1/POPULATION_SIZE
oldBest = oldPop[0][1]
print("Avg score was: " + str(oldAverage))
input4 = input("Continue? ")
input5 = input("Save Generation to File (Y/N) ")
if(input5.upper() == "Y"):
    with open('saved_gen.json', 'w') as file:
        json.dump(oldPop, file)

for i in range(1000):
    oldPop, sum2,newBest = breeding_process(oldPop)
    print("")
    print("Generation " + str(i+1) + " saw an average change of " + str(((sum2/POPULATION_SIZE)/oldAverage-1) * 100) + "%" + " since Generation " + str(i))
    print("Generation " + str(i+1) + "'s best score was " + str(((newBest/oldBest)-1) * 100) + "%" + " different from Generation " + str(i))
    print("")
    oldBest = newBest
    oldAverage = sum2/POPULATION_SIZE
    #print("Generation " + str(i+1))
    input5 = input("Save Generation to File (Y/N) ")
    if(input5 == "Y"):
        with open('saved_gen.json', 'w') as file:
            json.dump(oldPop, file)
    input3 = input("Continue? (Y/N) ")
    if(input3 == "N"):
        break


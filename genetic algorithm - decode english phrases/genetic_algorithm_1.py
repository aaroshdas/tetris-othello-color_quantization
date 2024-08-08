from math import log
from random import shuffle, sample, random
#sample var = sample(max num/list, number of things to choose)
stringDict = {}
with open("ngrams.txt") as f:
    for line in f:
        val = (line.strip()).upper()
        splitList = val.split()
        if(len(splitList[0]) == 3):
            stringDict[splitList[0]] = log(int(splitList[1]), 2)


#**** GLOBAL VARS*************

message = "XMTP CGPQR BWEKNJB GQ OTGRB EL BEQX BWEKNJB, G RFGLI.  GR GQ BEQX ABSETQB RFGQ QBLRBLSB TQBQ EJJ RBL KMQR SMKKML VMPYQ GL BLDJGQF:  'G FEUB RM AB E DMMY QRTYBLR GL RFER SJEQQ GL RFB PMMK MC RFER RBESFBP.'"
#message = "PF HACYHTTRQ VF N PBYYRPGVBA BS SERR YRNEAVAT NPGVIVGVRF GUNG GRNPU PBZCHGRE FPVRAPR GUEBHTU RATNTVAT TNZRF NAQ CHMMYRF GUNG HFR PNEQF, FGEVAT, PENLBAF NAQ YBGF BS EHAAVAT NEBHAQ. JR BEVTVANYYL QRIRYBCRQ GUVF FB GUNG LBHAT FGHQRAGF PBHYQ QVIR URNQ-SVEFG VAGB PBZCHGRE FPVRAPR, RKCREVRAPVAT GUR XVAQF BS DHRFGVBAF NAQ PUNYYRATRF GUNG PBZCHGRE FPVRAGVFGF RKCREVRAPR, OHG JVGUBHG UNIVAT GB YRNEA CEBTENZZVAT SVEFG.  GUR PBYYRPGVBA JNF BEVTVANYYL VAGRAQRQ NF N ERFBHEPR SBE BHGERNPU NAQ RKGRAFVBA, OHG JVGU GUR NQBCGVBA BS PBZCHGVAT NAQ PBZCHGNGVBANY GUVAXVAT VAGB ZNAL PYNFFEBBZF NEBHAQ GUR JBEYQ, VG VF ABJ JVQRYL HFRQ SBE GRNPUVAT. GUR ZNGREVNY UNF ORRA HFRQ VA ZNAL PBAGRKGF BHGFVQR GUR PYNFFEBBZ NF JRYY, VAPYHQVAT FPVRAPR FUBJF, GNYXF SBE FRAVBE PVGVMRAF, NAQ FCRPVNY RIRAGF.  GUNAXF GB TRAREBHF FCBAFBEFUVCF JR UNIR ORRA NOYR GB PERNGR NFFBPVNGRQ ERFBHEPRF FHPU NF GUR IVQRBF, JUVPU NER VAGRAQRQ GB URYC GRNPUREF FRR UBJ GUR NPGVIVGVRF JBEX (CYRNFR QBA’G FUBJ GURZ GB LBHE PYNFFRF – YRG GURZ RKCREVRAPR GUR NPGVIVGVRF GURZFRYIRF!). NYY BS GUR NPGVIVGVRF GUNG JR CEBIVQR NER BCRA FBHEPR – GURL NER ERYRNFRQ HAQRE N PERNGVIR PBZZBAF NGGEVOHGVBA-FUNERNYVXR YVPRAPR, FB LBH PNA PBCL, FUNER NAQ ZBQVSL GUR ZNGREVNY.  SBE NA RKCYNANGVBA BA GUR PBAARPGVBAF ORGJRRA PF HACYHTTRQ NAQ PBZCHGNGVBANY GUVAXVAT FXVYYF, FRR BHE PBZCHGNGVBANY GUVAXVAT NAQ PF HACYHTTRQ CNTR.  GB IVRJ GUR GRNZ BS PBAGEVOHGBEF JUB JBEX BA GUVF CEBWRPG, FRR BHE CRBCYR CNTR.  SBE QRGNVYF BA UBJ GB PBAGNPG HF, FRR BHE PBAGNPG HF CNTR.  SBE ZBER VASBEZNGVBA NOBHG GUR CEVAPVCYRF ORUVAQ PF HACYHTTRQ, FRR BHE CEVAPVCYRF CNTR."



population_size = 500
num_clones = 1
tournament_size = 20
tournament_win_probability = 0.75
crossover_locations = 5
mutation_rate = 0.8

run_time = 200



alphabetByFrequency = "ETAOINSRHLDCUMFPGWYBVKXJQZ"

def get_new_random_population(size):
    populationSet = set()
    while len(populationSet) < size:
        newAlpha = list(alphabetByFrequency)
        shuffle(newAlpha)
        populationSet.add(''.join(newAlpha))
    population_list = []
    for cipher in populationSet:
        population_list.append((cipher, score(cipher)))
    return sorted(population_list, key = lambda x:-1*x[1])

def selection_process(population):
    popGroup =  sample(population, tournament_size*2)

    tournament1 = sorted(popGroup[0:tournament_size], key = lambda x:-1*x[1])
    tournament2 = sorted(popGroup[tournament_size:len(popGroup)], key = lambda x:-1*x[1])
    parent1 = ""
    i = 0
    while parent1 == "":
        if(random() < tournament_win_probability):
            parent1 = tournament1[i][0]
        i+=1
    parent2 = ""
    k = 0
    while parent2 == "":
        if(random() < tournament_win_probability):
            parent2 = tournament2[k][0]
        k+=1
    return parent1, parent2
    
def breeding_process(old_population):
    newPopulation = []
    for clone in range(num_clones):
        newPopulation.append(old_population[clone])
    while len(newPopulation) <= population_size:
        child = [None]*26
        p1, p2 = selection_process(old_population)
        #p1
        indexs = sample(range(26), crossover_locations)
        for i in indexs:
            child[i] = p1[i]
        #p2:
        for k in range(len(child)):
            if(child[k] == None):
                for newLetter in p2:
                    if(newLetter not in child):
                        child[k] = newLetter
                        break
        if(random() < mutation_rate):
            i1, i2 = sample(range(26), 2)
            child[i1], child[i2] = child[i2], child[i1]
        strChild = ''.join(child)
        if((strChild, score(strChild)) not in newPopulation):
            newPopulation.append((strChild, score(strChild)))
    newPopulation = sorted(newPopulation, key = lambda x:-1*x[1])
    print(substitution_decode(message, newPopulation[0][0]))
    print(newPopulation[0][1])
    print("")

    return newPopulation
            


def substitution_decode(message, codebet):
    codebetDict = {}
    for i in range(len(codebet)):
        codebetDict[codebet[i]] = alphabetByFrequency[i]
    newMessage = ""
    for i in message.upper():
        if(i in alphabetByFrequency):
            newMessage += codebetDict[i]
        else:
            newMessage += i
    return newMessage

def score(codebet):
    newMessage = substitution_decode(message, codebet)
    totalScore = 0
    for i in range(len(newMessage)-2):
        if(newMessage[i:i+3] in stringDict):
            totalScore += stringDict[newMessage[i:i+3]]
    return totalScore



newPop = get_new_random_population(500)
for run in range(run_time):
    print(run)
    newPop = breeding_process(newPop)
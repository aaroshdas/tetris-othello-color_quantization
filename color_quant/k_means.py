from PIL import Image
from random import sample, choice, choices
img = Image.open("puppy.jpg") # Just put the local filename in quotes.
pix = img.load() 
pix[2,5] = (255, 255, 255) 
img.save("my_image.png") 
def create_image_bad_way():
    for x in range(img.size[0]):
        for y in range(img.size[1]):
            newList = [0, 0, 0]
            for i in range(len(pix[x, y])):
                if(pix[x,y][i] > 127):
                    newList[i] = 256
            pix[x, y] = tuple(newList)
    img.save("bad_output.png")

k = 8 # NUM OF COLORS

COLOR_DICT = {}
for x in range(img.size[0]):
    for y in range(img.size[1]):
        if(pix[x,y] in COLOR_DICT):
            COLOR_DICT[pix[x,y]] = COLOR_DICT[pix[x,y]] + 1
        else:
            COLOR_DICT[pix[x,y]] = 1
KMEANS_DICT = {}


def sort_to_means(means):
    for color in COLOR_DICT:
        lowestDiff = 10000000000
        bestMean = 0
        for mean in means:
            diff = 0
            for i in range(3):
                diff += (color[i] - mean[i])**2
            if(diff < lowestDiff):
                lowestDiff = diff
                bestMean = mean
        KMEANS_DICT[bestMean].append(color)
def make_new_mean():
    newDict = {}
    for mean in KMEANS_DICT:
        r = 0
        g = 0
        b = 0
        totalItems = 0
        for item in KMEANS_DICT[mean]:
            totalItems += COLOR_DICT[item]
            r += item[0]* COLOR_DICT[item]
            g += item[1]* COLOR_DICT[item]
            b += item[2]* COLOR_DICT[item]
        newMean = ((r/totalItems, g/totalItems, b/totalItems))
        newDict[newMean] = []
    return newDict
            
def k_means_plus():
    means = []
    newK = choice(list(COLOR_DICT.keys()))
    means.append(newK)
    while len(means) < k:
        colors = []
        weights = []
        for color in COLOR_DICT:
            if color not in means:
                lowestDiff = 10000000
                for m in means:
                    diff = 0
                    for i in range(3):
                        diff += (color[i] - m[i])**2
                    if(diff < lowestDiff):
                        lowestDiff = diff
            colors.append(color)
            weights.append(lowestDiff)
        means.append(choices(colors, weights = weights, k = 1)[0])
    return means

print(k_means_plus())
    
# newList = sample(list(COLOR_DICT.keys()), k)
# for i in newList:
#     KMEANS_DICT[i] = []


for i in k_means_plus():
    KMEANS_DICT[i] = []
#when making new means, weight them check color dict for how many of each color their are.
m = 0
while True:
    sort_to_means(list(KMEANS_DICT.keys()))
    newDict = make_new_mean()
    print(m)
    m+= 1
    if(list(newDict.keys()) == list(KMEANS_DICT.keys())):
        break
    else:
        KMEANS_DICT = newDict

print("K Means done replacing pixels now ")
sort_to_means(list(KMEANS_DICT.keys()))
for x in range(img.size[0]):
    for y in range(img.size[1]):
        lowestDiff = 1000000
        bestMean = 0
        for mean in KMEANS_DICT:
            diff = 0
            for i in range(3):
                diff += (pix[x, y][i] - mean[i])**2
            if(diff < lowestDiff):
                lowestDiff = diff
                bestMean = mean
        pix[x,y] = (int(bestMean[0]), int(bestMean[1]), int(bestMean[2]))
print("Done. check my good_output.png")
img.save("good_output.png")




        
    

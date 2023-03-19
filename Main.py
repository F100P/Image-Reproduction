# Python program to read
# image using PIL module
 
# importing PIL
from PIL import Image,ImageStat
from rgb2lab import *
import glob
import math

def compareLABs(lab1,lab2):
  
    
    deltaE = math.sqrt((lab1[0]-lab2[0])**2 + (lab1[1]-lab2[1])**2 + (lab1[2]-lab2[2])**2)
    
    return deltaE

def buildDB():
    result = []
    for filename in glob.glob('pokemon/*.png'): #assuming gif
        
        img=Image.open(filename).convert('RGB')
        color = ImageStat.Stat(img).mean
        #converts rgb 2 lab, later used to compare to mean of other images in database 
        lab = rgb2lab(color)
        result.append((img,lab))
    return result 


# Read image
database = buildDB()
print(database[0])
img = Image.open('test.jpg').convert('RGB')
r,g,b = img.split()
print(img.size[0])
# Output Images
width = img.size[0]
height = img.size[1]

tileSize= 1
x=0
y=0
newX = 0
newY = 0
#give a frame for the reconstruction to be pasted into, make laerger later 
newImg = Image.new('RGB',(width*20, height*20), (250,250,250))
while y+tileSize< height:
    while x+tileSize<width:
        current = img.crop((x,y,x+tileSize,y+tileSize))

        #extract the mena color of fthe region
        color = ImageStat.Stat(current).mean
        #converts rgb 2 lab, later used to compare to mean of other images in database 
        lab = rgb2lab(color)
        
        minDist = 100
        winner = database[0][0]
        for elem in database:
            deltaE = compareLABs(lab,elem[1])
            if  deltaE < minDist:
                minDist =deltaE
                winner = elem[0]
                
        winner = winner.resize((20,20))
        #paste a full square of color from the mean value. just for testing 
        newImg.paste((winner),(newX*winner.size[0],newY*winner.size[1]))
        newX = newX+1
        
        #newImg.paste(current,(x,y))
        #print(ImageStat.Stat(current).mean)
        x = x+tileSize
    y = y+tileSize 
    newY = newY+1
    x=0
    newX = 0
    

newImg.save("result.jpg")

# Python program to read
# image using PIL module
 
# importing PIL
from PIL import Image,ImageStat
from rgb2lab import *
import glob
import math
from tqdm import tqdm  
from instaLoader import * 



#for i in progressbar(range(15), "Computing: ", 40):

#Calculates Delta E between two points in the LAB color space
def compareLABs(lab1,lab2):
    deltaE = math.sqrt((lab1[0]-lab2[0])**2 + (lab1[1]-lab2[1])**2 + (lab1[2]-lab2[2])**2)
    return deltaE

#Creates an array containing all images in choosen Directory and corresponding LAB values in a tuple
def buildDB():
    result = []
    for filename in glob.glob('pokemon/*.png'): #assuming PNG
        
        img=Image.open(filename).convert('RGB')
        color = ImageStat.Stat(img).mean
        #converts rgb 2 lab, later used to compare to mean of other images in database 
        lab = rgb2lab(color)
        result.append((img,lab))
    return result 

def buildDBcustomDirectory(directory,filetype):
    result = []
    for filename in glob.glob(directory+'/*.'+filetype): #assuming PNG
        
        img=Image.open(filename).convert('RGB')
        color = ImageStat.Stat(img).mean
        #converts rgb 2 lab, later used to compare to mean of other images in database 
        lab = rgb2lab(color)
        result.append((img,lab))
    return result 

#Options
username = "timmyllyla" # will get overwritten
tileSize= 2
repImgSize = 75

while True:
    print("Please input a username")
    username = input("")
    print("is " + username +" correct? ")
    print("yes/no")
    ans = input("")
    if ans == "yes":
        break

    

#init instagramscrape
scrape = GetInstagramProfile()
scrape.download_users_profile_picture(username)
scrape.download_users_posts_with_periods(username)
#find the profile pic in all the files...
for file in glob.glob(username+'/*profile_pic.jpg'):
    print(file)
grabProfile = Image.open(file).convert('RGB')
grabProfile.show()

#build reproduction DB using scraped images
database = buildDBcustomDirectory(username,"jpg")

# Read image
#database = buildDB()
#print(database[0])
#img = Image.open('August.png').convert('RGB')
img = grabProfile
# Output Images
width = img.size[0]
height = img.size[1]


x=0
y=0
newX = 0
newY = 0

#give a frame for the reconstruction to be pasted into, make laerger later 
newImg = Image.new('RGB',(int((width/tileSize)*repImgSize), int((height/tileSize)*repImgSize)), (250,250,250))
pbar = tqdm(desc="Constructing Image", total=height-1)
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
                    
        winner = winner.resize((repImgSize,repImgSize))
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
    pbar.update(tileSize)
    

newImg.save("InstagramProfileTim.jpg")
newImg.show()

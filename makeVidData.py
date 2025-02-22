#tool to generate the ImageData.bin and FlagData.bin from Data/rickRoll.gif
#Gif is compressed to 16 collor palette based on the color palette of Data/16bitTest.png

from PIL import Image 
import numpy as np

#https://github.com/hbldh/hitherdither
import hitherdither as Hdith

#https://github.com/DorkmasterFlek/python-nlzss
import nlzss

Width  = 160 #20 tiles
Height = 160 #20 tiles

# Get palette info from 16bitTest.png
palt16bit = Image.open("Data/16bitTest.png")
palette1 = palt16bit.getpalette()
palette = np.array(palette1).reshape(16,3)


#Returns the squared difference between two colors, mapped to 0.0<=x<=1.0
def colorDist(c1,c2):
    return ((c1[0]-c2[0])**2+(c1[1]-c2[1])**2+(c1[2]-c2[2])**2)/195075

#Claculate the sum of colorDist of each pixel in a tile, val 0<=x<=64 
#(returns 0 iff tile1 == tile2) 
def TileDist(tile1,tile2):
    dist = 0
    for i in range(len(tile1)):
        dist += colorDist(palette[tile1[i]],palette[tile2[i]])
    return dist

#Convert from 8x8 numpy array into a 64 tuple of ints
def cleanTile(tile):
    t = []
    for row in tile:
        for i in row:
            t.append(int(i))
    return tuple(t)

#GBA Hardware tile size is 8x8 pixel tiles
TILESIZE = 8 
#Split frame into individual 8x8 tiles
def chunks(data):
    data = data.reshape((Height,Width))
    tiles = []
    for Tx in range(0,Height,TILESIZE):
        for Ty in range(0,Width,TILESIZE):
            t = data[Tx:Tx+TILESIZE,Ty:Ty+TILESIZE]
            tiles.append(cleanTile(t))
    return tiles

def getFrames(img):
    data = []
    Frames = []
    for i in range(img.n_frames):
        img.seek(i)
        frame = img.resize((Width,Height),Image.Resampling.NEAREST)
        frame = frame.convert("RGB").quantize(palette=palt16bit,dither=Image.Dither.NONE).convert("RGB")
        frame = Hdith.ordered.bayer.bayer_dithering(frame,Hdith.palette.Palette(palette),[256/4, 256/4, 256/4],order=4)
        #frame.convert("RGB").save(f"Out/roll/rick{i}.png")
        tiles = chunks(np.array(frame))
        data.append(tiles)
    oldf = [[0]*64]*(len(data[0]))
    tileData=[]
    flagData=[]
    for f in data:
        for i in range(len(f)):
            if TileDist(f[i],oldf[i])>0.015:
                tileData.extend(f[i])
                flagData.append(1)
                continue
            flagData.append(0)
        oldf = f
    byteData = []
    flagBytes=[]
    for i in range(0,len(tileData),2):
        byteData.append((tileData[i+1]<<4)+tileData[i])
    for i in range(0,len(flagData),8):
        b=0
        for c in range(8):
            b=b<<1
            b+=flagData[i+c]
            
        flagBytes.append(b)
    with open("Data/FlagData.bin","bw") as f:
        f.write(bytes(flagBytes))
    with open("Data/ImageData_raw.bin","bw") as f:
        print(f"uncompressed ImageData len:{hex(len(byteData))}")
        f.write(bytes(byteData))



    

gif = Image.open("Data/rickRoll.gif")

Frames = getFrames(gif)

nlzss.encode_file('./Data/ImageData_raw.bin','./Data/ImageData.bin')

with open("Data/ImageData.bin","br") as f:
    l = len(f.read())

print(f"Compressed Size:{int(l/4096)+1} sectors")
print(f"VidDataSize={hex(l)}")
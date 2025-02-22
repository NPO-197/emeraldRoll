import Savefileedit as SaveEdit

#Need a "Fresh" save file, one that was newly created from a wiped copy of emerald, 
#and has only been saved ONCE, as subsuqent saves will mess with the order of the save sectors...
with open("Data/FreshSave.sav","br+") as f:
    bindata = bytearray(f.read())

sectors = []
for i in range(32):
    sectors.append(SaveEdit.SaveSector(bindata[i*0x1000:(i+1)*0x1000]))

Slot2Start = 0
sect1      = 16
BoxStart   = 20
BoxSlide   = 26
BoxPayload = 27
HOF_1 = 28


#Overwrite the Object Event associated with the main character.
#Which will cause the game to execute a callback associated with a gitched object event,
#leading to a random jump somewhere in BOX12 Data (in wRAM)
#https://e-sh4rk.github.io/ACE3/emerald/advanced/improved-ace-env/#persistence
sectors[sect1].data[0x0A36]=0x6E 


# Overwrite second half of BOX12 Data with bootstrap code that will copy 
# the payload from FLASH memory into IWRAM and then jump to it
with open("build/bootstrap.bin","br") as f:
    bootstrapData = bytes(f.read())
i =0
for u8 in bootstrapData:
    sectors[BoxPayload].data[i] = u8
    i+=1

# Overwite the first sector of storage with our payload
with open("build/payload.bin","br") as f:
    payloadData = bytes(f.read())
assert(len(payloadData)<3968)
i = 0
for u8 in payloadData:
    sectors[BoxStart].data[i]= u8
    i+=1

# Overwrite the next 5 sectors of storage with the start of compressed vidData
# The rest get written to the first 12 sectors of the (unused) "backup" save data.
with open("Data/ImageData.bin","br") as f:
    vidData = bytes(f.read())

writtenBytes = 0

for s in range(1,6):
    for i in range(3968):
        sectors[BoxStart+s].data[i]=vidData[writtenBytes]
        writtenBytes+=1



for s in range(14):
    for i in range(0x1000):
        sectors[Slot2Start+s].data[i]=vidData[writtenBytes]
        writtenBytes+=1
        if writtenBytes==len(vidData):
            break
    if writtenBytes==len(vidData):
        break


# Overwrite (unused) Hall of Fame Data, Trainer Hill data, and recorded battle data with musicData
with open("Data/musicData.bin","br") as f:
    musicData = bytes(f.read())

assert(len(musicData)<0x4000)
writtenBytes = 0
for s in range(HOF_1,32):
    for i in range(0x1000):
        sectors[s].data[i] = musicData[writtenBytes]
        writtenBytes+=1
        if writtenBytes==len(musicData):
            break
    if writtenBytes==len(musicData):
        break



# Update checksums for save sectors that are signed, and combine all sectors into a new sav file
newSave = []
for sect in sectors:
    if sect.checkIsSigned():
        sect.updateChecksum()
    newSave.extend(sect.data)

with open("Out/EmeraldRoll.sav","bw") as f:
    f.write(bytearray(newSave))

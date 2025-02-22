#python script to help edit pokemon emerald save file
#written by NPO-197

#https://github.com/pret/pokeemerald/blob/master/include/save.h

SECTOR_TOTAL_SIZE = 0x1000
SECTOR_DATA_SIZE = 3968
SECTOR_SIGNATURE = 0x8012025
SIGNATURE = [0x25,0x20,0x01,0x08]

sectorIDs={
     0:"Slot1_SaveBlock2",
     1:"Slot1_SaveBlock1_Start",
     2:"Slot1_SaveBlock1_2",
     3:"Slot1_SaveBlock1_3",
     4:"Slot1_SaveBlock1_END",
     5:"Slot1_PKMNStorage1_Start",
     6:"Slot1_PKMNStorage1_2",
     7:"Slot1_PKMNStorage1_3",
     8:"Slot1_PKMNStorage1_4",
     9:"Slot1_PKMNStorage1_5",
    10:"Slot1_PKMNStorage1_6",
    11:"Slot1_PKMNStorage1_7",
    12:"Slot1_PKMNStorage1_8",
    13:"Slot1_PKMNStorage1_End",
    14:"Slot2_SaveBlock2",
    15:"Slot2_SaveBlock1_Start",
    16:"Slot2_SaveBlock1_2",
    17:"Slot2_SaveBlock1_3",
    18:"Slot2_SaveBlock1_END",
    19:"Slot2_PKMNStorage1_Start",
    20:"Slot2_PKMNStorage1_2",
    21:"Slot2_PKMNStorage1_3",
    22:"Slot2_PKMNStorage1_4",
    23:"Slot2_PKMNStorage1_5",
    24:"Slot2_PKMNStorage1_6",
    25:"Slot2_PKMNStorage1_7",
    26:"Slot2_PKMNStorage1_8",
    27:"Slot2_PKMNStorage1_End",
    28:"HOF_1",
    29:"HOF_2",
    30:"TrainerHill",
    31:"RecordedBattle"
}

def IDtoString(x):
    if x in sectorIDs:
        return sectorIDs[x]
    return "N/A"

#https://github.com/pret/pokeemerald/blob/master/src/save.c#L675
def checksum(data):
    checksum = 0
    for i in range(0,len(data)-3,4):
        checksum+=data[i]+(data[i+1]<<8)+(data[i+2]<<16)+(data[i+3]<<24)
    return ((checksum>>16)+checksum)&0x0000ffff

class SaveSector:
    def __init__(self,data):
        assert(len(data)==SECTOR_TOTAL_SIZE)
        self.data = data
        return

    def calcCheckSum(self):
        checksum = 0
        for i in range(0,SECTOR_DATA_SIZE-3,4):
            checksum+=self.data[i]+(self.data[i+1]<<8)+(self.data[i+2]<<16)+(self.data[i+3]<<24)
        return ((checksum>>16)+checksum)&0x0000ffff

    def getID(self):
        return self.data[-12]

    def getCurCheckSum(self):
        return (self.data[-9]<<8)+self.data[-10]
    
    def checkIsSigned(self):
        sig = self.data[-8:-4]
        n=[]
        for i in sig:
            n.append(i)
        return n == SIGNATURE
    def getSaveCounter(self):
        return (self.data[-1]<<24)+(self.data[-2]<<16)+(self.data[-3]<<8)+self.data[-4]
    
    def updateChecksum(self):
        chk = self.calcCheckSum()
        high =(chk &0xff00)>>8
        low = chk &0xff
        self.data[-9]=high
        self.data[-10]=low
        return


if __name__ == "__main__":
    with open("Data/FreshSave.sav","br+") as f:
        bindata = bytearray(f.read())

    sectors = []
    for i in range(32):
        sectors.append(SaveSector(bindata[i*0x1000:(i+1)*0x1000]))

    for sect in sectors:
        print(IDtoString(sect.getID()))
        print(f"SaveCount:{sect.getSaveCounter()}")
        print(f"curCHeckSum:{hex(sect.getCurCheckSum())}")
        print(f"calCheckSum:{hex(sect.calcCheckSum())}")
        print("")


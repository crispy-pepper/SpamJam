# %%
import cv2
import mediapipe as mp
import numpy as np
from matplotlib import pyplot as plt
import mediapipe as mp
from mediapipe.framework.formats import landmark_pb2
import math

from mediapipe.tasks import python
import pygame as pg
from mediapipe.tasks.python import vision
import random
import time

# %%
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()

pg.init()
collect = pg.mixer.Sound('C:\\Computer\\000JamHacks\\assets\\sounds\\collect.wav')
collect.set_volume(0.2)

# %%
w =  1280
h = 720


# %%
#functions
def drawline(layer,a,b,colour,width):
    cv2.line(layer, (int(a.x*w), int(a.y*h)), (int(b.x*w), int(b.y*h)), colour, width)

def incir(c,xc,yc,r):
    return (c.x*w-xc)**2 + (c.y*h-yc)**2 <= r**2

def allincir(l,x,y,r):
    for h in l:
        if not incir(h,x,y,r):
            return False
    
    return True

def drawdeflines():
    global imgPlayer,eyel,moul,eyer,mour,lshou,rshou,lelb,relb,pinl,lwrist,pinr,rwrist,thur,thul,indr,indl,nose
    """drawline(imgPlayer,eyel,eyer,(0,255,0),1)
    drawline(imgPlayer,moul,mour,(0,255,0),1)
    drawline(imgPlayer,eyel,moul,(0,255,0),1)
    drawline(imgPlayer,eyer,mour,(0,255,0),1)"""

    drawline(imgPlayer,lshou,rshou,(0,0,0),2)
    drawline(imgPlayer,lelb,lshou,(0,0,0),2)
    drawline(imgPlayer,relb,rshou,(0,0,0),2)
    drawline(imgPlayer,lelb,lwrist,(0,0,0),2)
    drawline(imgPlayer,relb,rwrist,(0,0,0),2)

    #drawline(imgPlayer,pinl,lwrist,(0,0,255),1)
    #drawline(imgPlayer,pinr,rwrist,(0,0,255),1)
    #drawline(imgPlayer,thul,lwrist,(0,0,255),1)
    #drawline(imgPlayer,thur,rwrist,(0,0,255),1)
    #drawline(imgPlayer,indl,lwrist,(0,0,255),1)
    #drawline(imgPlayer,indr,rwrist,(0,0,255),1)

    cv2.circle(imgPlayer, (int(nose.x*w),int(nose.y*h)), 7, (255,0,0), cv2.FILLED)
    cv2.circle(imgPlayer, (int(lwrist.x*w),int(lwrist.y*h)), 7, (255,255,0), cv2.FILLED)
    cv2.circle(imgPlayer, (int(rwrist.x*w),int(rwrist.y*h)), 7, (255,0,255), cv2.FILLED)
    cv2.circle(imgPlayer, (int(lshou.x*w),int(lshou.y*h)), 7, (0,255,255), cv2.FILLED)
    cv2.circle(imgPlayer, (int(rshou.x*w),int(rshou.y*h)), 7, (0,255,0), cv2.FILLED)
    cv2.circle(imgPlayer, (int(lelb.x*w),int(lelb.y*h)), 7, (0,0,255), cv2.FILLED)
    cv2.circle(imgPlayer, (int(relb.x*w),int(relb.y*h)), 7, (255,255,255), cv2.FILLED)

# %%
def START(name):
    ttt = [[w//2,100],[w//2,h-100],[200,h//2],[w-100,h//2]]

    cpath = "C:\\Computer\\000JamHacks\\assets"
    global cap,situation,targets,squences,sequnce,imgPlayer,eyel,moul,eyer,mour,lshou,rshou,lelb,relb,pinl,lwrist,pinr,rwrist,thur,thul,indr,indl,nose,targets
    cap = cv2.VideoCapture(0)
    order = ["","walk","scavenge","mix","package"]
    order = ["","mix"]
    situation = False
    targets = []
    sequences = {
        "scavenge":{
            "targets":{
                "nose": [[[random.randint(200,w-100),random.randint(100,h-100)] for x in range(5)] for y in range(3)],
                "lwrist":[[[random.randint(200,w//2),random.randint(100,h-100)] for x in range(2)] for y in range(3)],
                "rwrist":[[[random.randint(w//2,w-100),random.randint(100,h-100)] for x in range(2)] for y in range(3)],
                "lelb":[[[random.randint(200,w//2),random.randint(h//3,h*2//3)] for x in range(2)] for y in range(3)],
                "relb":[[[random.randint(w//2,w-100),random.randint(h//3,h*2//3)] for x in range(2)] for y in range(3)],
                "lshou":[[[random.randint(200,w//2),random.randint(100,h//2)] for x in range(2)] for y in range(3)],
                "rshou":[[[random.randint(w//2,w-100),random.randint(100,h//2)] for x in range(2)] for y in range(3)],
            },
            "name":"scavenge",
            "lines":[],
            "images":[[f"{cpath}\\basket.png",[100,100],[w//2,h//2+30]]],
            "circles":[],
            "rectangles":[],
            "text":[["Fruit picking :PPP",[300,h//2],2]],
            "path":f"{cpath}\\berries",
            "size":(60,60),
            "time":0,
            "starttime":0
        },
        "mix":{
            "targets":{
                "nose":[[[250,250]],[[1030,250]],[[1030,630]],[[250,630]],[],[],[],[],[],[],[],[],[],[],[]],
                "lwrist":[[],[],[],[],[[1030,250]],[[1030,630]],[[250,630]],[[250,250]],[],[],[],[],[],[],[]],
                "rwrist":[[],[],[],[],[],[],[],[],[[250,250]],[[1030,250]],[[1030,630]],[[250,630]],[],[],[]],
                "lelb":[[],[],[],[],[],[],[],[],[],[],[],[],[[250,250],[250,630]],[],[]],
                "relb":[[],[],[],[],[],[],[],[],[],[],[],[],[[1030,250],[1030,630]],[],[]],
                "lshou":[[],[],[],[],[],[],[],[],[],[],[],[],[],[[250,250],[1030,250]],[]],
                "rshou":[[],[],[],[],[],[],[],[],[],[],[],[],[],[],[[250,250],[1030,250]]],
            },
            "name":"mix",
            "lines":[],
            "images":[],
            "circles":[],
            "rectangles":[],
            "text":[["Mash",[250,h//2],3], ["MASH",[550,h//2],3],["Mash",[850,h//2],3]],
            "path":f"{cpath}\\jams",
            "size":(100,100),
            "time":0,
            "starttime":0
        },
        "walk":{
            "targets":{
                "nose":[[random.choice(ttt)] if xx%2 == 1 else [[w//2,h//2]] for xx in range(6)],
                "lwrist":[[],[],[],[],[],[]],
                "rwrist":[[],[],[],[],[],[]],
                "lelb":[[],[],[],[],[],[]],
                "relb":[[],[],[],[],[],[]],
                "lshou":[[],[],[],[],[],[]],
                "rshou":[[],[],[],[],[],[]],
            },
            "name":"walk",
            "lines":[],
            "images":[[f"{cpath}\\search.png",[100,100],[w-300,h//2+30]]],
            "circles":[],
            "rectangles":[],
            "text":[["Searchings for fruits...",[300,h//2],2]],
            "path":f"{cpath}\\jams",
            "size":(50,50),
            "time":0,
            "starttime":0
        },
        "package":{
            "targets":{
                "nose":[[],[],[]],
                "lwrist":[[[w//2-20,h//2]],[[200,h//2],[w-150,h//2],[w//2-20,100],[w//2-20,h-100]],[[200,100],[200,h-100],[w-250,h-100],[w//2-20,h//2],[w-150,100]]],
                "rwrist":[[[w//2+20,h//2]],[[250,h//2],[w-100,h//2],[w//2+20,100],[w//2+20,h-100]],[[250,100],[250,h-100],[w-200,h-100],[w//2+20,h//2],[w-100,100]]],
                "lelb":[[],[],[]],
                "relb":[[],[],[]],
                "lshou":[[],[],[]],
                "rshou":[[],[],[]],
            },
            "name":"walk",
            "lines":[],
            "images":[],
            "circles":[],
            "rectangles":[],
            "text":[],
            "path":f"{cpath}\\jams",
            "size":(75,75),
            "time":0,
            "starttime":0
        }
    }
    #print(sequences["walk"]["targets"])
    #sequences = [[[[250,250],[1030,250]],[[250,630],[1030,630]]],[[[640,350]]]]
    sequence = -1   
    berry = 0 

    while True:
        if cv2.waitKey(1)==ord('q'):
            cv2.destroyWindow("Play Window")
            xp = 0
            cap = None
            return [0,0]
        
        success, img = cap.read()

        img = cv2.resize(img, (w,h))
        img = cv2.flip(img, 1)
        imgPlayer = img
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = pose.process(imgRGB)
        lmp = None
        try:
            lmp = results.pose_landmarks.landmark
        except:
            continue

        eyel = lmp[8]
        eyer = lmp[7]
        moul = lmp[10]
        mour = lmp[9]

        lshou = lmp[12]
        rshou = lmp[11]
        lelb = lmp[14]
        relb = lmp[13]
        lwrist = lmp[16]
        rwrist = lmp[15]

        thul = lmp[22]
        thur = lmp[21]
        pinl = lmp[18]
        pinr = lmp[17]
        indl = lmp[20]
        indr = lmp[19]

        nose = lmp[0]

        parts = {
            "nose":lmp[0],
            "eyel":lmp[8],
            "eyer":lmp[7],
            "moul":lmp[10],
            "mour":lmp[9],

            "lshou":lmp[12],
            "rshou":lmp[11],
            "lelb":lmp[14],
            "relb":lmp[13],
            "lwrist":lmp[16],
            "rwrist":lmp[15],

            "thul":lmp[22],
            "thur":lmp[21],
            "pinl":lmp[18],
            "pinr":lmp[17],
            "indl":lmp[20],
            "indr":lmp[19]
        }
        
        partcoul = {"nose":(255,0,0),"lwrist":(255,255,0),"rwrist":(255,0,255),"lshou":(0,255,255),"rshou":(0,255,0),"lelb":(0,0,255),"relb":(255,255,255)}
        for i,(k,v) in enumerate(partcoul.items()):
            cv2.circle(imgPlayer,(50,i*80+130),30,v,-1)
            cv2.putText(imgPlayer,k.title(),(50,i*80+130),cv2.FONT_HERSHEY_DUPLEX,1,(0,0,0),1)
            

        if not situation:
            del order[0]
            #print(order)
            sequence = 0
            if order == []:
                break
            targets = sequences[order[0]]["targets"].copy()
            sequences[order[0]]["starttime"] = time.time()

            situation = True
            
        if len(targets["nose"][sequence]) == 0 and len(targets["lwrist"][sequence]) == 0 and len(targets["rwrist"][sequence]) == 0 and len(targets["lelb"][sequence]) == 0 and len(targets["relb"][sequence]) == 0 and len(targets["lshou"][sequence]) == 0 and len(targets["rshou"][sequence]) == 0:
            sequence += 1
            if sequence >= len(targets["nose"]) and sequence >= len(targets["lwrist"]) and sequence >= len(targets["rwrist"]) and sequence >= len(targets["lelb"]) and sequence >= len(targets["relb"]) and sequence >= len(targets["lshou"]) and sequence >= len(targets["rshou"]):
                sequences[order[0]]["time"] = time.time()-sequences[order[0]]["starttime"]
                situation = False
                #print("sdjnsdsdvfvfv")
                #print(sequence,"in")
                
                berry += 1
                #sequences["walk"]["targets"] = [[random.choice(ttt)] if xx%2 == 1 else [[w//2,h//2]] for xx in range(6)]
                continue
            #targets = s["targets"][sequence].copy()
            #print(sequence,"out")
           
            continue
        
        s = sequences[order[0]]

        for tt in s["text"]:
            cv2.putText(imgPlayer,tt[0],tt[1],cv2.FONT_HERSHEY_DUPLEX,tt[2],(0,0,0),2)

        for tt in s["images"]:
            pic = cv2.imread(tt[0])
            pic = cv2.resize(pic, tt[1])
            x_offset,y_offset=tt[2]
            imgPlayer[y_offset:y_offset+pic.shape[0], x_offset:x_offset+pic.shape[1]] = pic

        pic = cv2.imread(f"{s['path']}\\{name}.png",-1)
        
        pic = cv2.resize(pic, s["size"])
        for part,coul in partcoul.items():
            if len(targets[part]) > sequence:
                #print("wworking")
                for t in targets[part][sequence]:
                    #print("insideloop")
                    #cv2.circle(imgPlayer, (t[0], t[1]), 150, (255,0,0), cv2.FILLED)
                    x_offset,y_offset = t[0]-s["size"][0],t[1]-s["size"][1]
                    y1, y2 = y_offset, y_offset + pic.shape[0]
                    x1, x2 = x_offset, x_offset + pic.shape[1]
                    #print(pic)
                    alpha_s = pic[:, :, 3] / 255.0
                    alpha_l = 1.0 - alpha_s

                    for c in range(0, 3):
                        try:
                            cv2.circle(imgPlayer,(t[0]-(s["size"][0]//2),t[1]-(s["size"][1]//2)),s["size"][0]//2+5,coul,2)
                            imgPlayer[y1:y2, x1:x2, c] = (alpha_s * pic[:, :, c] +
                                                alpha_l * imgPlayer[y1:y2, x1:x2, c])
                        except:
                            pass
                    #imgPlayer[t[1]:t[1]+pic.shape[0], t[0]:t[0]+pic.shape[1]] = pic
                    if incir(parts[part],t[0]-(s["size"][0]//2),t[1]-(s["size"][1]//2),s["size"][0]):
                        del targets[part][sequence][targets[part][sequence].index(t)]
                        collect.play()

                        #print("in")

            #print("grr",sequence)
        

        
        drawdeflines()

        cv2.putText(imgPlayer, "Stop Watch: "+str(round(time.time()-sequences[order[0]]["starttime"],2)),(50,50),cv2.FONT_HERSHEY_DUPLEX,1,(0,255,0),3)

        cv2.imshow("Play Window", imgPlayer)

    cv2.destroyWindow("Play Window")
    cap = None
    return [189,berry]

# %%

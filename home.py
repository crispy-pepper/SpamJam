import pygame as pg
from pp import START
from data import data,slots,owned
import time

cpath = "C:\\Computer\\000JamHacks\\assets"
pg.init()
pg.font.init()
clock = pg.time.Clock()
w,h =700,700

click = pg.mixer.Sound('C:\\Computer\\000JamHacks\\assets\\sounds\\click.wav')
click.set_volume(0.2)
yell = pg.mixer.Sound('C:\\Computer\\000JamHacks\\assets\\sounds\\yell.wav')
yell.set_volume(0.99)

class Character(object):
    def __init__(self,name,colour):
        self.name = name
        self.level = data["characters"][self.name]["level"]
        self.expbartotal = self.level*100 +400
        self.colour = colour
        self.exp = data["characters"][self.name]["exp"]
        self.start = pg.time.get_ticks()
        self.now = pg.time.get_ticks()

        self.blink = [pg.image.load(f"{cpath}\\jams\\{self.name}1.png"),pg.image.load(f"{cpath}\\jams\\{self.name}2.png")]
        self.b = 0
        self.bar = None

    def get_name(self):
        return self.name
    
    def xpbar(self,x,y):
        self.bar = pg.Rect(x+4,y+4,int(self.exp*152/self.expbartotal),12)
        #bars = [[pg.Rect(x,y,160,20),(252, 222, 212)],[pg.Rect(x+4,y+4,int(self.exp*152/self.expbartotal),12),self.colour]]
        #return bars

    def add_xp(self,xp):
        if self.exp+xp >= self.expbartotal:
            xp = self.exp+xp-self.expbartotal
            self.exp = 0
            self.level += 1
            self.expbartotal += 100
            self.add_xp(xp)

        else:
            self.exp += xp

    def display(self,x,y):
        self.add_xp(0)
        self.now = pg.time.get_ticks()
        heart = pg.image.load(f"{cpath}\\hearts\\{self.name}.png")
        heart = pg.transform.scale(heart, (30, 30))
        if self.now-self.start > 800:
            self.b += 1
            self.start = self.now
        self.xpbar(x+20,y-25)
        r = pg.Rect(x+20,y-25,160,20)
        pg.draw.rect(screen,(252, 222, 212),r)
        pg.draw.rect(screen,self.colour,self.bar)

        self.font = pg.font.SysFont("ebrima",12)
        text = self.font.render(f"{self.exp}/{self.expbartotal}", False, (0,0,0))
        screen.blit(text, text.get_rect(center=(x+100,y-16)))
        screen.blit(heart,(x+5,y-30))

        self.font = pg.font.SysFont("ebrima",17)
        self.font.set_bold(True)
        text = self.font.render(f"LVL. {self.level}", False, (0,0,0))
        screen.blit(text, text.get_rect(center=(x+100,y-50)))

        screen.blit(self.blink[self.b%2],(x,y))

class Button(object):
    def __init__(self,name,x,y,w,h,colour,text,textcolour, font,size):
        self.name = name
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.size = size
        self.rec = pg.Rect(self.x,self.y,self.w,self.h)
        self.colour = colour
        self.font = pg.font.SysFont(font,self.size)
        self.font.set_bold(True)
        self.text = text
        self.tcolour = textcolour
    
    def bounds(self):
        return [[self.x,self.x+self.w],[self.y,self.y+self.h]]

    def set_name(self,name):
        self.text = name
    
    def draw(self):
        pg.draw.rect(screen,self.colour,self.rec)
        text = self.font.render(self.text, False, self.tcolour)
        screen.blit(text, text.get_rect(center=(self.x+self.w//2,self.y+self.h//2)))

        
class Selectable_Button(Button):
    def __init__(self,x,y,w,h,colour):
        self.x = x
        self.y = y
        self.h = h
        self.w = w
        self.rec = pg.Rect(self.x,self.y,self.w,self.h)
        self.colour = colour
        self.selected = False
    
    def select(self):
        self.selected = True
    def unselect(self):
        self.selected = False
    def is_selected(self):
        return self.selected
    def draw(self):
        if self.is_selected():
            pg.draw.rect(screen,(255,0,0),self.rec,2)
        
idletime = 60
# create the display surface object
# of specific dimension..e(X, Y).
screen = pg.display.set_mode((w, h))
pg.display.set_caption('Main')
events = pg.event.get()
run = True

def redrawmain():
    screen.fill((255, 157, 150))
    pg.draw.rect(screen, (252, 201, 197), pg.Rect(250, 200, 200, 270),0,10)
    currcharacter.display(250,250)
    play.draw()
    shop.draw()
    quit.draw()
    slot1.draw()
    slot2.draw()
    slot3.draw()
    slot4.draw()
    slot5.draw()
    instru.draw()
    ber.draw()

    berr = pg.image.load(f"{cpath}\\berries\\{currcharacter.get_name()}.png")
    pg.transform.scale(berr, (30, 30))
    screen.blit(berr,(20,30))


    ffffont = pg.font.SysFont("ebrima",30)
    ffffont.set_bold(True)
    text = ffffont.render(f"Time Left:", False, (0,0,0))
    screen.blit(text, text.get_rect(center=(((w-30-50-20-40-50)+(w-30-50-20))//2+25,590)))

    font = pg.font.SysFont("ebrima",100)
    font.set_bold(True)
    text = font.render(f"Spam", False, (189, 47, 47))
    screen.blit(text, text.get_rect(center=(w//2+50,h//2-300)))
    text = font.render(f"JAM", False, (134,0,255))
    screen.blit(text, text.get_rect(center=(w//2+190,h//2-240)))

    #font = pg.font.SysFont("ebrima",30)
    #font.set_bold(True)
    text = ffffont.render(f"{tl:.2f}", False, (255,0,0))
    screen.blit(text, text.get_rect(center=(((w-30-50-20-40-50)+(w-30-50-20))//2+25,630)))

    pg.display.update()

def redrawshop():
    screen.fill((255, 157, 150))
    
    #quit.draw()
    #instru.draw()
    exit.draw()
    slot1.draw()
    slot2.draw()
    slot3.draw()
    slot4.draw()
    slot5.draw()
    ber.draw()
    mpage.draw()
    lpage.draw()
    berr = pg.image.load(f"{cpath}\\berries\\{currcharacter.get_name()}.png")
    berr = pg.transform.scale(berr, (70, 70))
    screen.blit(berr,(0,10))

    font = pg.font.SysFont("ebrima",17)
    text = font.render(f"{page}/{len(shop_pages)}", False, (0,0,0))
    screen.blit(text, text.get_rect(center=(((w-30-50-20-40-50)+(w-30-50-20))//2+25,150)))

    for k,v in not_owned_slots.items():
        v.draw()

    if page == 1:
        shop_pages[page-1][0].display(30,150)
        shop_pages[page-1][1].display(w-440,150)
        shop_pages[page-1][2].display(30,430)
        shop_pages[page-1][3].display(w-440,430)
    else:
        shop_pages[page-1][0].display(30,150)


    for xxx in butt.values():
        xxx.draw()

    for k,v in not_owned_chars.items():
        if k in page2 and page == 2:
            v.draw()
        elif not(k in page2) and page ==1:
            v.draw()
    
    font = pg.font.SysFont("ebrima",30)
    font.set_bold(True)
    text = font.render(f"Time Left:", False, (0,0,0))
    screen.blit(text, text.get_rect(center=(((w-30-50-20-40-50)+(w-30-50-20))//2+25,590)))

    #font = pg.font.SysFont("ebrima",30)
    #font.set_bold(True)
    tl = idletime-(time.time()-lastplay)
    text = font.render(f"{tl:.2f}", False, (255,0,0))
    screen.blit(text, text.get_rect(center=(((w-30-50-20-40-50)+(w-30-50-20))//2+25,630)))

    pg.display.update()

currcharacter = Character("grape",(134,0,255))
characters = {
    "grape": currcharacter,
    "orange": Character("orange",(255,150,0)),
    "strawberry": Character("strawberry",(221,73,17)),
    "blueberry": Character("blueberry",(20,121,180)),
    "peach": Character("peach",(255,197,0))
}
chars = ["grape","orange","strawberry","blueberry","peach"]
ownedd = [x for x in owned]
butt = {
    "grape": Selectable_Button(30,150,200,200,(0,0,0)),
    "orange": Selectable_Button(w-440,150,200,200,(0,0,0)),
    "blueberry": Selectable_Button(w-440,430,200,200,(0,0,0)),
    "strawberry": Selectable_Button(30,430,200,200,(0,0,0)),
    "peach": Selectable_Button(30,150,200,200,(0,0,0))
}
start = pg.time.get_ticks()

page2 = ["peach"]

shop_pages = [
    [
        characters["grape"],
        characters["orange"],
        characters["strawberry"],
        characters["blueberry"],
    ],
    [
        characters["peach"],
    ]
]

page = 1
berries = data["berries"]

play = Button("play",30,200,180,30,(232, 77, 77),"Play!",(255,255,255),"ebrima",20)
shop = Button("shop",30,260,180,30,(232, 77, 77),"Shop",(255,255,255),"ebrima",20)
instru = Button("instru",30,320,180,30,(232, 77, 77),"How to play",(255,255,255),"ebrima",20)
quit = Button("quit",30,380,180,30,(189, 47, 47),"Save and Quit",(255,255,255),"ebrima",20)
exit = Button("exit",w-30-180,30,180,30,(232, 77, 77),"Exit Shop",(255,255,255),"ebrima",20)

ber = Button("berries",30,30,180,30,(232, 77, 77),f"Berries: {berries}",(255,255,255),"ebrima",20)

slot1 = Button("slot1",w-30-180,200,180,30,(232, 77, 77),"Slot 1",(255,255,255),"ebrima",20)
slot2 = Button("slot2",w-30-180,260,180,30,(232, 77, 77),"Slot 2",(255,255,255),"ebrima",20)
slot3 = Button("slot3",w-30-180,320,180,30,(232, 77, 77),"Slot 3",(255,255,255),"ebrima",20)
slot4 = Button("slot4",w-30-180,380,180,30,(232, 77, 77),"Slot 4",(255,255,255),"ebrima",20)
slot5 = Button("slot5",w-30-180,440,180,30,(232, 77, 77),"Slot 5",(255,255,255),"ebrima",20)
slot1.set_name(currcharacter.name.title())
slot2.set_name("orange".title())
slotts = {
    "slot1":slot1,
    "slot2":slot2,
    "slot3":slot3,
    "slot4":slot4,
    "slot5":slot5,
}

for k,v in slots.items():
    slotts[k].set_name(v)


mpage = Button("mpage",w-30-50-20,140,50,30,(232, 77, 77),">",(255,255,255),"ebrima",20)
lpage = Button("lpage",w-30-50-20-40-50,140,50,30,(232, 77, 77),"<",(255,255,255),"ebrima",20)

not_owned_slots = {
    "slot3":Button("bslot3",w-30-180+50,320,80,30,(19, 138, 51),"Buy: 30",(255,255,255),"ebrima",20),
    "slot4":Button("bslot4",w-30-180+50,380,80,30,(19, 138, 51),"Buy: 30",(255,255,255),"ebrima",20),
    "slot5":Button("bslot5",w-30-180+50,440,80,30,(19, 138, 51),"Buy: 30",(255,255,255),"ebrima",20)
}
not_owned_chars = {
    "strawberry":Button("straw",20,427,100,30,(19, 138, 51),"Buy: 500",(255,255,255),"ebrima",20),
    "blueberry":Button("blue",w-450,427,100,30,(19, 138, 51),"Buy: 350",(255,255,255),"ebrima",20),
    "peach":Button("peach",20,147,100,30,(19, 138, 51),"Buy: 100",(255,255,255),"ebrima",20)
}
tl = 1
main = True

shoop = False
selected = False
lastplay = time.time()

while run:
    clock.tick(60)
    mouse = pg.mouse.get_pos() 
    
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False
            break
        
        
        if tl <= 0:
            s = pg.Surface((w,h))
            s.set_alpha(128)                
            s.fill((0,0,0))           
            screen.blit(s, (0,0))
            ffont = pg.font.SysFont("ebrima", 50)
            text = ffont.render("Loading...", False, (255,255,255))
            screen.blit(text, text.get_rect(center=(w//2,h//2)))
            yell.play()

            exp, berry= START(currcharacter.get_name())
            pg.mixer.pause()
            berries += berry
            currcharacter.add_xp(exp)
            lastplay = time.time()
            ber.set_name(f"Berries: {berries}")
            pg.display.update()
            break

        if event.type == pg.MOUSEBUTTONDOWN:
            click.play()
            if main and play.x <= mouse[0] <=play.x+play.w and play.y <= mouse[1] <=play.y+play.h:
                s = pg.Surface((w,h))
                s.set_alpha(128)                
                s.fill((0,0,0))           
                screen.blit(s, (0,0))
                ffont = pg.font.SysFont("ebrima", 50)
                text = ffont.render("Loading...", False, (255,255,255))
                screen.blit(text, text.get_rect(center=(w//2,h//2)))

                exp, berry= START(currcharacter.get_name())
                berries += berry
                currcharacter.add_xp(exp)
                ber.set_name(f"Berries: {berries}")
                lastplay = time.time()
                pg.display.update()

            
            elif main and slot1.x <= mouse[0] <=slot1.x+slot1.w and slot1.y <= mouse[1] <=slot1.y+slot1.h:
                characters[currcharacter.name] = currcharacter
                currcharacter = characters[slot1.text.lower()]
            elif main and slot2.x <= mouse[0] <=slot2.x+slot2.w and slot2.y <= mouse[1] <=slot2.y+slot2.h:
                characters[currcharacter.name] = currcharacter
                currcharacter = characters[slot2.text.lower()]

            elif main and slot3.text!="Slot 3" and slot3.text!="Set Name -"and slot3.x <= mouse[0] <=slot3.x+slot3.w and slot3.y <= mouse[1] <=slot3.y+slot3.h:
                characters[currcharacter.name] = currcharacter
                currcharacter = characters[slot3.text.lower()]
            elif main and slot4.text!="Slot 4"and slot4.text!="Set Name -"and slot4.x <= mouse[0] <=slot4.x+slot4.w and slot4.y <= mouse[1] <=slot4.y+slot4.h:
                characters[currcharacter.name] = currcharacter
                currcharacter = characters[slot4.text.lower()]
            elif main and slot5.text!="Slot 5"and slot5.text!="Set Name -"and slot5.x <= mouse[0] <=slot5.x+slot5.w and slot5.y <= mouse[1] <=slot5.y+slot5.h:
                characters[currcharacter.name] = currcharacter
                currcharacter = characters[slot5.text.lower()]

            
            
            elif shoop and selected and slot1.x <= mouse[0] <=slot1.x+slot1.w and slot1.y <= mouse[1] <=slot1.y+slot1.h:
                slot1.set_name(selected.title())
            elif shoop and selected and slot2.x <= mouse[0] <=slot2.x+slot2.w and slot2.y <= mouse[1] <=slot2.y+slot2.h:
                slot2.set_name(selected.title())
            elif shoop and slot3.text != "Slot 3" and selected and slot3.x <= mouse[0] <=slot3.x+slot3.w and slot3.y <= mouse[1] <=slot3.y+slot3.h:
                slot3.set_name(selected.title())
            elif shoop and slot4.text != "Slot 4" and selected and slot4.x <= mouse[0] <=slot4.x+slot4.w and slot4.y <= mouse[1] <=slot4.y+slot4.h:
                slot4.set_name(selected.title())
            elif shoop and slot5.text != "Slot 5" and selected and slot5.x <= mouse[0] <=slot5.x+slot5.w and slot5.y <= mouse[1] <=slot5.y+slot5.h:
                slot5.set_name(selected.title())
                
            elif shop.x <= mouse[0] <=shop.x+shop.w and shop.y <= mouse[1] <=shop.y+shop.h:
                main = False
                shoop = True
            elif exit.x <= mouse[0] <=exit.x+exit.w and exit.y <= mouse[1] <=exit.y+exit.h:
                main = True
                shoop = False

            elif shoop and page == 1 and butt["grape"].x <= mouse[0] <=butt["grape"].x+butt["grape"].w and butt["grape"].y <= mouse[1] <=butt["grape"].y+butt["grape"].h:
                if butt["grape"].is_selected():
                    butt["grape"].unselect()
                    selected = False
                else:
                    butt["grape"].select()
                    selected = "grape"
            
            elif shoop and page == 1 and butt["orange"].x <= mouse[0] <=butt["orange"].x+butt["orange"].w and butt["orange"].y <= mouse[1] <=butt["orange"].y+butt["orange"].h:
                if butt["orange"].is_selected():
                    butt["orange"].unselect()
                    selected = False
                else:
                    butt["orange"].select()
                    selected = "orange"
            elif shoop and (not ("strawberry" in not_owned_chars)) and page == 1 and butt["strawberry"].x <= mouse[0] <=butt["strawberry"].x+butt["strawberry"].w and butt["strawberry"].y <= mouse[1] <=butt["strawberry"].y+butt["strawberry"].h:
                if butt["strawberry"].is_selected():
                    butt["strawberry"].unselect()
                    selected = False
                else:
                    butt["strawberry"].select()
                    selected = "strawberry"
            elif shoop and (not ("blueberry" in not_owned_chars)) and page == 1 and butt["blueberry"].x <= mouse[0] <=butt["blueberry"].x+butt["blueberry"].w and butt["blueberry"].y <= mouse[1] <=butt["blueberry"].y+butt["blueberry"].h:
                if butt["blueberry"].is_selected():
                    butt["blueberry"].unselect()
                    selected = False
                else:
                    butt["blueberry"].select()
                    selected = "blueberry"
            elif shoop and (not ("peach" in not_owned_chars)) and page == 2 and butt["peach"].x <= mouse[0] <=butt["peach"].x+butt["peach"].w and butt["peach"].y <= mouse[1] <=butt["peach"].y+butt["peach"].h:
                if butt["peach"].is_selected():
                    butt["peach"].unselect()
                    selected = False
                else:
                    butt["peach"].select()
                    selected = "peach"
            
            if shoop and page == 1 and mpage.x <= mouse[0] <=mpage.x+mpage.w and mpage.y <= mouse[1] <=mpage.y+mpage.h:
                page += 1
            if shoop and page == 2 and lpage.x <= mouse[0] <=lpage.x+lpage.w and lpage.y <= mouse[1] <=lpage.y+lpage.h:
                page -= 1

            temp = not_owned_slots.copy()
            for k,v in  not_owned_slots.items():
                cost = int(v.text.split()[1])
                if shoop and berries>= cost and v.x <= mouse[0] <=v.x+v.w and v.y <= mouse[1] <=v.y+v.h:
                    del temp[k]
                    if k == "slot3":
                        slot3.set_name("Set Name -")
                    if k == "slot4":
                        slot4.set_name("Set Name -")
                    if k == "slot5":
                        slot5.set_name("Set Name -")
                    berries -= cost
                    ber.set_name(f"Berries: {berries}")
            not_owned_slots = temp

            temp = not_owned_chars.copy()
            for k,v in  not_owned_chars.items():
                cost = int(v.text.split()[1])
                #print((page == [1,2][k in page2]))
                #print(page,page2,k,k in page2)
                #print()
                if shoop and (page == [1,2][k in page2]) and berries>= cost and v.x <= mouse[0] <=v.x+v.w and v.y <= mouse[1] <=v.y+v.h:
                    del temp[k]

                    berries -= cost
                    ber.set_name(f"Berries: {berries}")
            not_owned_chars = temp

            if main and quit.x <= mouse[0] <=quit.x+quit.w and quit.y <= mouse[1] <=quit.y+quit.h:
                f = open("data.py", "w")
                f.write(f'''data = {"{"}
    "berries":{berries},
    "characters":{"{"}
''')
                for x in chars:
                    f.write(f'''        "{x}": {"{"}
            "level":{characters[x].level},
            "exp":{characters[x].exp},
        {"},"}
''')
                f.write('''    }
}
''')
                f.write(f'''slots = {"{"}''')
                for k,v in slotts.items():
                    f.write(f'''
    "{k}": "{v.text}",''')
                
                f.write('''
}''')
                f.write("\nowned = "+str(ownedd))
                f.close()
                run = False
                break
                
    if main:
        redrawmain()
    elif shoop:
        redrawshop()
    tl = idletime-(time.time()-lastplay)
    pg.display.update()


pg.quit()
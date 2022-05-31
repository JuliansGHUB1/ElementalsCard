import time

import pygame, random
pygame.init()

##Set the display's width and height
width = 1200
height = 800
screen = pygame.display.set_mode((width, height))

##make a background surface, fill it
background = pygame.surface.Surface((width, height))
background.fill((0, 0, 0))

##The point at which the deck is contained
deck_x = width/2
deck_y = height/2
##Where played cards are stored
slot_holderx = width/2 - 300
slot_holdery = height/2


##we will have 8 cards in our deck
number_of_cards = 8

##Class blueprint for card surface objects
class cardHolder(pygame.sprite.Sprite):
    def __init__(self, posx, posy, order):
        super().__init__()
        self.posx = posx
        self.posy = posy
        self.image = pygame.surface.Surface((width/number_of_cards, height/4))
        self.rect = self.image.get_rect()
        self.rect.topleft = (posx, posy)
        self.in_use = False
        self.pos = order
        self.image.fill((random.randint(0, 100), random.randint(0, 100), random.randint(0, 100)))
    def update(self):
        self.rect.topleft = (self.posx, self.posy)

##datastructures for cardholder objects
array_cardholders = []

group_cardholders = pygame.sprite.Group()


##Method to generate cardHolder objects
def insantiate_CardHolders():

    posx_incrementer = 0
    posy_incrementer = 0

    for i in range(number_of_cards):
        newCardHolder = cardHolder(posx_incrementer,posy_incrementer, i)

        newCardHolder.in_use = False

        array_cardholders.append(newCardHolder)
        group_cardholders.add(newCardHolder)
        print(newCardHolder.posx)
        posx_incrementer = posx_incrementer + width/(number_of_cards)

##Calling of above method
insantiate_CardHolders()


##Card object class
class Card(pygame.sprite.Sprite):
    def __init__(self, cardnumber, name):
        super().__init__()
        ##pos of -1 indicates card is A) played, B) in deck
        self.pos = -1
        self.name = name
        self.in_use = False
        self.played = False
        self.posx = 0
        self.posy = 0
        self.image = pygame.surface.Surface((width/number_of_cards, height/4))
        self.rect = self.image.get_rect()
        self.rect.topleft = (self.posx, self.posy)
        self.font1 = pygame.font.SysFont("Comic Sans", 40)
        self.text_surface = self.font1.render(str(cardnumber), False, (240, 248, 230))
        self.text_surf_holder = pygame.surface.Surface((self.text_surface.get_width(), self.text_surface.get_height()))
        self.image.fill((0, 50, 100))
    def update(self):
        self.rect.topleft = (self.posx, self.posy)
        self.text_surf_holder.blit(self.text_surface, (0, 0))
        self.image.blit(self.text_surf_holder, (0, 0))


    ##These are two methods that I will call within the 4 main methods for card movement

    def changeCardSurfaceState(self, in_use):
        ##I have decided to update the state of the card surface when I move the card
        for i in array_cardholders:
            if i.pos == self.pos:
                i.in_use = in_use

    def remove_previous_inplay(self):
        for i in array_card:
            if i.played == True:
                i.removefromPlay()


    ## 4 main methods for card movement

    def drawfromDeck(self, new_pos):
        ##Method concerned with drawing card from deck and moving it to an empty cardholder. Note, when moving to an empty cardholder, the cardholder's
        ##internal data must be changes as well
        self.pos = new_pos
        self.changeCardSurfaceState(True)
        self.posx = Locations[new_pos]
        self.posy = 0
        self.in_use = True
        self.played = False

    def ChangeCardPos(self,new_pos):
        ##Method that changes the position of the card, as well as changes the state of the card surface's in use field to reflect the moving of the card
        self.changeCardSurfaceState(False)
        self.pos = new_pos
        self.changeCardSurfaceState(True)
        self.posx = Locations[new_pos]
        self.posy = Locations[new_pos]




    def playCard(self):
        self.remove_previous_inplay()
        self.changeCardSurfaceState(False)
        self.pos = -1
        self.posx = slot_holderx
        self.posy = slot_holdery
        self.in_use = True
        self.played = True

    def removefromPlay(self):
        self.pos = -1
        self.posx = deck_x
        self.posy = deck_y
        self.in_use = False
        self.played = False

##Datastructures for card objects
array_card = []
group_card = pygame.sprite.Group()
##method to instantiate card objects
Locations = {}
def setLocations():
    newincrementer = 0
    for i in range(8):
        Locations[i] = newincrementer
        newincrementer = newincrementer + width/number_of_cards
    print(Locations)

setLocations()

def instantiateCardObjects():
    posx_incrementer = 0
    for i in range(20):
        if i >= 8:
            newCardObject = Card(i, "card " + str(i))
            newCardObject.removefromPlay()
            array_card.append(newCardObject)
            group_card.add(newCardObject)
        else:
            newCardObject = Card(i, "card " + str(i))
            newCardObject.drawfromDeck(i)
            array_card.append(newCardObject)
            group_card.add(newCardObject)
            posx_incrementer = posx_incrementer + width/number_of_cards

def Check_Clicked():
    for z in eventList:
        if z.type == pygame.MOUSEBUTTONDOWN:
            return True
last_clicked = 0

def PlayCard():
    global last_clicked
    mouse_pos = pygame.mouse.get_pos()
    for i in array_card:
        ##for each card in the group of cards
        if i.in_use == True:
            ###if the card object is in use(in the deck)
            if i.rect.collidepoint(mouse_pos) and time.time() - last_clicked > 1 and Check_Clicked() == True:
                i.playCard()
                checkCardObjectsInstantiated()
                checkCardHoldersData()
                last_clicked = time.time()





run = True

instantiateCardObjects()

def checkCardObjectsInstantiated():
    for i in array_card:
        print(i.in_use, i.played, i.pos, i.posx, i.posy)
        print("Note to user of method: refer to instantiatite card object methods to gain an understanding of this method")
        print("Notably, while i is in range (0,8) we create card obects that are in_use, the rest up till the range specified are simply cards in the pile")
def checkCardHoldersData():
    for i in array_cardholders:
        print("Following is cardholder data")
        print(i.pos, i.in_use)


while run:
    eventList = pygame.event.get()

    PlayCard()



    group_cardholders.draw(screen)
    group_card.update()
    group_card.draw(screen)
    pygame.display.update()





    ##check all events in evenList

    for event in eventList:
        if event.type == pygame.QUIT:
            run = False





raise SystemExit
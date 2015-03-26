#-------------------------------------------------------------------------------------
#This is an attempt to make a single player game similar to Stock Exchange board game
#Initial attempt was in C++, this is a second attempt by using Python
#
#Author: Abhinav Dhere
#Date of Starting: 25 March 2015
#-------------------------------------------------------------------------------------
import os
import random
import time

class NewGame(object):
    '''
    Intialization functions
    '''
    def __init__(self,name,rounds):
        '''
        Initializes a new game
        '''
        self.name=name
        self.rounds=rounds
        self.priceMap=self.readCompanies()
        os.system('cls')
        print 'Hi '+self.name+'!\n'
        print 'The initial stock prices are: \n'
        self.displayPrices()
        
        
    def readCompanies(self):
        '''
        Reads from file Companies.txt
        Returns dictionary which is map of the companies and their initial prices
        '''
        FILE_PATH="Companies.txt"
        priceMap={}
        companies=open(FILE_PATH,"r")
        for line in companies:
            line=line.strip('\n')
            companyList=line.split(':')
            priceMap[companyList[0]]=float(companyList[1])
        return priceMap

    def displayPrices(self):
        '''
        Prints the stock prices of companies
        '''
        for element in self.priceMap.keys():
            print element+':'+str(self.priceMap[element])+' ',
        print ''

    def roundInit(self):
        '''
        Starts a new round
        '''
        for i in range(self.rounds):
            print 'Round number: '+str(i)
            newRound=NewRound()

class NewRound(NewGame):
    '''
    Starts a new round
    '''
    def __init__(self):
        #self.distribCards()
        pass

    def cardsAvailable(self):
        '''
        Populates a list of available cards
        Returns a tuple containing three lists of cards
        '''
        cardType={}
        windfall=['Cash: +20%','Cash: -20%','Cash: +10%','Cash: -10%','Loan Stock Matured','Debenture','Rights Issue']
        companyCards=game.priceMap.keys()
        cards=windfall+companyCards
        return (cards,windfall,companyCards)

    def generateCards(self):
        '''
        Generates 10 random cards
        Returns dictionary of cards and their value
        '''
        (cards,windfall,companyCards)=self.cardsAvailable()
        cardList={}
        for i in range(10):
            card=random.choice(cards)
            if card in cardList:
                card=card+''
            if card in companyCards:
                value=random.randrange(-3,4)
                cardList[card]=value
            elif card in windfall:
                cardList[card]=''
        return cardList
    
    def distribCards(self):
        cardList=self.generateCards()
        print 'Your cards for this round are:'
        for card in cardList:
            if cardList[card]!='':
                if cardList[card]>0:
                    print card+': +'+str(cardList[card])
                elif cardList[card]<0:
                    print card+': '+str(cardList[card])
            elif cardList[card]=='':
                print card

        
        
    
def menu():
    '''
    Home screen output
    Returns menu option number 
    '''
    os.system('cls') #clears screen
    print "\t\t\tWelcome to the Share Trader PC game!"
    print "\n1.New Game \n2.Help \n3.Exit"
    i=int(raw_input("Select option number: "))
    return i

def createGame():
    '''
    Creates a new instance of a game
    '''
    os.system('cls')
    name=raw_input("Enter your name: ")
    rounds=int(raw_input("Enter num of rounds: "))
    print "Creating a new game against CPU..."
    time.sleep(2)
    game=NewGame(name,rounds)
    return game

run=False
gameNum=1
while run:
    try:
        i=menu()
        if i==1:
            game=createGame()
            game.roundInit()
            gameNum+=1
            raw_input("Press enter to return to menu")
            
        elif i==2:
            os.system('cls')
            help=open("Game Rules.txt","r")
            print help.read()
            raw_input("Press enter to continue")
        elif i==3:
            run=False
    except:
        print 'Invalid Entry'
        time.sleep(2)
game=NewGame('A',2)
r=NewRound()
print r.generateCards()

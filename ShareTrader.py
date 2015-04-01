#------------------------------------------------------------------------------------------------------------------------
#This is an attempt to make a single player game similar to Stock Exchange board game
#Initial attempt was in C++, this is a second attempt by using Python
#
#Author: Abhinav Dhere
#Date of Starting: 25 March 2015
#
#
#License: This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
#         See http://creativecommons.org/licenses/by-nc-sa/4.0/ for details.
#
#------------------------------------------------------------------------------------------------------------------------
import os
import random
import time

class NewUser(object):
    '''
    Holds stats and data about a user
    '''
    def __init__(self,name):
        self.name=name                      #name of player
        self.cash=60000.0                   #cash owned by player
        self.stock={}                       #stock owned by player
        self.investedCash=self.getInvested()#cash invested in stock
    
    def getStock(self,company):
        '''
        Takes a string company as input. Assumes that company is a valid company.
        Returns the amount of stock owned by player in a company
        '''
        try:
            return self.stock[company]
        except KeyError:
            return 0

    def buyStock(self,company,stock):
        '''
        Increments the amount of stock owned in a company by the int stock.
        Decrements cash by amount invested
        Assumes that the string company is a valid company 
        '''
        try:
            if self.cash-stock*game.priceMap[company]<0:
                raise ValueError
            self.cash-=stock*game.priceMap[company]
            if company not in self.stock:
                self.stock[company]=stock
            elif company in self.stock:
                self.stock[company]+=stock
            print str(stock)+' shares bought in '+company
        except ValueError:
            print "Insufficient Funds!"
            return ValueError

    def sellStock(self,company,stock):
        '''
        Decrements the amount of stock owned in a company by the int stock.
        Increments cash by amount invested
        Assumes that the string company is a valid company 
        '''
        try:
            if self.stock[company]-stock<0:
                raise ValueError
            self.stock[company]-=stock
            self.cash+=stock*game.priceMap[company]
            print str(stock)+' shares of '+company+' sold'
        except ValueError:
            print "You have only "+str(self.stock[company])+" shares in "+company+"!"
            raise ValueError
        except KeyError:
            print "You do not own any shares in "+company+"!"
            return ValueError
        
    def getInvested(self):
        '''
        Calculates the total cash invested in all stocks
        '''
        investedCash=0
        for company in self.stock.keys():   #Multiplies the stock in a company by its price and adds all values
            investedCash+=self.stock[company]*game.priceMap[company]
        return investedCash
    
    def getStats(self):
        '''
        Prints the stats of a player at the end of each round
        '''
        print 'Player Stats:'
        print 'Name: '+self.name
        print 'Cash in hand: Rs. '+str(self.cash)
        print 'Cash Invested: Rs. '+str(self.getInvested())
        print 'Total Cash: Rs. '+str(self.cash+self.getInvested())
        
class NewGame(object):
    '''
    Intialization functions for creating a new game
    '''
    def __init__(self,rounds):
        '''
        Initializes a new game
        '''
        self.rounds=rounds                  #no. of rounds to be played
        self.priceMap=self.readCompanies()  #reads initial prices & names of companies into priceMap
        os.system('cls') #clear screen
        print 'Hi '+user.name+'!\n'
        print 'The initial stock prices are: \n'
        self.displayPrices()                #prints the initial prices
        
        
    def readCompanies(self):
        '''
        Reads from file Companies.txt
        Returns dictionary which is mapping of the companies to their initial prices
        '''
        FILE_PATH="Companies.txt"           #file containing names of companies and initial prices
        priceMap={}
        companies=open(FILE_PATH,"r")
        for line in companies:
            line=line.strip('\n')           #strip the newline character
            companyList=line.split(':')     #converts a line in file to list containing name of company & price 
            priceMap[companyList[0]]=float(companyList[1])
        return priceMap

    def displayPrices(self):
        '''
        Prints the stock prices of companies
        '''
        for element in self.priceMap.keys():
            print element+':'+str(self.priceMap[element])+' ',
        print '\n'

    def isValidCompany(self,company):
        '''
        Checks if a string company is a valid company
        Returns a boolean
        '''
        if company in self.priceMap:
            return True
        elif company not in self.priceMap:
            return False
        
    def roundInit(self):
        '''
        Starts a new round
        '''
        for i in range(1,self.rounds+1):    #create new rounds as per self.rounds 
            print '\nRound number: '+str(i)+'\n'
            newRound=NewRound()

class NewRound(NewGame):
    '''
    Starts a new round
    '''
    def __init__(self):
        self.distribCards()                 #distribute cards at start of round
        print "\nTo buy shares type 'Name of Company'(space)'Number of Shares'"
        print "To sell shares type 'Name of Company'(space)'Number of Shares'"
        print "To pass the turn, type 'pass'"
        for turnNum in range(3):
            playTurnUser()

    def cardsAvailable(self):
        '''
        Populates a list of available cards
        Returns a tuple containing three lists of cards
        '''
        cardType={}
        windfall=['Cash: +20%','Cash: -20%','Cash: +10%','Cash: -10%','Loan Stock Matured','Debenture','Rights Issue']
        companyCards=game.priceMap.keys()
        cards=windfall+companyCards         #obtain a list combining both company cards and windfall cards
        return (cards,windfall,companyCards)


    def generateCards(self):
        '''
        Generates 10 random cards
        Returns dictionary of cards and their value
        '''
        (cards,windfall,companyCards)=self.cardsAvailable()
        cardMap={}
        windfallNum=4                       #maximum number of windfall cards allowed
        valRange=range(-4,0)+range(1,5)     #range of values for company cards
        for j in range(10):
            if windfallNum<1:               #conditionals to generate a new card while restricting max num of windfall cards
                card=random.choice(companyCards)
            else:
                card=random.choice(cards)
                
            if card in companyCards:        #conditionals to allot values to company cards and add to dictionary
                if card not in cardMap:     #value is given in form of list to accomodate multiple cards of same company
                    value=[random.choice(valRange)]
                    cardMap[card]=value
                elif card in cardMap:       #appends to list of values if more than one cards of same company
                    cardMap[card].append(random.randrange(-3,4))
                    
            elif card in windfall:          #conditionals to add windfall cards and their frequency to dictionary
                windfallNum-=1
                if  card not in cardMap:
                    cardMap[card]=1         #value of the card is frequency of occurance of the card
                elif card in cardMap:
                    cardMap[card]+=1        #increments frequency is same windfall card multiple times

        return (cardMap,companyCards,windfall)
    
    def distribCards(self):
        '''
        Distributes the cards generated by generateCards function i.e.
        Prints them in a proper way
        '''
        (cardMap,companyCards,windfall)=self.generateCards()
        for card in cardMap:
            if card in companyCards:
                for val in cardMap[card]:
                    if val>0:               #prints card and value with sign prefixed
                        print card+': +'+str(val)
                    elif val<0:
                        print card+': '+str(val)
            elif card in windfall:
                print card+': '+str(cardMap[card])+' cards'

        
class playTurnUser():
    '''
    For a user to play one turn of a round
    '''
    def __init__(self):
        self.parseInput()

    def parseInput(self):
        try:
            inputString=raw_input('>> ')
            inputString=inputString.strip()#remove whitespace from start and end if present
            if inputString=='pass' or inputString=='Pass':
                return None                     #no action needed if pass
            commandList=inputString.split()     #split input string in list of parameters as below
            operation=commandList[0]
            company=commandList[1]
            stock=int(commandList[2])
            if operation=='buy':
                if game.isValidCompany(company):
                    buy=user.buyStock(company,stock)
                    if buy==ValueError:
                        raise ValueError
                else:
                    raise ValueError            #error raised if invalid company
            elif operation=='sell':
                if game.isValidCompany(company):
                    sell=user.sellStock(company,stock)
                    if sell==ValueError:
                        raise ValueError
                else:
                    raise ValueError
            else:
                raise ValueError
        except ValueError:
            print 'Invalid Input'
            return self.parseInput()            #recursion if error encountered
    
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

def createUser():
    '''
    Creates a new instance of a user
    '''
    os.system('cls')
    name=raw_input("Enter your name: ")
    user=NewUser(name)
    return user

def createGame():
    '''
    Creates a new instance of a game
    '''
    rounds=int(raw_input("Enter num of rounds: "))
    print "Creating a new game against CPU..."
    time.sleep(1)#generates a delay of 1 second to let user read the print statement above
    game=NewGame(rounds)
    return game

run=True                                   #run flag used to indicate whether loop should run again
gameNum=1
while run:
    try:
        i=menu()
        if i==1:
            user=createUser()
            game=createGame()
            game.roundInit()
            gameNum+=1
            raw_input("Press enter to return to menu")
            
        elif i==2:
            os.system('cls')
            help=open("Game Rules.txt","r") #reads rules from Game Rules file
            print help.read()
            raw_input("Press enter to continue")
        elif i==3:
            run=False
    except:
        print 'Invalid Entry'
        time.sleep(1)
##user=NewUser('Abhinav')
##game=NewGame(1)

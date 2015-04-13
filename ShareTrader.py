#------------------------------------------------------------------------------------------------------------------------
#This is an attempt to make a single player game similar to Stock Exchange board game.
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
    Holds stats and functions for a user
    '''
    def __init__(self,name):
        self.name=name                      #name of player
        self.cash=100000.0                  #cash owned by player
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
            print str(stock)+' shares worth Rs.'+str(stock*game.priceMap[company])+' bought in '+company+'.',
            print "Cash in Hand: Rs."+str(self.cash)
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
            print str(stock)+' shares worth Rs.'+str(stock*game.priceMap[company])+' in '+company+' sold.',
            print "Cash in Hand: Rs."+str(self.cash)
        except ValueError:
            print "You have only "+str(self.stock[company])+" shares in "+company+"!"
            raise ValueError
        except KeyError:
            print "You do not own any shares in "+company+"!"
            return ValueError

    def specialBuy(self,company,stock):
        '''
        For buying at rate of Rs 1/share in case of Debenture
        '''
        try:
            if self.cash-stock*game.priceMap[company]<0:
                raise ValueError
            self.cash-=stock
            if company not in self.stock:
                self.stock[company]=stock
            elif company in self.stock:
                self.stock[company]+=stock
            print str(stock)+' shares worth Rs.'+str(stock)+' bought in '+company+'.',
            print "Cash in Hand: Rs."+str(self.cash)
        except ValueError:
            print "Insufficient Funds!"
            return ValueError
        
    def getInvested(self):
        '''
        Calculates the total cash invested in all stocks
        '''
        investedCash=0
        for company in self.stock.keys():   #Multiplies the stock in a company by its price and adds all values
            investedCash+=self.stock[company]*game.priceMap[company]
        return investedCash

    def specialSell(self,RIcompany,pastPrices):
        '''
        For selling in case of Rights Issue
        '''
        stock=self.stock[RIcompany]
        self.stock[RIcompany]=0
        self.cash+=stock*pastPrices[RIcompany]
    
    def getStats(self):
        '''
        Prints the stats of a player at the end of each round
        '''
        print 'Player Stats:\n'
        print 'Name: '+self.name
        print 'Cash in hand: Rs. '+str(self.cash)
        print 'Cash Invested: Rs. '+str(self.getInvested())
        print 'Total Cash: Rs. '+str(self.cash+self.getInvested())
        print ''

    def __str__(self):
        return self.name

class CPU():
    '''
    Holds stats and functions for CPU
    '''
    def __init__(self):
        self.name='CPU'
        self.cash=100000.0                  #cash owned by player
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
        if self.cash-stock*game.priceMap[company]<0:
            raise ValueError
        self.cash-=stock*game.priceMap[company]
        if company not in self.stock:
            self.stock[company]=stock
        elif company in self.stock:
            self.stock[company]+=stock

    def sellStock(self,company,stock):
        '''
        Decrements the amount of stock owned in a company by the int stock.
        Increments cash by amount invested
        Assumes that the string company is a valid company 
        '''
        if self.stock[company]-stock<0:
            raise ValueError
        self.stock[company]-=stock
        self.cash+=stock*game.priceMap[company]

    def specialBuy(self,company,stock):
        '''
        For buying at rate of Rs 1/share in case of Debenture
        '''
        if self.cash-stock<0:
            raise ValueError
        self.cash-=stock
        if company not in self.stock:
            self.stock[company]=stock
        elif company in self.stock:
            self.stock[company]+=stock

    def specialSell(self,RIcompany,pastPrices):
        '''
        For selling in case of Rights Issue
        '''
        stock=self.stock[RIcompany]
        self.stock[RIcompany]=0
        self.cash+=stock*pastPrices[RIcompany]
        
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
        print 'Player Stats:\n'
        print 'Cash in hand: Rs. '+str(self.cash)
        print 'Cash Invested: Rs. '+str(self.getInvested())
        print 'Total Cash: Rs. '+str(self.cash+self.getInvested())
        print ''

    def __str__(self):
        return self.name
        
    
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
        dumpLine=companies.readline()
        for line in companies:
            line=line.strip('\n')           #strip the newline character
            companyList=line.split(':')     #converts a line in file to list containing name of company & price 
            priceMap[companyList[0]]=float(companyList[1])
        return priceMap

    def displayPrices(self):
        '''
        Prints the stock prices of companies
        '''
        dictList=sorted(self.priceMap,key=self.priceMap.get)#gives a list of keys sorted by values
        for element in dictList:            #print all companies & prices in ascending order of price
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

    def endGame(self):
        '''
        Conclude a game
        '''
        print '\nAt the end of this game, the user stats are:'
        user.getStats()
        print 'And CPU stats are:'
        cpu.getStats()
        userTotal=user.cash+user.getInvested()
        cpuTotal=cpu.cash+cpu.getInvested()
        if userTotal>cpuTotal:
            print user.name+' wins!'
        elif cpuTotal>userTotal:
            print 'CPU wins!'
        elif cpuTotal==userTotal:
            print 'Its a tie!'
            

class NewRound(NewGame):
    '''
    Starts a new round
    '''
    def __init__(self):
        self.userCreds=self.distribCards()                 #distribute cards at start of round
        print "\nTo buy shares type buy(space)'Name of Company'(space)'Number of Shares'"
        print "To sell shares type sell(space)'Name of Company'(space)'Number of Shares'"
        print "To pass the turn, type 'pass'"
        for userTurnNum in range(3):
            playTurnUser()
        cardMap,companyCards,windfall=self.generateCards()#generate new cards for CPU
        self.cp=playCPU(cardMap,companyCards,windfall)
        endRound(self.userCreds,self.cp)                     #perform calcs for ending round

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
        userCreds=(cardMap,companyCards,windfall)
        for card in cardMap:
            if card in companyCards:
                for val in cardMap[card]:
                    if val>0:               #prints card and value with sign prefixed
                        print card+': +'+str(val)
                    elif val<0:
                        print card+': '+str(val)
            elif card in windfall:
                print card+': '+str(cardMap[card])+' cards'
        return userCreds
        
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

class playCPU(object):
    '''
    For CPU to play one round
    '''
    def __init__(self,cardMap,companyCards,windfall):
        self.cardMap=cardMap
        self.companyCards=companyCards
        self.windfall=windfall
        for i in range(3):
            self.playTurn()

    def sell(self):
        '''
        Makes a decision on which shares to sell and sells them
        '''
        minCard=0
        maxCost=0
        for comp in cpu.stock.keys():       #iterate through all companies for which stock bought
            if cpu.getStock(comp)>maxCost:  #find the stock with highest cost
                maxCost=cpu.getStock(comp)
                avlComp=comp
            if comp in self.cardMap.keys() and sum(self.cardMap[comp])<minCard: #find the stock with lowest prediction
                minCard=self.cardMap[comp]
                CardComp=comp
        if minCard<0:                       #sell if stock may go in negative fluctuation
            cpu.sellStock(CardComp,cpu.getStock(CardComp))
        elif len(cpu.stock.keys())!=0:      #sell if stock is of high cash value
            cpu.sellStock(avlComp,cpu.getStock(avlComp))
        else:
            pass
                
    def invest(self):
        '''
        Makes a decision on which shares to buy and buys them
        '''
        maxValue=0
        compMap=self.cardMap.copy()
        for card in compMap.keys():         #obtain a price Map without Windfall
            if card in self.windfall:
                del compMap[card]
        for comp in compMap.keys():         #iterate to find stock with highest predicted value
            if sum(compMap[comp])>maxValue:
                maxValue=sum(compMap[comp])
                maxComp=comp

        if maxValue>5:                      #means highly profitable stock
            try:
                if game.priceMap[maxComp]>10:
                    cpu.buyStock(maxComp,1000)
                else:
                    cpu.buyStock(maxComp,1500)
            except ValueError:              #exception to handle if cash deficiency
                i=1500
                while cpu.cash<game.priceMap[maxComp]*i:
                    i-=100
                cpu.buyStock(maxComp,i)

        elif maxValue>3 and maxValue<5:     #no of shares bought decreases as maxValue decreases
            try:
                if game.priceMap[maxComp]>10:
                    cpu.buyStock(maxComp,500)
                else:
                    cpu.buyStock(maxComp,750)
            except ValueError:
                i=750
                while cpu.cash<game.priceMap[maxComp]*i:
                    i-=100
                cpu.buyStock(maxComp,i)

        elif maxValue>0 and maxValue<3:
            try:
                if game.priceMap[maxComp]>10:
                    cpu.buyStock(maxComp,300)
                else:
                    cpu.buyStock(maxComp,500)
            except ValueError:
                i=500
                while cpu.cash<game.priceMap[maxComp]*i:
                    i-=50
                cpu.buyStock(maxComp,i)

        elif maxValue<0:                    #pass if no shares will rise
            pass
                
                
    def playTurn(self):
        '''
        play one turn of a round
        '''
        if cpu.cash>0:
            self.invest()
        elif maxValue>0 and cpu.cash<0:
            self.sell()
        else:
            pass

class endRound(object):
    '''
    Performs calculations for ending round
    '''
    def __init__(self,userCreds,cp):
        self.userCreds=userCreds            #creds for user
        self.cp=cp                          #class object for playCPU
        self.fluctuation={}                 #dictionary to hold fluctuations
        self.windUsers={}                   #dictionary to hold windfall cards of users
        self.windCPU={}                     #dictionary to hold windfall cards of cpu
        self.calcUser()
        self.calcCPU()
        self.pastPrices=self.calcFlucs()
        self.Windfall(user)
        self.Windfall(cpu)
        self.giveStats()

    def calcUser(self):
        '''
        Find fluctuations & windfall cards from user
        '''
        for card in self.userCreds[0].keys():
            if card in self.userCreds[1]:
                self.fluctuation[card]=sum(self.userCreds[0][card])
            elif card in self.userCreds[2]:
                for i in range(self.userCreds[0][card]):#build windfall card frequency dictionary
                    self.windUsers[card]=self.windUsers.get(card,0)+1
                    
    def calcCPU(self):
        '''
        Find fluctuations & windfall cards from CPU
        '''
        for Card in self.cp.cardMap.keys():
            if Card in self.cp.companyCards and Card in self.fluctuation.keys():
                self.fluctuation[Card]+=sum(self.cp.cardMap[Card])
            elif Card in self.cp.companyCards and Card not in self.fluctuation.keys():
                self.fluctuation[Card]=sum(self.cp.cardMap[Card])
            elif Card in self.cp.windfall:
                for j in range(self.cp.cardMap[Card]):
                    self.windCPU[Card]=self.windCPU.get(Card,0)+1

    def calcFlucs(self):
        '''
        Calulate the new prices from fluctuations & mutate original Price Map
        Also saves a backup of old prices and returns it.
        '''
        pastPrices=game.priceMap.copy()
        for company in self.fluctuation.keys():
            game.priceMap[company]+=self.fluctuation[company]
        return pastPrices

    def Windfall(self,player):
        '''
        Execute windfall cards
        '''
        for card in self.windUsers.keys():
            for k in range(self.windUsers[card]):
                if card=='Cash: +10%':
                    player.cash+=0.1*player.cash
                    print str(player)+' got Cash +10%'
                elif card=='Cash: -10%':
                    player.cash-=0.1*player.cash
                    print str(player)+' got Cash -10%'
                elif card=='Cash: +20%':
                    player.cash+=0.2*player.cash
                    print str(player)+' got Cash +20%'
                elif card=='Cash: -20%':
                    player.cash-=0.2*player.cash
                    print str(player)+' got Cash -20%'
                elif card=='Loan Stock Matured':
                    player.cash+=10000
                    print str(player)+' got Loan Stock Matured! Rs 10,000 added to cash.'
                elif card=='Debenture':
                    print 'Debenture: In any one company, buy 1 share for every 2 you own in that company @ Rs.1/share!'
                    self.debenture(player)
                elif card=='Rights Issue':
                    self.rightsIssue(player)

    def debenture(self,player):
        '''
        Execute Debenture
        '''
        if len(player.stock.keys())==0: #do not execute if no stocks owned
            print 'Sorry you have no stocks,'+str(player)+'!'
            return
        
        if player==user:
            inputString=raw_input('>> ')
            commandList=inputString.split()
            company=commandList[1]
            stock=int(0.5*user.stock[company])
            
        elif player==cpu:
            company=random.choice(cpu.stock.keys())
            stock=int(0.5*cpu.stock[company])
            
        try:
            if game.isValidCompany(company):
                buy=player.specialBuy(company,stock)
                if buy==ValueError:
                    raise ValueError
            else:
                raise ValueError            
        except ValueError:
            print 'Invalid Input'
            return self.debenture()

    def rightsIssue(self,player):
        '''
        Execute the windfall card rights issue
        Lets you sell all your shares in a bankrupted company at 
        original prices.
        '''
        RIAvail=False
        for comp in game.priceMap.keys():   #check if any bankrupt company
            if game.priceMap[comp]<=0:
                RIcompany=comp
                RIAvail=True

        if RIAvail and player==user:
            ask=raw_input('Use Rights Issue for '+RIcompany+'?(y/n)')
            if ask=='y':
                player.specialSell(RIcompany,self.pastPrices)

        if RIAvail and player==cpu:
            player.specialSell(RIcompany,self.pastPrices)

    def giveStats(self):
        '''
        Gives final stats at end of round
        '''
        print 'At the end of this round, stats for '+str(user)+' are:\n'
        user.getStats()
        print 'And CPU stats are:\n'
        cpu.getStats()

        
def menu():
    '''
    Home screen output
    Returns menu option number 
    '''
    os.system('cls') #clears screen
    print "\t\t  Welcome to the Share Trader PC game!"
    print "\n\n\n\t\t\t\t1.New Game \n\n\t\t\t\t2.Help \n\n\t\t\t\t3.About \n\n\t\t\t\t4.Exit\n\n"
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

def initCPU():
    '''
    Creates a new instance of CPU user
    '''
    cpu=CPU()
    return cpu

def createGame():
    '''
    Creates a new instance of a game
    '''
    rounds=int(raw_input("Enter num of rounds: "))
    print "Creating a new game against CPU..."
    time.sleep(1)#generates a delay of 1 second to let user read the print statement above
    game=NewGame(rounds)
    return game
        
run=True                                #run flag used to indicate whether loop should run again
gameNum=1
while run:
    try:
        i=menu()
        if i==1:
            user=createUser()
            cpu=initCPU()
            game=createGame()
            game.roundInit()
            game.endGame()
            gameNum+=1
            raw_input("Press enter to return to menu")
            
        elif i==2:
            os.system('cls')
            helpMan=open("Game Rules.txt","r") #reads rules from Game Rules file
            print helpMan.read()
            raw_input("Press enter to return to menu")
        
        elif i==3:
            os.system('cls')
            print "ShareTrader v1.0\n\nWritten by Abhinav Dhere\n"
            print "This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License."
            print "See http://creativecommons.org/licenses/by-nc-sa/4.0/ for details."
            raw_input("Press enter to return to menu")

        elif i==4:
            run=False
    except:
        print 'Invalid Entry'
        time.sleep(1)

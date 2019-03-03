#ATM.py
from graphics import *
from button import Button

class User:

    def __init__(self, name, pin, checking, savings):
        self.name = name
        self.pin = pin
        self.checking = float(checking)
        self.savings = float(savings)

    def setChecking(self, amount):
        self.checking = amount
    

    def setSavings(self, amount):
        self.savings = amount

    def getChecking(self):
        #print(self.checking)
        return self.checking

    def depositChecking(self, amount):
        self.checking = float(self.checking) + float(amount)

    def depositSavings(self, amount):
        self.savings = float(self.savings) + float(amount)

    def withdrawChecking(self, amount):
        self.checking = float(self.checking) - float(amount)

    def withdrawSavings(self, amount):
        self.savings = float(self.savings) - float(amount)

    def getSavings(self):
        #print(self.savings)
        return self.savings

    def getName(self):
        return self.name

    def getPIN(self):
        return self.pin

    def transferToChecking(self, amount):
        self.savings = float(self.savings) - float(amount)
        self.checking = float(self.checking) + float(amount)

    def transferToSavings(self, amount):
        self.checking = float(self.checking) - float(amount)
        self.savings = float(self.savings) - float(amount)

class ATM:

    def __init__(self, user, interface):
        self.userDict = {}
        filename = 'accounts.txt'
        infile = open(filename, 'r')
        for line in infile:
            username, pin, checking, savings = line.split('\t')
            self.userDict[username] = User(username, pin, checking, savings)
        infile.close()
        self.user = user
        self.interface = interface

    def run(self):
        while True and self.interface.keepGoing():
            selection = self.interface.getSelection()
            #print(selection)
            self.processSelection(selection)
            # need to have a pause here. maybe make a method
            # in interface like interface.continue() not sure
            # if i should put here or at top like
            # 'while True and self.interface.continue()'??
        self.closeATM()
        
        
    def processSelection(self, s):
        # view
        if s[0] == 'V':
            account = self.interface.chooseAccount()
            if account[0] == 'C':
                msg = self.checkCheckingBalance(self.user)
                
                self.interface.displayMsg(msg)
            elif account[0] == 'S':
                msg = self.checkSavingsBalance(self.user)
                self.interface.displayMsg(msg)
        # withdraw
        elif s[0] == 'W':
            account = self.interface.chooseAccount()
            amount = self.interface.chooseAmount()
            self.withdraw(self.user, amount, account)
        # deposit
        elif s[0] == 'D':
            account = self.interface.chooseAccount()
            amount = self.interface.chooseAmount()
            self.deposit(self.user, amount, account)
        # transfer
        elif s[0] == 'T':
            accountTo = self.interface.chooseAccount()
            amount = self.interface.chooseAmount()
            transString = self.transfer(self.user, accountTo, amount)
            self.interface.displayMsg(transString)
        # close
        elif s[1] == 'l':
            self.closeATM()
            
        
    def checkCheckingBalance(self, name):
        return self.userDict[name].getChecking()

    def checkSavingsBalance(self, name):
        return self.userDict[name].getSavings()

    def deposit(self, name, amount, account):
        if account[0].lower() == 'c':
            self.userDict[name].depositChecking(amount)
        elif account[0].lower() == 's':
            self.userDict[name].depositSavings(amount)

    def withdraw(self, name, amount, account):
        if account[0].lower() == 'c':
            self.userDict[name].withdrawChecking(amount)
        elif account[0].lower() == 's':
            self.userDict[name].withdrawChecking(amount)

    def transfer(self, name, accountTo, amount):
        if accountTo[0].lower() == 'c':
            if self.userDict[name].getSavings() >= float(amount):
                self.userDict[name].transferToChecking(amount)
                return '{0} was transfered to checking'.format(amount)
            else:
                return 'Not enough in savings.'
        elif accountTo[0].lower() == 's':
            if self.userDict[name].getChecking() >= float(amount):
                self.userDict[name].transferToSavings(amount)
                return '{0} was transfered to savings'.format(amount)
            else:
                return 'Not enough in checking.'

    def closeATM(self):
        filename = 'accounts.txt'
        outfile = open(filename, 'w')
        for i in self.userDict:
            print(self.userDict[i].getName(), self.userDict[i].getPIN(),
                  self.userDict[i].getChecking(), self.userDict[i].getSavings(),
                  sep = '\t', file=outfile)
        outfile.close()
        self.interface.closeInterface()
        #print(type(self.interface))

class GraphicInterface:

    def __init__(self):

        win = GraphWin("ATM", 600, 500)
        win.setCoords(0.0,0.0,6.0,5.0)
        self.win = win
        self.__createButtons()
        self.__createDisplay()

    def __createButtons(self):

        self.commandButtonList = []
        self.amtButtonList = []
        self.accountButtonList = []
        commandButtonSpecs = [(1.5, 4, "View"), (2.5, 4, "Withdraw"),
                             (3.5, 4, "Deposit"), (4.5, 4, "Transfer")]
        for (x,y,label) in commandButtonSpecs:
            self.commandButtonList.append(Button(self.win, Point(x,y), 1, .5, label))

        amtButtonSpecs = [(2,3,"20"), (2.5,3,"40"), (3,3,"60"), (3.5,3,"80"),
                          (4,3,"100"), (2,2.5,"120"), (2.5,2.5,'140'), (3,2.5,'160'),
                          (3.5,2.5,'180'), (4,2.5,'200')]
        for (x,y,label) in amtButtonSpecs:
            self.amtButtonList.append(Button(self.win, Point(x,y), 0.5, 0.5, label))

        self.accountButtonList.append(Button(self.win, Point(3,2), 1, 0.5, "Checking"))
        self.accountButtonList.append(Button(self.win, Point(3,1), 1, 0.5, "Savings"))
        self.closeButton = Button(self.win, Point(4.5, 1), 1, 0.5, "Close")

        self.mainButton = Button(self.win, Point(1, 1), 1, 0.5, "Main")

    def __createDisplay(self):

        text = Text(Point(3,4.5), "")
        text.draw(self.win)
        self.display = text

    def getSelection(self):
        self.mainButton.deactivate()
        self.closeButton.activate()
        for b in self.accountButtonList:
            b.deactivate()
        for b in self.amtButtonList:
            b.deactivate()
        for b in self.commandButtonList:
            b.activate()
        self.display.setText("Select an action")
        while True:
            p = self.win.checkMouse()
            try:
                for b in self.commandButtonList:
                    if b.clicked(p):
                        return b.getLabel()
                if self.closeButton.clicked(p):
                    return self.closeButton.getLabel()
            except AttributeError as error:
                if error == "'NoneType' object has no attribute 'getX'":
                    pass

    def chooseAccount(self):
        for b in self.commandButtonList:
            b.deactivate()
        for b in self.accountButtonList:
            b.activate()
        self.display.setText("Select an account")
        while True:
            p = self.win.checkMouse()
            try:
                for b in self.accountButtonList:
                    if b.clicked(p):
                        return b.getLabel()
            except AttributeError as error:
                if error == "'NoneType' object has no attribute 'getX'":
                    pass
                
    def chooseAmount(self):
        for b in self.commandButtonList:
            b.deactivate()
        for b in self.accountButtonList:
            b.deactivate()
        for b in self.amtButtonList:
            b.activate()
        self.display.setText("Select an amount")
        while True:
            p = self.win.checkMouse()
            try:
                for b in self.amtButtonList:
                    if b.clicked(p):
                        return b.getLabel()
            except AttributeError as error:
                if error == "'NoneType' object has no attribute 'getX'":
                    pass

    def closeInterface(self):
        self.win.close()

    def displayMsg(self, msg):
        self.display.setText(str(msg))
        #print(msg)

    def keepGoing(self):
        #print(str(type(self)))
        #if str(type(self)) == "<class 'ATM.GraphicInterface'>":
            #print("yes")
        for b in self.commandButtonList:
            b.deactivate()
        for b in self.accountButtonList:
            b.deactivate()
        for b in self.amtButtonList:
            b.deactivate()
        self.mainButton.activate()
        self.closeButton.activate()
        while True:
            p = self.win.checkMouse()
            try:
                if self.mainButton.clicked(p):
                    return True
                elif self.closeButton.clicked(p):
                    return False
            except AttributeError as error:
                if error == "'NoneType' object has no attribute 'getX'":
                    pass
class userLogin:

    def __init__(self):
        self.userDict = {}
        filename = 'accounts.txt'
        infile = open(filename, 'r')
        for line in infile:
            username, pin, checking, savings = line.split('\t')
            self.userDict[username] = User(username, pin, checking, savings)
        infile.close()

        win = GraphWin("Enter Login Information", 200, 300)
        win.setCoords(0,0,2,3)
        self.win = win

        self.nameEntry = Entry(Point(1, 2), 15)
        self.nameEntry.draw(self.win)
        self.nameEntry.setText("Enter Username")
        self.pinEntry = Entry(Point(1,1.3), 15)
        self.pinEntry.draw(self.win)
        self.pinEntry.setText("Enter PIN")
        self.go = Button(self.win, Point(1,0.7), 1, 0.5, "Accept")
        self.go.activate()
        self.text = Text(Point(1, 2.5), "Enter Login Info")
        self.text.draw(self.win)

    def getUser(self):
        while True:
            p = self.win.checkMouse()
            try:
                if self.go.clicked(p):
                    username = self.nameEntry.getText()
                    pin = self.pinEntry.getText()
                    if self.accessGranted(username, pin):
                        self.win.close()
                        return username
                    else:
                        self.text.setText("Incorrect Username or PIN")
            except AttributeError as error:
                if error == "'str' object has no attribute 'getX'":
                    pass
                
    def accessGranted(self, username, pin):
        if self.userDict[username].getPIN() == pin:
            return True
        else:
            return False
                

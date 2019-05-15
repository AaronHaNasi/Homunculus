import random

class dice:
    sides = 6 # number of sides on die
    numberOfDice = 1 # number of dice
    modifier = 0 # number to add or subtract from final number. Will not be added or subtracted in shadowrun style (see below) 
    explodingDice = False # whether or not to activate exploding die
    # exploding dice are when the highest number is rolled, dice is rerolled and added to sum
    shadowRunStyle = False # when true, will return number of 5s and 6s, or 'hits' instead of sum total. Used with Shadowrun
    fudgeDice = False # some systems use 'fudge' dice, such as fate. If true, will roll fudge dice
    toString = ' '
    # def __new__(dice, inpt : str): 
    #     return 
    def roll(self): 
        rollResult = random.randint(1, self.sides) 
        return rollResult  
    def rollDice(self): 
        loopIterator = 0
        rollList = []
        total = 0 
        # while numberOfDice > loopIterator): 
        #     roll = random.randInt(1, sides)
        #     total += roll
        #     rollList.append(str(roll))
        #     loopIterator = loopIterator + 1
        
        while self.numberOfDice > loopIterator:
            rollTemp = self.roll()
            total += rollTemp
            rollList.append(str(rollTemp))
            loopIterator += 1
            while rollTemp == self.sides and self.explodingDice:
                rollTemp = self.roll()
                total += rollTemp
                rollList.append(str(rollTemp))
        total += self.modifier
        rollList.append('_**Final Total: ' + str(total) + '**_')
        self.toString = (', '.join(rollList))
        return self.toString
    def rollFudgeDice(self):
        # function to roll fudge dice
        rollList = []
        loopIterator = 0
        total = 0
        while self.numberOfDice > loopIterator:
            rollTemp = self.roll()
            if rollTemp is 1:
                rollList.append('+')
                total += 1
            elif rollTemp is 2: 
                rollList.append('-')
                total -= 1
            elif rollTemp is 3: 
                rollList.append('B')
            loopIterator += 1
        rollList.append('_**Final Total: ' + str(total) +'**_')
        self.toString = (', '.join(rollList))
        return 
            
    def rollShadowRunDice(self): # function to roll shadowrun dice and count 'hits'
        if self.sides is not 6:
            self.toString = 'Shadowrun uses d6s only.'
            return 
        hits = 0
        rollList = []
        loopIterator = 0
        while self.numberOfDice > loopIterator: 
            rollTemp = self.roll()
            if rollTemp == 5 or rollTemp == 6:
                hits += 1
            rollList.append(str(rollTemp))
            while self.explodingDice and rollTemp == 6:
                rollTemp = self.roll()
                if rollTemp == 5 or rollTemp == 6:
                    hits +=1
                rollList.append(str(rollTemp)) 
            loopIterator += 1 
        rollList.append('_**Total Hits: ' + str(hits) + '**_')
        self.toString = (', '.join(rollList))
        return # self.toString


    def in_string(self, inpt : str):
        # takes in string from discord command !rollDice
        # initialize temporary variables
        inpt = inpt.lower() 
        numberOfDiceStr = ' '
        sidesStr = ' '
        modifierStr = ' '
        if inpt.find('-e') is not -1: # discover if person wants exploding dice
            self.explodingDice = True
            inpt.replace('-e', '') # remove from string
        else:
            self.explodingDice = False
        if inpt.find('-s') is not -1: # discover if person wants to count 'hits' 
            self.shadowRunStyle = True 
            inpt.replace('-s','') # remove from string
        else:
            self.shadowRunStyle = False
        if inpt.find('-se') is not -1 or inpt.find('-es') is not -1:
                # discover if person wants to use both shadowrun style and exploding dice (both are commonly used in shadowrun) 
                self.shadowrunStyle = True
                self.explodingDice = True
                if inpt.find('-se') is not -1:
                    inpt.replace('-se', '')
                if inpt.find('-es') is not -1:
                    inpt.replace('es','')
        if inpt.find('d') is not -1:
            numberOfDiceStr, sidesStr = inpt.split('d')
        else:
            self.toString = 'Please input your dice roll as \'<x>d<y>\', where <x> and <y> are integers. <y> may also be \'f\' to roll fudge dice.'
            return 
        numberOfDiceStr = numberOfDiceStr.strip() # remove white space if numberOfDiceStr is 'f' or numberOfDiceStr is 'F':
        if len(numberOfDiceStr) is 0:
            self.numberOfDice = 1
        elif numberOfDiceStr.isdigit(): 
            self.numberOfDice = int(numberOfDiceStr) # convert to int 
        else: 
            self.toString = 'Please input your dice roll as \'<x>d<y>\', where <x> and <y> are integers. <y> may also be \'f\' to roll fudge dice.'
            return
        if sidesStr.find('+') is not -1: # check to see if there is a positive modifier
            sidesStr, modifierStr = sidesStr.split('+') #
            modifierStr = modifierStr.strip()
            self.modifier = int(modifierStr)
        elif sidesStr.find('-') is not -1: # check to see if there is a negative modifier 
            sidesStr, modifierStr = sidesStr.split('-')
        sidesStr = sidesStr.strip()
        if sidesStr is 'f' or sidesStr is 'F':
            self.fudgeDice = True
            self.sides = 3
        else:
            self.sides = int(sidesStr)
        if self.shadowRunStyle:
            self.rollShadowRunDice()
        elif self.fudgeDice:
             self.rollFudgeDice()
        else:
            self.toString = self.rollDice() 
        print(self.toString)
        return self.toString
        
    def __init__(self, inpt : str):
         self.in_string(inpt)
         # return output

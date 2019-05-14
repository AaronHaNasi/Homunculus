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
    
    def in_string(inpt : str):
        # takes in string from discord command !rollDice
        if inpt.find('-e') is not -1: # discover if person wants exploding dice
            explodingDie = True 
            inpt.replace('-e', '') # remove from string
        if inpt.find('-s') is not -1: # discover if person wants to count 'hits' 
            shadowRunStyle = True 
            inpt.replace('-s','') # remove from string
        if inpt.find('-se') is not -1 or if inpt.find('-es' is not -1:
                # discover if person wants to use both shadowrun style and exploding dice (both are commonly used in shadowrun) 
                shadowrunStyle = True
                explodingDie = True 
                if inpt.find('-se') is not -1:
                    inpt.replace('-se', '')
                if inpt.find('-es') is not -1:
                    inpt.replace('es','')
        if inpt.find('d') is not -1:
            numberOfDiceStr, sidesStr = dice.split('d')
        elif inpt.find('D') is not -1:
            numberOfDiceStr, sideStr = dice.split('D')
        numberOfDiceStr = numberOfDiceStr.strip() # remove white space
        if numberOfDiceStr is 'f' or numberOfDiceStr is 'F':
            # go to method for fudge dice
            return toString
        numberOfDice = int(numberOfDiceStr) # convert to int 
        if sideStr.find('+') is not -1: # check to see if there is a positive modifier
            sideStr, modifierStr = sideStr.split('+') #
            modifierStr = modifierStr.strip()
            modifier = int(modifierStr)
        elif sideStr.find('-') is not -1: # check to see if there is a negative modifier 
            sideStr, modifierStr = sideStr.split('-')
        sideStr = sideStr.strip()
        sides = int(sideStr)
        if shadowRunStyle:
            rollShadowRunDice()
        elif fudgeDice:
            rollFudgeDice()
        else:
            rollDice() 
        return toString
    def roll(self): 
        rollResult = random.randInt(1, sides) 
        return rollResult  
    def rollDice(self): 
        loopIterator = 0
        rollList = []
        total = 0 
       ''' while numberOfDice > loopIterator): 
            roll = random.randInt(1, sides)
            total += roll
            rollList.append(str(roll))
            loopIterator = loopIterator + 1
        '''
        while numberOfDice > loopIterator:
            rollTemp = roll()
            total += rollTemp
            rollList.append(str(rollTemp))
            while rollTemp == sides and explodingDice:
                rollTemp = roll()
                total += rollTemp
                rollList.append(str(rollTemp))
        total += modifier
        rollList.append('_**Final Total: ' + str(total) + '**_')
        toString = (', '.join(rollList))
    def rollFudgeDice(self):
        # function to roll fudge dice

    def rollShadowRunDice(self): 
        # function to roll shadowrun dice and count 'hits'
        hits = 0
        rollList = []
        loopIterator = 0
        while numberOfDice > loopIterator: 
            rollTemp = roll()
            if rollTemp == 5 or rollTemp == 6:
                hits += 1
            rollList.append(str(rollTemp))
            while explodingDice and rollTemp == 6:
                rollTemp = roll()
                if rollTemp == 5 or rollTemp == 6:
                    hits +=1
                rollList.append(str(rollTemp)) 
        rollList.append('_**Total Hits: ' + str(hits) + '**_')
        toString = (', '.join(rollList)) 

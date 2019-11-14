import random

# Used to 'pull' things out of a hat. Users can add things to the hat, and when something is pulled (at random), the string is removed from the text document
class hat:

    def addItem(self, inpt : str):
        hatFile = open('hat.txt', 'r')
        currentHatItems = hatFile.read()
        hatFile.close()
        hatFile = open('hat.txt', 'w')
        # hatItem = inpt[8:]
        hatFile.write(currentHatItems + '\n' + inpt)
        hatFile.close()
       
    def pullItem(self):
        hatItems = []
        hatFile = open('hat.txt', 'r')
        hatItems = hatFile.read().split('\n')
        hatFile.close()
        item = random.choice(hatItems)
        removeItem(item)
        return item

    def removeItem(self, itemToRemove : str):
        hatItems = []
        hatFile = open('hat.txt', 'r')
        hatItems = hatFile.read().split('\n')
        hatFile.close()
        for item in hatItems:
            if item == itemToRemove:
                hatItems.remove(item)
                return "Found item! Removed!"
            else:
                return "Could not find in hat."


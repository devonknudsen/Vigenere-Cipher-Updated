######################################
# Name: Devon Knudsen
# Date: 17 April 2020
# Assingment: Le Chiffre
# Written in Python 3
######################################

from sys import stdin

# shows stats of the deciphering process, if true
STATS = False

# the alphabet
# ALPHABET = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "
ALPHABET = " -,;:!?/.'\"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ"

# denotes the punctuation within the above alphabets, used for normalizing words
PUNCTUATION = " -,;:!?/.'\"()[]$&#%"

# dictionary file as well as potential keys
DICTIONARY_FILE = "dictionary.txt"

# threshold for the acceptable percentage of words
THRESHOLD = 0.9

# moves all keys that contain 5 or more chars to the front of the list (average length of US english words are 4.7 chars long)
# returns the shifted list of keys
def shiftLargerKeys(keys):
    avgKeys = []
    for key in keys:
        if (len(key) >= 5):
            avgKeys.append(key)
    
    for key in avgKeys:
        keys.remove(key)
        keys.insert(0, key)
            
    return keys

# generates and returns a list of all possible shifts of a given alphabet
def generateShifts():
    shiftedAlphabets = []
    for i in range(len(ALPHABET)):
        shiftStr = ALPHABET
        newStartIndx = 0
        
        # if not a shift of 0 (not the base alphabet),
        # concatenate all letters to be shifted to the end of the shifted alphabet string
        # update the starting index for string slicing
        if(i > 0):
            for j in range(i):
                shiftStr += shiftStr[j]
                newStartIndx += 1
        
        # slice the shifted chars from the beginning of shifted alphabet string
        shiftStr = shiftStr[newStartIndx:]
        
        # append correctly shifted alphabet string to the shifted alphabets list at
        # index where its first char would reside within the non shifted alphabet
        shiftedAlphabets.append(shiftStr)
    
    return shiftedAlphabets

# deciphers the a given cipher text using a given key and list of all alphabet shifts
# returns the deciphered text
def decipher(cTxt, key, alphaShifts):    
    dTxt = ""
    currKeyIndx = 0
    for i in range(len(cTxt)):
        if(cTxt[i] in ALPHABET):
            
            # reset current index within key if you've reached the end
            if(currKeyIndx == len(key)):
                currKeyIndx = 0
                
            # finds the index of the current key char within the base alphabet
            kIndx = ALPHABET.find(key[currKeyIndx])
            
            # finds the index of the plain text char using the shifted alphabet of the current key char and the current cipher text char
            pIndx = alphaShifts[kIndx].find(cTxt[i])
            
            # concatenates the plain text char to the deciphered text
            dTxt += ALPHABET[pIndx]
            
            # iterates to the next char within the key
            currKeyIndx += 1
        else:
            dTxt += cTxt[i]
    
    return dTxt

# normalizes candidate text by removing punctuation and new lines
# returns the normalized text
def normalizeTxt(txt):
    for p in PUNCTUATION:
        if(p != "'"):
            txt = txt.replace(p, "")
    
    txt = txt.replace("\n", " ")
    
    return txt.lower()

# MAIN
file = open(DICTIONARY_FILE, "r")
pKeys = file.read().rstrip("\n").split("\n")
file.close()

dictionary = []
for word in pKeys:
    dictionary.append(word.lower())
    
# filter potential keys
pKeys = shiftLargerKeys(pKeys)
    
cipherTxt = stdin.read().rstrip("\n")
cipherTxt = "\n".join(cipherTxt.split("\n"))

# generate list of all alphabet shifts
shiftedAlpha = generateShifts()

# iterating through keys to find the most correct deciphered text
for key in pKeys:
    pTxt = decipher(cipherTxt, key, shiftedAlpha)
    words = pTxt.split(" ")
    
    count = 0
    amountOfWords = len(words)
    for x in range(len(words)):
        normalizedWord = normalizeTxt(words[x])
        
        # if normalization caused two complete words to be held within a single string (removal of a new line)
        if(" " in normalizedWord):
            spaceIndx = normalizedWord.index(" ")
            normalizedWord = normalizedWord.replace(" ", "")
            firstWord = normalizedWord[:spaceIndx]
            secondWord = normalizedWord[spaceIndx:]
            if firstWord in dictionary:
                count += 1
            if secondWord in dictionary:
                count += 1
            
            # increasing count of the amount of words within the candidate text accounts for the two words
            # being bound together within a single string by a new line
            amountOfWords += 1
                
        elif(normalizedWord in dictionary):
            count += 1
           
    if((count/amountOfWords) >= THRESHOLD):
        print("KEY=" + key)
        print(pTxt)
        
        if(STATS):
            print("PERCENTAGE CORRECT: " + str(count/amountOfWords))
            print("COUNT: " + str(count))
            print("LENGTH OF WORDS: " + str(amountOfWords))
            
        exit(0)
import numpy as np
import pandas as pa
import pathlib
from collections import Counter

def readFile(path):

    wordList = []

    with open(path, 'r', encoding='UTF-8') as fil:
        for line in fil:
            wordList.extend(line.lower().split())
    return wordList

def countWordsInList(lis):
    pa.value_counts(np.array(lis))

def removeDuplicatesFromList(lis):
    return list(dict.fromkeys(lis))

def allListsInCat(listOfLists):
    res = []
    for lis in listOfLists:
        res = list(np.unique(res + lis))
    return res

def getTrimedListOfFilesInCat(path):
    catread = pathlib.Path(path)
    temp = list(catread.iterdir())
    allFil = []
    for fip in temp:
        allFil.append(readFile(fip))
    trimed = []
    for worlis in allFil:
        trimed.append(removeDuplicatesFromList(worlis))
    try:
        trimed.remove(['the', 'of', 'and', 'is', 'a', 'to'])
    except:
        pass
    return trimed

def readAllWordsInCat(path):
    return allListsInCat(getTrimedListOfFilesInCat(path))

def checkForExistenceInCat(catPath, checkCou):
    count = Counter()
    listOfTrimedTexts = getTrimedListOfFilesInCat(catPath)
    max = len(listOfTrimedTexts)
    for lis in listOfTrimedTexts:
        count.update(lis)
    wyn = {}
    for word, cou in count.items():
        wyn[word] = cou/max
    sorte = sorted(wyn.items(), key=lambda x: x[1], reverse=True)
    fin = []
    for tup in sorte:
        fin.append(tup[0])
    n_items = fin[0:checkCou]
    return n_items

def getMostCommonInAllCats(path, checkCou):
    catread = pathlib.Path(path)
    temp = list(catread.iterdir())
    allList = [None] * 21
    for cat in temp:
        try:
            allList[int(cat.__str__()[-2:])] = checkForExistenceInCat(cat, checkCou)
        except :
            allList[int(cat.__str__()[-1])] = checkForExistenceInCat(cat, checkCou)
    return allList

def checkFit(txtPath, models):
    wl = readFile(txtPath)
    counts = Counter()
    for i in range(0, 21):
        for wor in wl:
            if wor in models[i]:
                counts.update([i])
    return counts

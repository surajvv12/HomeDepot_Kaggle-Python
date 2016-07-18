# -*- coding: utf-8 -*-
"""
Created on Tue Feb 16 15:37:52 2016

@author: aniruddha
"""

import csv
import math
import nltk
import pdb
from scipy import spatial
from pandas import DataFrame, read_csv
import pandas as pd
import numpy as np
from nltk.corpus import wordnet as wn
from textblob import TextBlob
from textblob import Word
from textblob.wordnet import Synset
from textblob import TextBlob
import re
from nltk.corpus import stopwords



def generateTokens(TextItem):
    words = TextItem.split()
    return words

def ConvertTo_FreqVector(item, Lexicon) :
    vec = [0] * len(Lexicon)
    for itemword in item : # for each word in text
        for dicword in Lexicon :
            if itemword == dicword : # compare to the 
               indx = Lexicon.index(dicword) 
               # increment frequency
               vec[indx] = vec[indx] + 1
    return vec
    
def regexpProcessing (s) :
        s = s.replace("("," ")
        s = s.replace(")"," ")
        s = s.replace("\""," ")
        s = s.replace(",","") #could be number / segment later
        s = s.replace("$"," ")
        s = s.replace("?"," ")
        s = s.replace("-"," ")
        s = s.replace("//","/")
        s = s.replace("..",".")
        s = s.replace(" / "," ")
        s = s.replace(" \\ "," ")
        s = s.replace("."," . ")
        s = re.sub(r"(^\.|/)", r"", s)
        s = re.sub(r"(\.|/)$", r"", s)
        s = re.sub(r"([0-9])([a-z])", r"\1 \2", s)
        s = re.sub(r"([a-z])([0-9])", r"\1 \2", s)
        s = s.replace(" x "," xbi ")
        s = re.sub(r"([a-z])( *)\.( *)([a-z])", r"\1 \4", s)
        s = re.sub(r"([a-z])( *)/( *)([a-z])", r"\1 \4", s)
        s = s.replace("*"," xbi ")
        s = s.replace(" by "," xbi ")
        s = re.sub(r"([0-9])( *)\.( *)([0-9])", r"\1.\4", s)
        s = re.sub(r"([0-9]+)( *)(inches|inch|in|')\.?", r"\1in. ", s)
        s = re.sub(r"([0-9]+)( *)(foot|feet|ft|'')\.?", r"\1ft. ", s)
        s = re.sub(r"([0-9]+)( *)(pounds|pound|lbs|lb)\.?", r"\1lb. ", s)
        s = re.sub(r"([0-9]+)( *)(square|sq) ?\.?(feet|foot|ft)\.?", r"\1sq.ft. ", s)
        s = re.sub(r"([0-9]+)( *)(cubic|cu) ?\.?(feet|foot|ft)\.?", r"\1cu.ft. ", s)
        s = re.sub(r"([0-9]+)( *)(gallons|gallon|gal)\.?", r"\1gal. ", s)
        s = re.sub(r"([0-9]+)( *)(ounces|ounce|oz)\.?", r"\1oz. ", s)
        s = re.sub(r"([0-9]+)( *)(centimeters|cm)\.?", r"\1cm. ", s)
        s = re.sub(r"([0-9]+)( *)(milimeters|mm)\.?", r"\1mm. ", s)
        s = s.replace("°"," degrees ")
        s = re.sub(r"([0-9]+)( *)(degrees|degree)\.?", r"\1deg. ", s)
        s = s.replace(" v "," volts ")
        s = re.sub(r"([0-9]+)( *)(volts|volt)\.?", r"\1volt. ", s)
        s = re.sub(r"([0-9]+)( *)(watts|watt)\.?", r"\1watt. ", s)
        s = re.sub(r"([0-9]+)( *)(amperes|ampere|amps|amp)\.?", r"\1amp. ", s)
        s = s.replace("  "," ")
        s = s.replace(" . "," ")
        
        return s

def SimilarityCalculation(text1, text2) :
    
    # convert both texts into upper case
    TEXT1=text1.upper()
    TEXT2=text2.upper()

    TextItems= [TEXT1, TEXT2]
    token = []
    tokenList=[]
    for i in range(len(TextItems)):        
        token = generateTokens(TextItems[i])
        tokenList.append(token)
        token = []
    #print tokenList
    
    # create dictionary
    Lexicon = set()
    Lexicon = set().union(*tokenList)
    Lexicon = list(Lexicon)
    #print (Lexicon)

    # create vector space model from each text
    VectorPoints= []
    #pdb.set_trace()
    for textWordList in tokenList :
        vec=ConvertTo_FreqVector (textWordList, Lexicon)
        VectorPoints.append(vec)

    #print (VectorPoints)

    CosineSimilarity = 1 - spatial.distance.cosine(VectorPoints[0], VectorPoints[1])
    #print ("Cosine Silimatiry = ")
    #print (CosineSimilarity)
    if CosineSimilarity==0 :
        print(text1)
        print(text2)
    return CosineSimilarity
    
    
    
def Sim2(text1, text2) :
    
    stop = stopwords.words('english')
    
    text1=regexpProcessing(text1)
    text2=regexpProcessing(text2)
    
    # convert both texts into upper case
    TEXT1=text1.strip()
    TEXT2=text2.strip()
    TEXT1=TEXT1.lower()
    TEXT2=TEXT2.lower()
    
    token1 = generateTokens(TEXT1)
    token2 = generateTokens(TEXT2)
    
    t1List=[]
    for tok1 in token1:
        word1 = Word(tok1)
        w1=word1.spellcheck()
        correctw=w1[0][0]
        confidence = w1[0][1]
        
        if (confidence > 0.8) and (correctw not in stop):
            t1List.append(correctw)
            
            
    t2List=[]
    for tok2 in token2:
        word2 = Word(tok2)
        w2=word2.spellcheck()
        correctw=w2[0][0]
        confidence = w2[0][1]
        
        if (confidence > 0.8) and (correctw not in stop):
            t2List.append(correctw)
            
             
        
        
    
    
    
    for i in range(len(TextItems)):        
        token = generateTokens(TextItems[i])
        tokenList.append(token)
        token = []
    # spell correction
     
    
    # POS Tagging
    word1 = wn.synset('dog.n.01')
    word2 = wn.synset('cat.n.01')

    word1.path_similarity(word2)
    return CosineSimilarity
    
def main() :
    
    with open('product_descriptions.csv', 'r') as PD :
        PDreader = csv.reader(PD)
        PDmatrix = list(PDreader)
        
    
    file='train.csv'
    data = pd.read_csv(file,encoding="ISO-8859-1")
    
    print(data)
        
    print(0)
        
    
    


if __name__ == "__main__" :
    
    #main()
    with open('product_descriptions.csv', 'r') as PD :
        PDreader = csv.reader(PD)
        PDmatrix = list(PDreader)
        
    
    pdDict={}    
    for product in PDmatrix :
        pdDict[product[0]]=product[1]
         
    
    
        
        
            
    
    file='train.csv'
    data = np.array(pd.read_csv(file,encoding="ISO-8859-1",header=None))
    
    x=[]
    y=[]
    z=[]
    
    for idx,item in enumerate(data) :
        if idx > 0 :
              search_term=item[3]
              product_title=item[2]
              product_uid=item[1]
              relevance=item[4]
        
              # Find the corresponding description in PDmatrix
        
              item_description=pdDict[product_uid]
                
              x.append (Sim2(search_term, item_description))
              y.append (Sim2(search_term, product_title))
              z.append(relevance)
    

        
        
        
    
    print(data)
        
    print(0)
    

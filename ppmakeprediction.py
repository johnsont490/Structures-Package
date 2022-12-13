# -*- coding: utf-8 -*-
"""
Created on Mon Dec 12 20:22:41 2022

@author: johns
"""

from CheenadyNN1 import predictCheenadyhardness
from PughNN import predictPughhardness

def main():
    modeltype=input("Enter Pugh or Cheenady")
    inputdata=input("Enter material data in a pandas dataframe: ")
    if modeltype=="Cheenady":
        prediction=predictCheenadyhardness(inputdata)
    else:
        prediction=predictPughhardness(inputdata)
    print(prediction)
    



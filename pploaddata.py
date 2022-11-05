# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 14:35:02 2022

@author: johns
"""
#loads the data from matminer and uses pymatgen to find material structure 

from matminer.datasets import get_available_datasets
get_available_datasets()
from matminer.datasets import load_dataset
df=load_dataset("brgoch_superhard_training")
from matminer.datasets import get_all_dataset_info

from pymatgen.core.structure import Molecule

#need to find number of bonds in unit cell, unit cell volume, 
#bond length, electronegativity, and cood number

#create list of elements in each molecule
species=df["composition"]

#find cartesian coods
cartesiancoods=df["structure"]

materialslist=df["shear_modulus"]

print(df.iloc[0])

#create molecular info for each material in the database
moleculelist=[]    
for i, material in enumerate(df):
    elementslist=[]
    coodlist=[]
    for element in species[i]:
        elementslist.append(element)
    for cood in cartesiancoods[i]:
        coodlist.append(cood)
    print(elementslist)
    print(coodlist)
    break
    moleculelist.append(Molecule(elementslist,coodlist))
    
    #trying to get a list of the molecules but for some reason 
    #the length of the coodlist is double that of the elementslist 
    
print(moleculelist)

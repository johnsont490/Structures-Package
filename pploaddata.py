# -*- coding: utf-8 -*-
"""
Created on Sat Nov  5 14:35:02 2022

@author: johns
"""
#loads the data from matminer and uses pymatgen to find material structure 
from matminer.datasets import load_dataset
from hardnesscalculator import calculate_hardness
from bond_detector import detect_bonds
import pandas as pd
import pymatgen 

#load the dataset
df=load_dataset("brgoch_superhard_training")
                                                                  
#need to find number of bonds in unit cell, unit cell volume, 
#bond length, electronegativity, and cood number

def main():    
    #create pugh_hardness column 
    #clean dataset to remove shear and bulk modulus values <= 0
    filtereddf=df[df["shear_modulus"] > 0]
    filtereddf=df[df["bulk_modulus"] > 0]
    #calculate pugh hardness from filtered shear and bulk modulus cols 
    pugh_hardness = filtereddf["shear_modulus"]**3 / filtereddf["bulk_modulus"]**2
    filtereddf["pugh_hardness"] = 2*pugh_hardness**0.585 - 3
    #remove hardness values <= 0
    pughdf = filtereddf[filtereddf['pugh_hardness'] > 0]
    #save data as csv and pickle files 
    pughdf.to_csv("pugh_hardness.csv")
    pd.to_pickle(pughdf, "pugh_hardness.pkl") 
    
    #create intrinsic_hardness column
    dfn=load_dataset("brgoch_superhard_training")
    #remove floats 
    drop_indexes = []
    for row in dfn.itertuples():
        if type(row.structure) != pymatgen.core.structure.Structure:
            drop_indexes.append(row.Index)
    dfn.drop(drop_indexes, inplace=True)
    def get_intrinsic_hardness(structure):
        bonds = detect_bonds(structure)
        hardness = calculate_hardness(
            structure, bonds, model="CAS")
        return hardness
    dfn["intrinsic_hardness"] = dfn["structure"].apply(get_intrinsic_hardness)
    intrinsicdf=dfn[dfn["intrinsic_hardness"] > 0]        
    intrinsicdf.to_csv("intrinsic_hardness.csv")
    pd.to_pickle(intrinsicdf, "intrinsic_hardness.pkl")  
  
    
if __name__ == '__main__':
    main()  

    
    
    
    
    
    
    
    
    

"""
from matminer.featurizers.structure import SiteStatsFingerprint
from matminer.featurizers.site import AverageBondLength
from pymatgen.analysis.local_env import CrystalNN

nnalgo = CrystalNN()
bl = AverageBondLength(nnalgo)

sspbl = SiteStatsFingerprint(site_featurizer=bl)
df2 = sspbl.featurize_dataframe(df, "structure",ignore_errors=True)
 bonded_structure = CrystalNN().get_bonded_structure(structure)
 class Bond:
     def __init__(self,electronegativity,coodnum,bondlen):
         self.electronegativity=electronegativity
         self.coodnum=coodnum
         self.bondlen=bondlen
     def getbondinfo(self,electronegativity,coodnum,bondlen):

#featurize the elements
from matminer.featurizers.composition import ElementFraction
ef=ElementFraction()
element_fraction_labels=ef.feature_labels()
df = ef.featurize_dataframe(df, "composition")
"""


#CAS 
#map bonds and hardess to structure
#.apply
#doing ML only on features,hardness
#coming back and updating with structures info 
#use Salil package and add a hardness column 
#use pugh model and compare the two to show which works better 








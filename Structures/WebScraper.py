#!/usr/bin/env python
# coding: utf-8

# In[ ]:

import pandas as pd
from pathlib import Path

def scraper():
    """web scrape material websites to create a Pandas Dataframe
    
    Args: None, folder of text files must be in user's working directory
    
    Returns: Pandas DataFrame of materials and their respective properties, as well saves csv file of DataFrame
    """
    #import necessary packages
    from bs4 import BeautifulSoup as bs
    import requests
    
    
    #list of material text files in materials folder that will be given to user to download and place in their working directory
    
    materiallist = ["firstset.txt","secondset.txt","thirdset.txt","fourthset.txt","fifthset.txt","sixthset.txt","seventhset.txt","eighthset.txt","ninthset.txt","misc.txt"]
    
    #empty lists
    materials = []
    densities = []
    elasticmodulus = []
    yieldstrength = []
    website = []

    #iterate through list of material text files in materials folder
    for materialtxtfile in materiallist:
        
        #setting file path
        inputdata = Path.cwd() / "data"  / "Materials" / materialtxtfile
        
        #open material text filers
        with open(inputdata) as f:
            
            #read material ID's within material text files
            list_lines = f.readlines()
            
            #iterate through material ID's within material text files
            for line in list_lines:
                
                line = line.strip("\n")
                
                #request access to URL's of all materials using material ID's
                web_id = requests.get(f"https://www.azom.com/article.aspx?ArticleID={line}").text
                
                #material URL's
                web = (f"https://www.azom.com/article.aspx?ArticleID={line}")
                website.append(web)
                
                #parse html's of material websites
                soup = bs(web_id, "html.parser")
                
                #location of webaite title in html, specifically material name
                material = soup.find("h1")
                materialname = material.text.strip()
                materialname= materialname.replace("Aluminium / Aluminum" , "Aluminum")
                materialname= materialname.replace("Aluminum / Aluminium" , "Aluminum")
                materialname= materialname.replace("Brass Alloys - ", "")
                materialname= materialname.replace(" Properties, Fabrication and Applications","")
                materials.append(materialname)
                
                #first material text file
                if materialtxtfile == "firstset.txt":
                    
                    #specify tables that contain necessary material properties
                    table = soup.find_all("table",attrs={"style":"text-align: center; width: 100%;"})[1]
                    table2 = soup.find_all("table",attrs={"style":"text-align: center; width: 100%;"})[2]
                    
                    #location of material's density in html
                    density = table.find_all("td")[1]
                    
                    #location of material's yield strength in html
                    ystrength = table2.find_all("td")[4]
                    
                    #location of material's elastic modulus in html
                    emodulus = table2.find_all("td")[13]
                
                #second material text file
                if materialtxtfile == "secondset.txt":
                    
                    table = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[1]
                    table2 = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[2]
                    
                    density = table.find_all("td")[1]
                    ystrength = table2.find_all("td")[4]
                    emodulus = table2.find_all("td")[13]
                
                #third material text file
                if materialtxtfile == "thirdset.txt":
                    
                    table = soup.find_all("table",attrs={"style":"text-align: center; width: 100%"})[1]
                    table2 = soup.find_all("table",attrs={"style":"text-align: center; width: 100%"})[2]
                    
                    density = table.find_all("td")[1]
                    ystrength = table2.find_all("td")[4]
                    emodulus = table2.find_all("td")[10]
                
                #fourth material text file
                if materialtxtfile == "fourthset.txt":
                    
                    table = soup.find_all("table",attrs={"style":"text-align: center; width: 100%"})[1]
                    table2 = soup.find_all("table",attrs={"style":"text-align: center; width: 100%"})[2]
                    
                    density = table.find_all("td")[1]
                    ystrength = table2.find_all("td")[4]
                    emodulus = table2.find_all("td")[13]
                    
                #fifth material text file
                if materialtxtfile == "fifthset.txt":
                    
                    table = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[1]
                    table2 = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[2]
                    
                    density = table.find_all("td")[1]
                    ystrength = table2.find_all("td")[4]
                    emodulus = table2.find_all("td")[10]
                    
                #sixth material text file
                if materialtxtfile == "sixthset.txt":
                    
                    table = soup.find_all("table",attrs={"style":"text-align:center; width:100%"})[1]
                    table2 = soup.find_all("table",attrs={"style":"text-align:center; width:100%"})[2]
                    
                    ystrength = table.find_all("td")[1]
                    density = table2.find_all("td")[1]
                    emodulus = table2.find_all("td")[2]        
                    
                #seventh material text file
                if materialtxtfile == "seventhset.txt":
                    
                    table = soup.find_all("table",attrs={"style":"text-align: center; width: 100%"})[1]
                    table2 = soup.find_all("table",attrs={"style":"text-align: center; width: 100%"})[2]
                    
                    density = table.find_all("td")[1]
                    ystrength = table2.find_all("td")[4]
                    emodulus = table2.find_all("td")[7]
                    
                #eighth material text file
                
                if materialtxtfile == "eigthset.txt":
                    table = soup.find_all("table",attrs={"border":"0"})[1]
                    table2 = soup.find_all("table",attrs={"border":"0"})[2]
                    
                    ystrength = table.find_all("p")[5]
                    density = table2.find_all("p")[3]
                    emodulus = table2.find_all("p")[7]
                    
                #ninth material text file
                if materialtxtfile == "ninthset.txt":
                    
                    table = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[1]
                    table2 = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[2]
                    
                    density = table.find_all("td")[1]
                    ystrength = table2.find_all("td")[4]
                    emodulus = table2.find_all("td")[10]
                
                #miscellaneous text file containing remaining material ID's whose html's are unique from the others
                if materialtxtfile == "misc.txt":
                    
                        #first material ID in miscellaneous text file
                        if line == "6620":
                            
                            table = soup.find_all("table",attrs={"style":"text-align: center; width: 100%;"})[1]
                            table2 = soup.find_all("table",attrs={"style":"text-align: center; width: 100%;"})[2]
                            
                            density = table.find_all("td")[1]
                            ystrength = table2.find_all("td")[4]
                            emodulus = table2.find_all("td")[10]
                            
                        #second material ID in miscellaneous text file
                        if line == "6754":
                            
                            table = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[1]
                            table2 = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[2]
                            
                            density = table.find_all("td")[1]
                            ystrength = table2.find_all("td")[4]
                            emodulus = table2.find_all("td")[7]
                            
                        #third material ID in miscellaneous text file
                        if line == "960":
                            
                            table = soup.find_all("table",attrs={"width":"99%"})[0]
                            table2 = soup.find_all("table",attrs={"width":"99%"})[1]
                            
                            ystrength = table.find_all("td")[9]
                            density = table2.find_all("p")[13]
                            emodulus = table2.find_all("p")[14]
                            
                        #fourth material ID in miscellaneous text file
                        if line == "6575":
                            
                            table = soup.find_all("table",attrs={"style":"text-align: center; width: 100%;"})[1]
                            table2 = soup.find_all("table",attrs={"style":"text-align: center; width: 100%;"})[2]
                            
                            density = table.find_all("td")[1]
                            ystrength = table2.find_all("td")[4]
                            emodulus = table2.find_all("td")[7]
                            
                        #fifth material ID in miscellaneous text file
                        if line == "6380":
                            
                            table = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[1]
                            table2 = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[2]
                            
                            density = table.find_all("td")[7]
                            ystrength = table2.find_all("td")[7]
                            emodulus = table2.find_all("td")[25]
                            
                        #sixth material ID in miscellaneous text file
                        if line == "6371":
                            
                            table = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[1]
                            table2 = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[2]
                            
                            density = table.find_all("td")[1]
                            ystrength = table2.find_all("td")[4]
                            emodulus = table2.find_all("td")[19]
                            
                        #seventh material ID in miscellaneous text file
                        if line == "6506":
                            
                            table = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[1]
                            table2 = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[2]
                            
                            density = table.find_all("td")[1]
                            ystrength = table2.find_all("td")[13]
                            emodulus = table2.find_all("td")[1]
                            
                        #eighth material ID in miscellaneous text file
                        if line == "6396":
                            
                            table = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[1]
                            table2 = soup.find_all("table",attrs={"style":"TEXT-ALIGN: center; WIDTH: 100%"})[2]
                            
                            density = table.find_all("td")[1]
                            ystrength = table2.find_all("td")[13]
                            emodulus = table2.find_all("td")[5]
                
                #strip whitespace and split at whitespace for all density's
                newdensity = density.text.strip().split()
                
                #split first element at dash (to split up density's that are in the form of a range)
                newdensity = newdensity[0].split("-")
                
                if float(newdensity[0]) < 10:
                    
                    #convert density's in g/cm3 to kg/m3 (make units uniform)
                    newdensity[0] = float(newdensity[0])*1000
                
                #strip whitespace and split at whitespace for all yield strength's
                newyield = ystrength.text.strip().split()
                
                #split first element at dash (to split up yield strength's that are in the form of a range)
                newyield = newyield[0].split("-")
                
                #strip whitespace and split at whitespace for all elastic modulus'
                newelastic = emodulus.text.strip().split()
                
                #split first element at dash (to split up elastic modulus' that are in the form of a range)
                newelastic = newelastic[0].split("-")
                
                #add first density value in list as float to empty densities list
                densities.append(float(newdensity[0]))
                
                #add first yield strength value in list as float to empty yieldstrength list
                yieldstrength.append(float(newyield[0]))
                
                #add first elastic modulus value in list as float to empty elasticmodulus list
                elasticmodulus.append(float(newelastic[0]))
    
    #create dataframe out of all lists and save as a csv file
    materialproperties = pd.DataFrame({"Material": materials, "Density": densities, "YieldStrength": yieldstrength, "ElasticModulus": elasticmodulus, "Website": website}).to_csv("MaterialProperties.csv",index=False)
    
    #read newly saved csv file to display dataframe of materials and their properties
    data = pd.read_csv("MaterialProperties.csv")

    return data



def material_selection(beamobject):
    """selects optimal material for cantilever/supported beam by comparing max von Mises stress to all material's yield strength from scraper function
    
    Args: beamobject: created beam object from BeamSolver module
    
    Returns: calculated max Von mises stress and optimal material and its properties and website URL if user wants more information on chosen material
    """
    
    #import necessary modules and functions
    from BeamSolver import read_properties 
    from BeamSolver import Cantilever_Beam
    from BeamSolver import Supported_Beam
    import numpy as np
    
    #/ "data" / 
    #setting file path
    csvfile = Path.cwd() / "data" / "MaterialProperties.csv"
    data = pd.read_csv(csvfile)
    
    #calculating forces and reactions
    beamobject.calculate_forces()
    beamobject.shear_moment_calculation()
    forces = beamobject.force_dictionary
    
    #beam length
    b = beamobject.length
    
    #beam height
    h = beamobject.beam_height
    
    #max bending moment but absolute value (in N*m)
    M = abs(max(beamobject.moment))
    
    #max shear force but absolute value (in N)
    SF = abs(max(beamobject.shear))
    
    #calculate area of beam (in m^2)
    A = b*h

    #calculate moment of inertia of beam (in m^4)
    I = (b*h**3)/12

    #calculate distance from neutral axis of beam (in m)
    c = h/2

    #calculate max bending stress of beam (in Pa)
    bendstress = (M*c)/I

    #calculate max axial stress of beam (in Pa)
    axialstress = SF/A

    #calculate max von Mises stress of beam, will compare to yield stress (in MPa)
    vMstress = (np.sqrt((bendstress**2)+(axialstress**2)))*10**-6
    maxstress = print("Max Beam Stress: "+str(vMstress) + " MPa\n")
    
    #set first yield strength to infinity float
    currentYS = float("inf")
    
    #iterate through dataframe
    for row in data.itertuples():
        
        #checking yield strength against von Mises stress
        if row.YieldStrength > vMstress:
            
            #checking next yield stress in data frame against current yield stress
            if row.YieldStrength < currentYS:
                
                #if current yield stress satisfies requirements, output optimal material
                optimalmaterial = str(f"Optimal Material: {row.Material}"
                    f"\nDensity: {row.Density} kg/m3"
                    f"\nYield Strength: {row.YieldStrength} MPa"
                    f"\nElastic Modulus: {row.ElasticModulus} GPa"
                    f"\nWebsite: {row.Website}\n")
                
                #update yield stress that doesnt satisfy to next yield stress in dataframe
                currentYS = row.YieldStrength
                
    #if max stress greater than all available yield strengths then no suitable material for beam
    if currentYS == float("inf"):
        print("No optimal material for this beam")
    else:
        print(optimalmaterial)
        
    return 


# Structures Package 
This is a statics/structures package that can solve general problems and automatically generate beam illustrations and shear force/bending moment diagrams. It also includes a module on machine learning for calculating hardness from materials data.   


## Beam Solver Module
The beam solver module is a tool for solving statically determinate beams. The beams are restricted to supported and cantilever arrangements.
Beams are initially defined as either a Support_Beam or Cantilever_Beam object. Methods exist within the object to construct the features
and reactions acting upon the beam. The beam and it's reactions can then be solved through methods within the object.

Beams can be constructed from scratch using all the object methods or a read_properties function can be used to read a configuration file, with 
the details of the beam.


### Inputs:

**Point Force**:
* position (m)
* magnitude (N)

**Uniform Distributed Load**:
* start/end (m)
* distributed load (N/m)

**Moment**:
* position (m)
* magnitude (Nm)

**Supports**:
* position (m)

#### Outputs:
**Shear Force / Bending Moment Beam Diagrams**
  * position (m)
  * shear force (N) moment (Nm)

*All attributes of the beam object can also be saved as variables for any further personal calculations*

## WebScraper Module
This module was developed to scrape data from material websites, specifically the material names and their density, yield strength, and elastic modulus. This information is then used to create a Pandas DataFrame and save it as a csv file. Additionally, this module can select an optimal material for the beam case in the Beam Solver module by calculating the max von Mises stress of the beam and comparing it to the yield strength's in the DataFrame. If the max von Mises stress of the beam is greater than all yield strength's, then there is no optimal material for that case. 

### Inputs:
**Scraper**:
  * None

**Material Selection**:
  * Beam object from Beam Solver module
 
### Outputs:
**Scraper**:
   * Pandas DataFrame of materials and their respective properties

**Material Selection**:
   * Max von Mises stress of beam (MPa)
   * Optimal Material
   * Material's Density (kg/cm3)
   * Material's Yield Strength (MPa)
   * Material's Elastic Modulus (GPa)
   * Material's website
   * If no optimal material, then statement saying so
 
 *Material Selection can be done for beam's created manually or from config files*

## Machine Learning Module
This module was developed to predict hardness from material data using neural networks. These networks were trained on data using two different equations for calculating hardness- the Pugh model and the Cheenady model. Shear and bulk modulus data, and features data, respectively, were used to calculate hardness for a large number of materials, which was used as the target data to train the neural networks, which are able to calculate hardness in a way that is less computationally expensive.
### Importing the Package
from makehardnessprediction import makehardnessprediction
### Using the Package 
input materials data and model type as the arguments for the function below:

makehardnessprediction(inputdata,modeltype)

### Modules within Package:
### Modules used to create hardness data for training the neural networks:
* pploaddata - used to generate and export hardness data from Pugh and Cheenady models
* hardnesscalculator - used to calculate Cheenady hardness
* bond_detector - used to determine number of bonds 
 ***hardnesscalculator and bond_detector were made from https://github.com/salil91/intrinsic-hardness
### Modules used to create neural networks
* PughNNupd - neural network trained on Pugh hardness data
* CheenadyNNupd - neural network trained on Pugh hardness data
### Modules used to predict hardness from neural networks
* makehardnessprediction - backend for user interface, used to make hardness prediction from neural network
* Neural_Netuserinterface - user interface for the hardness prediction hardness prediction package 
* NN_Example_Notebook - an example of how to use the hardness prediction package 

### Inputs
* Model type (either Pugh or Cheenady)
* Materials data- either shear and bulk modulus (for Pugh) or features data (for Cheenady) 

### Outputs
* prediction for material hardness

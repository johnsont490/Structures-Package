# Taylor Johnson
# module for prediction hardness from neural network models 
 
#load the neural network modules 
from CheenadyNNupd import predictCheenadyhardness
from PughNNupd import predictPughhardness

#function to predict hardness from a given model and xlsx file containing material data 
def makehardnessprediction(modeltype,inputdata):
    #if selected model type 
    if modeltype=="cheenady":
        prediction=predictCheenadyhardness(inputdata)
    elif modeltype=="pugh":
        prediction=predictPughhardness(inputdata) 
    return prediction



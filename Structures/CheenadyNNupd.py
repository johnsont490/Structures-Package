# Taylor Johnson
# Cheenady NN

#import relevant libraries
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from keras import layers
from pathlib import Path

#import file from working directory
cheenadytrainingdata=Path.cwd() / "data" / "intrinsic_hardness1.pkl"

#load pickled dataframe
intrinsicdf=pd.read_pickle(cheenadytrainingdata)

#set the target as the intrinsic_hardness column, which contains the data from the hardness simulations
target=intrinsicdf["intrinsic_hardness"]
#set the features as the brgoch_feats column, which contains the atomistic data needed for training the NN
featuresdicseries=intrinsicdf["brgoch_feats"]
#turn the column into a list 
featuresdiclist=list(featuresdicseries)
#turn the list of dictionaries into a pandas dataframe containing the features data 
features = pd.DataFrame.from_records(featuresdiclist)
#add the target data column to the features dataframe
features["targetdata"]=intrinsicdf["intrinsic_hardness"]
#get the values of the features 
dataset=features.values
#create a mask that drops all the NaNs from the dataset 
mask = ~np.isnan(dataset).any(axis=1)
# Use the mask to index the array and remove the rows with NaN values
newdataset = dataset[mask]
#define the x array (the features to predict hardness) 
x = newdataset[:,0:150]
#define the y array (the target data)
y = newdataset[:,150]
#reshape the y array 
y=np.reshape(y, (-1,1))
    
#create the architecture of the neural network
from tensorflow.python.keras.optimizer_v2.adam import Adam
#define the learning rate 
adam_opt = Adam(learning_rate=0.0001)
#rescale the data 
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()
scaler_x.fit(x)
xscale=scaler_x.transform(x)
scaler_y.fit(y)
yscale=scaler_y.transform(y)
#divide the training and testing data 
X_train, X_test, y_train, y_test = train_test_split(xscale, yscale)
#define the moodel 
model = Sequential()
model.add(Dense(28, input_dim=150, kernel_initializer='normal', activation='relu'))
#add dropout layer to prevent overfitting of data 
model.add(layers.Dropout(0.25))
#commented out the below neuron to prevent overfitting
#model.add(Dense(13, activation='relu'))
model.add(Dense(1, activation='linear'))
#measure accuracy by mean squared error 
model.compile(loss='mse', optimizer=adam_opt, metrics=['mse','mae'])
#train the neural network 
history = model.fit(X_train, y_train, epochs=300, batch_size=100,  verbose=1, validation_split=0.2)
    
#creates a graph showing the model vs testing loss, uncomment to see 
"""plt.plot(history.history['loss'],color="blue")
    plt.plot(history.history['val_loss'],color="red")
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()"""

#create the function for predicting hardness based on the Cheenady NN 
def predictCheenadyhardness(inputdata):
    #material data should be an excel file path of structures data 
    df = pd.read_excel(inputdata)
    #get the values of the data
    inputarray=df.values
    #reshape the input 
    inputdata_reshaped = np.reshape(inputarray, (1, 150))
    #transform the input data
    transformeddata= scaler_x.transform(inputdata_reshaped)
    #predict the hardness from the Cheenady model
    hardnessprediction=model.predict(transformeddata)
    #invert the prediction to transform to original scale 
    invertedhardnessprediction = scaler_y.inverse_transform(hardnessprediction) 
    #print the prediction
    print("Predicted=%s" % (invertedhardnessprediction[0]))



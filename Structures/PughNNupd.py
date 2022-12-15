# Taylor Johnson
# Pugh NN

#import relevant libraries
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from tensorflow.python.keras.models import Sequential
from tensorflow.python.keras.layers import Dense
from keras import layers
from pathlib import Path

#import file from working directory
pughtrainingdata=Path.cwd() / "data" / "pugh_hardness.pkl"


#load pickled dataframe
pughdf=pd.read_pickle(pughtrainingdata)

#separate target and feature data
colstodrop=["formula", "composition", "material_id","structure","brgoch_feats","suspect_value"]
#drop unneeded columns
pughdf=pughdf.drop(columns=colstodrop)
#get the values of the data 
dataset=pughdf.values
#define the x array (the features to predict hardness)  
x = dataset[:,0:2]
#define the y array (the target data)
y = dataset[:,2]
#reshape the y array 
y=np.reshape(y, (-1,1))

#import optimizer library
from tensorflow.python.keras.optimizer_v2.adam import Adam
#define the learning rate 
adam_opt = Adam(learning_rate=0.0001)
#scale the x and y 
scaler_x = MinMaxScaler()
scaler_y = MinMaxScaler()
scaler_x.fit(x)
xscale=scaler_x.transform(x)
scaler_y.fit(y)
yscale=scaler_y.transform(y)
#divide the training and testing data 
X_train, X_test, y_train, y_test = train_test_split(xscale, yscale)
#create the model 
model = Sequential()
model.add(Dense(13, input_dim=2, kernel_initializer='normal', activation='relu'))
#add dropout layer to prevent overfitting of data 
model.add(layers.Dropout(0.25))
model.add(Dense(13, activation='relu'))
model.add(Dense(1, activation='linear'))
#compile the model 
model.compile(loss='mse', optimizer=adam_opt, metrics=['mse','mae'])
history = model.fit(X_train, y_train, epochs=300, batch_size=100,  verbose=1, validation_split=0.2)

#create the architecture of the neural network
def predictPughhardness(inputdata):
    #Pughdata should be an excel of bulk and shear modulus data 
    df = pd.read_excel(inputdata)
    inputarray=df.values
    #reshape the input 
    inputdata_reshaped = np.reshape(inputarray, (1, 2))
    #transform the input data
    transformeddata= scaler_x.transform(inputdata_reshaped)
    #predict the hardness from the Cheenady model
    hardnessprediction=model.predict(transformeddata)
    invertedhardnessprediction = scaler_y.inverse_transform(hardnessprediction) 
    print("Predicted=%s" % (invertedhardnessprediction[0]))




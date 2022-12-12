#!/usr/bin/env python
# coding: utf-8

# In[462]:


def cheenadyNN(): 
    import matplotlib.pyplot as plt
    import numpy as np
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.model_selection import cross_val_score
    from sklearn.model_selection import KFold
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import MinMaxScaler
    from tensorflow.python.keras.models import Sequential
    from tensorflow.python.keras.layers import Dense
    from tensorflow.python.keras.wrappers.scikit_learn import KerasRegressor
    from keras import layers
    #load pickled dataframe
    intrinsicdf=pd.read_pickle('intrinsic_hardness1.pkl')
    intrinsicdf = intrinsicdf.dropna(axis=0)
    target=intrinsicdf["intrinsic_hardness"]
    featuresdicseries=intrinsicdf["brgoch_feats"]
    featuresdiclist=list(featuresdicseries)
    features = pd.DataFrame.from_records(featuresdiclist)
    features = features.dropna(axis=0)
    features["targetdata"]=intrinsicdf["intrinsic_hardness"]
    dataset=features.values
    mask = ~np.isnan(dataset).any(axis=1)
    # Use the mask to index the array and remove the rows with NaN values
    newdataset = dataset[mask]
    x = newdataset[:,0:150]
    y = newdataset[:,150]
    y=np.reshape(y, (-1,1))
    
    #create the architecture of the neural network
    from tensorflow import keras
    import tensorflow as tf
    from tensorflow.keras import optimizers
    from tensorflow.python.keras.optimizer_v2.adam import Adam
    adam_opt = Adam(learning_rate=0.0001)
    scaler_x = MinMaxScaler()
    scaler_y = MinMaxScaler()
    scaler_x.fit(x)
    xscale=scaler_x.transform(x)
    scaler_y.fit(y)
    yscale=scaler_y.transform(y)
    X_train, X_test, y_train, y_test = train_test_split(xscale, yscale)
    model = Sequential()
    model.add(Dense(28, input_dim=150, kernel_initializer='normal', activation='relu'))
    #add dropout layer to prevent overfitting of data 
    model.add(layers.Dropout(0.25))
    #model.add(Dense(13, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer=adam_opt, metrics=['mse','mae'])
    #train the neural network 
    history = model.fit(X_train, y_train, epochs=300, batch_size=100,  verbose=1, validation_split=0.2)
    print(history.history.keys())
    
    #creates a graph showing the model vs testing loss, uncomment to visualize 
    """plt.plot(history.history['loss'],color="blue")
    plt.plot(history.history['val_loss'],color="red")
    plt.title('model loss')
    plt.ylabel('loss')
    plt.xlabel('epoch')
    plt.legend(['train', 'validation'], loc='upper left')
    plt.show()"""


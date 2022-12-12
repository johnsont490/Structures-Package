#!/usr/bin/env python
# coding: utf-8

# In[30]:


def pughNN(): 
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
    pughdf=pd.read_pickle("pugh_hardness.pkl")

    #starting with pugh hardness 
    from sklearn.preprocessing import StandardScaler
    #separate target and feature data
    colstodrop=["formula", "composition", "material_id","structure","brgoch_feats","suspect_value"]
    pughdf=pughdf.drop(columns=colstodrop)
    dataset=pughdf.values
    x = dataset[:,0:2]
    y = dataset[:,2]
    y=np.reshape(y, (-1,1))

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
    model.add(Dense(13, input_dim=2, kernel_initializer='normal', activation='relu'))
    #add dropout layer to prevent overfitting of data 
    model.add(layers.Dropout(0.25))
    model.add(Dense(13, activation='relu'))
    model.add(Dense(1, activation='linear'))
    model.compile(loss='mse', optimizer=adam_opt, metrics=['mse','mae'])
    history = model.fit(X_train, y_train, epochs=300, batch_size=100,  verbose=1, validation_split=0.2)


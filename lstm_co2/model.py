import tensorflow as tf
tf.compat.v1.enable_eager_execution()
import numpy as np
import itertools
from tensorflow import keras
from keras import layers
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import statsmodels.api as sm
import matplotlib.dates as dates
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import math
from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout, LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
from keras import optimizers
import time

#数据预处理和训练集，测试集构建
data = sm.datasets.co2.load_pandas().data
index = pd.date_range(start=data.index[0],periods=len(data),freq='W-SAT')
data=pd.DataFrame(data['co2'], index=index, columns=['co2'])
data = data['co2'].resample('MS').mean()
data = data.fillna(data.bfill())

data = data.values
scaler = MinMaxScaler(feature_range=(0, 1))
data = scaler.fit_transform(data.reshape(-1, 1))
x=[]
y=[]
time_back=1
for i in range(len(data)-time_back-1):
    x.append(data[i:i+time_back])
    y.append(data[i+time_back])
x=np.array(x) 
y=np.array(y)  
from sklearn.model_selection import train_test_split
trainX, testX, trainY, testY = train_test_split(x, y, test_size=0.3)
# #LSTM模型构建以及训练
# model=tf.keras.models.Sequential([
#     tf.keras.layers.LSTM(input_dim=1, units=50, return_sequences=True),
#     tf.keras.layers.LSTM(input_dim=50, units=100, return_sequences=True),
#     tf.keras.layers.LSTM(input_dim=100, units=200, return_sequences=True),
#     tf.keras.layers.LSTM(300, return_sequences=False),
#     tf.keras.layers.Dense(units=100),
#     tf.keras.layers.Dense(units=1)
# ])
# model.add(Activation('sigmoid'))    #激活函数可以自选
# start = time.time()
# model.summary()
# model.compile(optimizer=keras.optimizers.Adam(0.01),loss=keras.losses.mean_squared_error)
# model_information=model.fit(trainX,trainY,epochs=100,verbose=1)
# #模型损失可视化
# information_loss=model_information.history['loss']  #模型训练损失
# def loss(information_loss):
#     plt.figure(figsize=(12, 8))
#     plt.plot(information_loss)
#     plt.title('model loss')
#     plt.ylabel('loss')
#     plt.xlabel('epoch')
#     plt.show()
# loss(information_loss)

# tf.keras.models.save_model(model, 'my_model.h5')

model = tf.keras.models.load_model('my_model.h5')
#对测试集进行预测
testPredict = model.predict(testX)#这里预测出的结果也是在0-1之间的，这次就没做反归一化了，做不做效果都一样
#测试集进行可视化
plt.figure(figsize=(15, 5))
plt.plot(range(len(testPredict)), testPredict, label='prediction', linewidth=1)
plt.plot(range(len(testY)), testY, label='true', linewidth=1)
plt.ylabel('co2')
plt.xlabel('date')
plt.legend()
plt.title("prediction and true")
plt.show()

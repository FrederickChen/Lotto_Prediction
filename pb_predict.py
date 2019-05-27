import numpy
#import matplotlib.pyplot as plt
import pandas
import math
from keras.models import Sequential
from keras.layers import Dense,Dropout,Activation
from keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler
from sklearn.metrics import mean_squared_error
import sys

if (len(sys.argv)<= 1):
        print("Usage:%s loopback"%(sys.argv[0]))
        sys.exit(0)
if not sys.argv[1].isdigit():
        print("Please input a integer number!")
        sys.exit(0)
        
# convert an array of values into a dataset matrix
def create_dataset(dataset, look_back=1):
	dataX, dataY = [], []
	for i in range(len(dataset)-look_back-1):
		a = dataset[i:(i+look_back), :]
		dataX.append(a)
		dataY.append(dataset[i + look_back, :])
	return numpy.array(dataX), numpy.array(dataY)
# fix random seed for reproducibility
numpy.random.seed(8)
# load the dataset

dataframe = pandas.read_csv('pb.csv',header=None, engine='python')
dataset = dataframe.values
#print(dataset)
dataset = dataset.astype('float64')
bk_dataset = dataset

# normalize the dataset
scaler = MinMaxScaler(feature_range=(0, 1))
dataset = scaler.fit_transform(dataset)

# split into train and test sets
#train_size = int(len(dataset) * 0.9)
#test_size = len(dataset) - train_size
#train, test = dataset[0:train_size,:], dataset[train_size:len(dataset),:]

look_back = int(sys.argv[1])
train, test = dataset[:,:], dataset[-look_back:,:]

# reshape into X=t and Y=t+1

trainX, trainY = create_dataset(train, look_back)
#testX, testY = create_dataset(test, look_back)
testX = numpy.array(test)

# reshape input to be [samples, time steps, features]
trainX = numpy.reshape(trainX, (trainX.shape[0], look_back, trainX.shape[2]))
#testX = numpy.reshape(testX, (testX.shape[0], look_back, testX.shape[2]))
testX = numpy.reshape(testX, (1, look_back, testX.shape[1]))


# create and fit the LSTM network
model = Sequential()
model.add(LSTM(256, input_shape=(trainX.shape[1], trainX.shape[2]),return_sequences=True))
model.add(LSTM(128))
model.add(Dense(8))
model.compile(loss='mse', optimizer='adam',metrics=['acc'])
model.fit(trainX, trainY, epochs=800, batch_size=1, verbose=0)

# make predictions
trainPredict = model.predict(trainX)
testPredict = model.predict(testX)

# invert predictions
trainPredict = scaler.inverse_transform(trainPredict)
trainY = scaler.inverse_transform(trainY)

testPredict = scaler.inverse_transform(testPredict)
for i in range(testPredict.shape[1]):
        print("%.1f"%(testPredict[0,i]), end=' ')
print('\n',end="")       
#print(testPredict)

#testPredict_to_int = numpy.zeros((testPredict.shape[0],testPredict.shape[1]))
#testPredict_to_int = testPredict_to_int.astype('int64')
#for i in range(testPredict.shape[0]):
#       for j in range(testPredict.shape[1]):
#                testPredict_to_int[i,j] = round(testPredict[i,j])
#df = pandas.DataFrame(testPredict_to_int)
#df.to_csv('testPredict_pb',sep='\t',header=False,index=False)
                
sys.exit(0)


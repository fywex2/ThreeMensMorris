import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Flatten, MaxPooling2D
#from keras.utils import
import pandas as pd
data_frame = pd.read_csv('boardsAndWinnerTicTacToe.csv')
#print(data_frame)





X = data_frame.iloc[:,0:9].to_numpy()
X = X.reshape(-1, 3, 3)
X = X.reshape((958, 3, 3, 1))
y = data_frame.loc[:, ['winner']].to_numpy().reshape(1,-1).flatten()
#print(data_frame.loc[10:20])
#print(X)
#print(y)
y = keras.utils.to_categorical(y)

#y = to_categorical(y)
#print(y)
#exit()
x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)
#print(x_test)
#exit()
#print(x_test.shape, x_train.shape, y_test.shape, y_train.shape)
model = Sequential([
    #Conv2D(filters=1, kernel_size=(3, 3), input_shape=(3, 3, 1), activation='relu'),
    # Add more layers as needed
    Conv2D(filters=128, kernel_size=(3, 3), input_shape=(3, 3, 1), activation='relu', padding='same'),
    Conv2D(filters=64, kernel_size=(3, 3), input_shape=(3, 3, 1), activation='relu', padding='same'),
    #MaxPooling2D(pool_size=(2, 2)),
    Flatten(),
    Dense(128, activation='relu'),
    Dense(64, activation='tanh'),
    Dense(16, activation='relu'),
    #Dense(units=64, activation='relu'),
    Dense(units=3, activation='softmax')  # 3 output units for the three classes
])
'''
model = Sequential([
      Conv2D(64, (3,3), activation= 'relu',input_shape=(3,3,1)),
      Flatten(),
      Dense(64, activation='tanh'),
      Dense(16, activation='relu'),
      Dense(3, activation='softmax')
   ])'''
model.compile(
      optimizer='Adam',
      loss= 'categorical_crossentropy',
      metrics=['accuracy']
   )
#print(y, y.shape)

history = model.fit(
      x=x_train,
      y=y_train,
      epochs=50,
      shuffle=True
   )



score = model.evaluate(x_test, y_test, verbose = 0)
score_train = model.evaluate(x_train, y_train, verbose = 0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])

#answer = model.predict(np.array([1,0,2,0,1,2,0,0,1]).reshape(-1, 1).T)
#print("[1,0,2,0,1,2,0,0,1]",answer)
state = np.array([1,0,2,0,1,2,0,0,1])
state = state.reshape(-1, 3, 3)
state = state.reshape((-1, 3, 3, 1))
answer = model.predict([state])
print(answer,"succeed?")
print(history.history.keys())
acc=history.history['accuracy']
print("accuracy - train",score_train[1])

loss=history.history['loss']
#val_loss=history.history['val_loss']

epochs=range(1,len(acc)+1)
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.plot(epochs, acc, 'bo', label='Training acc')

plt.title('Training  accuracy')
plt.legend()



plt.show()

# save and load model
model.save('saved model.keras')
model1 = keras.models.load_model('saved model.keras')

#answer1 = model1.predict(np.array([1,0,2,0,1,2,0,0,1]).reshape(-1, 1).T)
#print("[1,0,2,0,1,2,0,0,1] from saved  model",answer1)

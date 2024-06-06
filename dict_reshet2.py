from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout
from keras.utils import to_categorical
import pandas as pd
from sklearn.metrics import confusion_matrix
from keras.layers import Dense,Dropout, Conv2D,Flatten,MaxPooling2D

#print(data_frame)
X=np.load('x_file.npy')

y=np.load('y_file.npy')

#print(y)
#exit()

print(X.shape)
print(y.shape)

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)


#print(x_test)
#exit()
#print(x_test.shape, x_train.shape, y_test.shape, y_train.shape)
model = Sequential([

    Conv2D(filters=64, kernel_size=(3, 3), input_shape=(3, 3, 1), activation='relu', padding='same'),
    Flatten(),
    Dense(258, activation='relu'),
    Dense(64, activation='tanh'),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(units=1, activation='tanh'),
])
#    Dense(258, activation='relu',input_shape=(5, 5, 1)), without conv2D
#   add anther x3 that contains all the boards in 1 dimansinal
model.compile(
      optimizer='Adam',
      loss= 'mse',
      metrics=['accuracy']
   )

history = model.fit(
      x=x_train,
      y=y_train,
      epochs=20,
      shuffle=True
   )



score = model.evaluate(x_test, y_test, verbose = 0)
score_train = model.evaluate(x_train, y_train, verbose = 0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])


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
model.save('saved model3.keras')

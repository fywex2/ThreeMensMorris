import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Flatten, MaxPooling2D
import pandas as pd


X = np.load("x_file.npy")
y = np.load("y_file.npy")

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

model = Sequential([
    Conv2D(filters=64, kernel_size=(3, 3), input_shape=(3, 3, 1), activation='relu', padding='same'),
    Flatten(),
    Dense(258, activation='relu'),
    Dense(64, activation='tanh'),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(units=1, activation='tanh'),
])
model.compile(
      optimizer='Adam',
      loss='mse',
      metrics=['accuracy']
   )

history = model.fit(
      x=x_train,
      y=y_train,
      epochs=20,
      shuffle=True
   )

score = model.evaluate(x_test, y_test, verbose=0)
score_train = model.evaluate(x_train, y_train, verbose=0)

print('Test loss:', score[0])
print('Test accuracy:', score[1])

print(history.history.keys())
acc = history.history['accuracy']
print("accuracy - train", score_train[1])

loss = history.history['loss']

epochs = range(1, len(acc)+1)
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.plot(epochs, acc, 'bo', label='Training acc')

plt.title('Training  accuracy')
plt.legend()
plt.show()

model.save('saved model2.keras')




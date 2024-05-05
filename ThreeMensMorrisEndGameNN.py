import numpy as np
import matplotlib.pyplot as plt
from tensorflow import keras
from sklearn.model_selection import train_test_split
from keras.models import Sequential
from keras.layers import Dense, Dropout, Conv2D, Flatten, MaxPooling2D
import pandas as pd


X = np.load("x_file.npy")
y = np.load("y_file.npy")

y = keras.utils.to_categorical(y)

x_train, x_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=0)

model = Sequential([
    #Conv2D(filters=128, kernel_size=(3, 3), input_shape=(3, 3, 1), activation='relu', padding='same'),
    Conv2D(filters=32, kernel_size=(3, 3), input_shape=(3, 3, 1), activation='tanh', padding='same'), # relu 64 before change
    Flatten(),
    #Dense(128, activation='relu'),
    Dense(64, activation='tanh'),
    #Dense(16, activation='relu'),
    Dense(units=2, activation='softmax')  # 2 output units for the three classes
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
model1 = keras.models.load_model('saved model2.keras')

import numpy as np
import json

with open("dict2.json", 'r') as fp:
    existing_data = json.load(fp)

# Extract values from the dictionary
reshaped_array = np.array([np.array([int(char) for char in string]).reshape(3, 3) for string in existing_data.keys()])
reshaped_array[reshaped_array == 2] = -1

print(reshaped_array)
np.save('x_file.npy', reshaped_array)
import json
import numpy as np

with open("dict.json", 'r') as fp:
    existing_data = json.load(fp)

keys = np.array(list(existing_data.keys()))

def string_to_3x3_array(s):
    return np.array(list(map(int, s))).reshape(3, 3)

# Function to replace 2 with -1 in a 3x3 array
def replace_2_with_minus_1(arr):

    return arr

# Convert each string in keys to a 3x3 array of integers and replace 2 with -1
result = np.array([replace_2_with_minus_1(string_to_3x3_array(s)) for s in keys])

# Output the result
print(result)

np.save('x_file.npy', result)
import json
import numpy as np

with open("dict.json", 'r') as fp:
    existing_data = json.load(fp)

list_of_keys_as_lists = [[int(char) for char in key[i:i+3]] for key in existing_data.keys() for i in range(0, 9, 3)]
list_of_keys_as_lists = [list_of_keys_as_lists[i:i+3] for i in range(0, len(list_of_keys_as_lists), 3)]
array_of_keys = np.array(list_of_keys_as_lists)

print(array_of_keys)
np.save('x_file.npy', array_of_keys)
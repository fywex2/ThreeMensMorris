import numpy as np
import json

with open("dict.json", 'r') as fp:
    existing_data = json.load(fp)

# Extract values from the dictionary
values_list = [value[0] for value in existing_data.values()]

# Convert the list to a NumPy array
array_of_values = np.array(values_list)

print(array_of_values)
# Save the array to a .npy file
np.save('y_file.npy', array_of_values)
import numpy as np
import json

with open("dict.json", 'r') as fp:
    existing_data = json.load(fp)

# Extract values from the dictionary
values = np.array([value[0] for value in existing_data.values()])

print(values)
np.save('y_file.npy', values)
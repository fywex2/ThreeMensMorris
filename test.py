import json

# Open the JSON file
with open('dict2.json') as json_file:
    # Load the JSON data into a Python dictionary
    my_dict = json.load(json_file)

modified_dict = {}

for key in my_dict:
    # Replace '2' with 'X' and '1' with 'O' in the key
    modified_key = key.replace('2', 'X').replace('1', 'O')
    # Assign the value of the original key to the modified key
    modified_dict[modified_key] = my_dict[key]

print(modified_dict)

with open('dict2.json','w') as json_file:
  json.dump(modified_dict, json_file)
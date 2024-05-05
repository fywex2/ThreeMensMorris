import json

# Open the JSON file
with open('dict.json') as json_file:
    # Load the JSON data into a Python dictionary
    my_dict = json.load(json_file)

def replace_symbols(board_dict):
    replaced_dict = {}
    for key, value in board_dict.items():
        new_key = key.replace('2', 'X').replace('1', 'O')
        replaced_dict[new_key] = value
    return replaced_dict

my_dict = replace_symbols(my_dict)
print(my_dict)

with open('dict2.json','w') as json_file:
  json.dump(my_dict, json_file)
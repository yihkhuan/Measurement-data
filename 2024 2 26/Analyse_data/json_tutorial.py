## reading a json file
import json
 
# Opening JSON file
# f = open('fitted.json')
 
# # returns JSON object as 
# # a dictionary
# data = json.load(f)
 
# # Iterating through the json
# # list
# for i in data['fitted_data']:
#     print(i.get('name'))
 
# # Closing file
# f.close()

## A nested dictionary
f = open('json_try.json')
dictionary = json.load(f)
print(dictionary['x'].get('name'))

f.close()

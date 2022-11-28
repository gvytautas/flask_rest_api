import requests
import json

base_url = 'http://127.0.0.1:5000'

result_index = requests.get(base_url + '/api/index')
print('Dictionary:', json.loads(result_index.text))
print('JSON:', result_index.text)

# data = {
#    'key': True
# }
# json.dumps -> dict to json <-> serialization
# json.loads -> json to dict <-> deserialization
# print(json.dumps(data))
# print(json.loads(json.dumps(data)))

result_show_categories = requests.get(base_url + '/api/show_categories')
print(json.loads(result_show_categories.text))

data = {
    'name': 'Category4'
}

result_create_category = requests.post(base_url + '/api/create_category', json=data)
print(json.loads(result_create_category.text))

data = {
    'name': 'NewCategoryName1'
}

result_update_category = requests.put(base_url + f'/api/update_category/{1}', json=data)
print(json.loads(result_update_category.text))

result_delete_category = requests.delete(base_url + f'/api/delete_category/{4}')
print(json.loads(result_delete_category.text))

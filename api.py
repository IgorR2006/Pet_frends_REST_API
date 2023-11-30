import requests
import json
from requests_toolbelt.multipart.encoder import MultipartEncoder



class PetFriends:
    def __init__(self):
        self.base_url = 'https://petfriends.skillfactory.ru'
        
    def get_api_key(self, email, password):
        
        headers = {
            'email': email,
            'password': password
        }
        
        res = requests.get(self.base_url + '/api/key', headers=headers)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        
        return status, result
    
    
    def get_list_of_pets(self, auth_key, filter):
        
        headers = {
            'auth_key': auth_key['key']
        }
        filter = {
            'filter': filter
        }
        
        res = requests.get(self.base_url + '/api/pets', headers=headers, params=filter)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        
        return status, result

    
    def post_api_create_pet_simple(self, auth_key: json, name: str, animal_type: str, age: str) -> json:
        """ Метод отправляет POST-запрос, позволяющий добовлять (постить) нового питомца без фотографии,
        возвращает статус запроса на сервер и результат в формате json с данными добавленного питомца"""

        data = MultipartEncoder(
            fields={
                'name': name,
                'animal_type': animal_type,
                'age': age
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/create_pet_simple', headers=headers, data=data)

        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result
    
    
    def post_api_pets_set_photo(self, auth_key: json, pet_id: str, pet_photo: str) -> json:
        """ Метод передает POST-запрос для добавления фотографии к уже существующему питомцу, используя pet_id,
        возвращает статус запроса и результат с обновленными данными питомца в формате json"""

        data = MultipartEncoder(
            fields={
                'pet_photo': (pet_photo, open(pet_photo, 'rb'), 'image/jpeg')
            })
        headers = {'auth_key': auth_key['key'], 'Content-Type': data.content_type}

        res = requests.post(self.base_url + '/api/pets/set_photo/' + pet_id, headers=headers, data=data)
        status = res.status_code
        result = ""
        try:
            result = res.json()
        except json.decoder.JSONDecodeError:
            result = res.text
        print(result)
        return status, result
from api import PetFriends
from settings import valid_email, valid_password
import os.path


pf = PetFriends()

def message(mess):
    return print(f'{mess}')


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result 
    
    
def test_get_all_pets_whith_valid_key(filter=''):
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0 
    
    
def test_post_api_create_pet_simple(name='Котэ_', animal_type='cat', age = '4'):
    """Тест на добавление нового питомца без фотографии"""

    # Запрашиваем ключ api и сохраняем его в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фотографии
    status, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name  
    
    
def test_post_api_pets_set_photo(pet_photo = 'images\jelly.jpg'):
    """ Тест на добавление фотографии питомца """

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем добавить фотографию
    if len(my_pets['pets']) > 0:
        status, result = pf.post_api_pets_set_photo(auth_key, my_pets['pets'][0]['id'], pet_photo)
        # Проверяем, что статус ответа = 200
        assert status == 200
    else:
        # если список питомцев пустой, то срабатывает исключение "об отсутствии своих питомцев"
        raise Exception(message("Мои питомцы отсутствуют!"))    
   
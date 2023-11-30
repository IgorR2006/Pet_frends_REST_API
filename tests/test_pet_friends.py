from api import PetFriends
from settings import valid_email, valid_password, no_valid_email, no_valid_password
import os.path


pf = PetFriends()

def message(mess):
    return print(f'{mess}')


def test_get_api_key_for_valid_user(email=valid_email, password=valid_password):
    status, result = pf.get_api_key(email, password)
    assert status == 200
    assert 'key' in result 
    
    
def test_get_all_pets_whith_valid_key(filter=''):
    """Тест на наличие списка всех питомцев"""
    
    # Получаем ключ auth_key и проверяем наличие питомцев в разделе "Все птомцы"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    assert status == 200
    assert len(result['pets']) > 0 
    
# Тест №1    
    
def test_post_api_create_pet_simple(name='Котэ_', animal_type='cat', age = '4'):
    """Тест на добавление нового питомца без фотографии"""

    # Запрашиваем ключ api и сохраняем его в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фотографии
    status, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name      

# Тест №2

def test_get_my_pets(filter='my_pets'):
    """Тест на наличие списка своих питомцев"""

    # Получаем ключ auth_key и проверяем наличие питомцев в разделе "Мои питомцы"
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)
    if len(result['pets']) > 0:
        # Проверяем, что статус ответа 200
        assert status == 200
    else:
        # Если раздел "Мои питомцы" пуст, срабатывает исключение "об отсутствии своих питомцев"
        raise Exception(message("Мои питомцы отсутствуют!"))    
    
# Тест №3    
    
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
        raise Exception(message('Мои питомцы отсутствуют!'))    
   
# Тест №4
   
def test_get_api_key_with_no_valid_user(email=no_valid_email, password=no_valid_password):
    """ Тест на ввод некорректных email и пароля"""

    status, result = pf.get_api_key(email, password)
    # Проверяем, что статус ответа 403 и не удается получить ключ auth_key
    assert status == 403
    assert 'key' not in result
    message("Вы ввели неверный email и пароль!")   
    
# Тест №5
    
def test_get_api_key_with_no_valid_email(email=no_valid_email, password=valid_password):
    """ Тест на ввод некорректного email при вводе верного пароля"""

    status, result = pf.get_api_key(email, password)
    # Проверяем, что статус ответа 403 и не удается получить ключ auth_key
    assert status == 403
    assert 'key' not in result
    message("Вы ввели неверный email!")    
    
# Тест №6
    
def test_get_api_key_with_no_valid_password(email=valid_email, password=no_valid_password):
    """ Тест на ввод неверного пароля"""

    status, result = pf.get_api_key(email, password)
    # Проверяем, что статус ответа 403 и не удается получить ключ auth_key
    assert status == 403
    assert 'key' not in result
    message("Вы ввели неверный пароль!")
    
# Тест №7   
    
def test_create_pet_simple_not_valid(name='', animal_type='', age = ''):
    """Тест на добавление нового питомца с незаполненными данными,
    на данный момент тест FAILED, так как при отправке незаполненных полей возвращает статус 200 и
    создает в списке Мои питомцы питомцев с пустыми полями"""

    # Запрашиваем ключ api и сохраняем его в переменную auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца без фотографии
    status, result = pf.post_api_create_pet_simple(auth_key, name, animal_type, age)

    # Сверяем полученный ответ с ожидаемым результатом 400, означающим - предоставляемые данные не верны
    assert status == 400
    
# Тест №8 
    
def test_delete_pet_with_notvalid_auth_key():
    """Тест на невозможность удаления питомца при неверном ключе авторизации"""

   # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Допустим возможность применения неверного ключа авторизации
    notvalid_auth_key = {"key": "a27aadb613116dfd656a96f42aed887a4fc371acb748f7637634f69"}

    # Проверяем - если список своих питомцев пустой, то добавляем нового и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Котопес", "пес", "2", "images/peng.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")    
        
    # Выбираем первого питомца и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(notvalid_auth_key, pet_id)

    # Убеждаемся, что при неверном ключе удаление питомца из списка мои питомцы не осуществляется, статус 403
    # The error code means that provided auth_key is incorrect
    assert status == 403
    message("Неверный ключ авторизации!")
    
    
 # Тест №9

def test_update_pet_info_invalid_auth_key(name='Масахиро', animal_type='котя', age=4):
    """Тест на обновление информации о питомце при неверном ключе авторизации"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Допустим возможность приминения неверного ключа авторизации
    notvalid_auth_key = {"key": "a27aadb613116dfd656a96f42aed887a4fc371acb748f7637634f69"}

    # # Если список не пустой, то пробуем обновить имя, тип и возраст питомца при не верном ключе
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(notvalid_auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем статус ответа:
        assert status == 403
        message("Неверный ключ авторизации!")

    else:
    # если спиок питомцев пустой, то срабатывает исключение с текстом об отсутствии своих питомцев
        raise Exception("Список моих питомцев пуст!")


 # Тест №10

def test_update_pet_info_not_valid(name='', animal_type='', age=''):
    """Тест на обновление информации о питомце при вводе пустых значений,
    на данный момент тест FAILED, так как статус ответа 200 и допускается ввод пустых значений"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Если список не пустой, то пробуем обновить имя, тип и возраст питомца
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

    # Проверяем статус ответа, 400 (The error code means that provided data is incorrect)
        assert status == 400
        message("Незаполненные поля!")

    else:
    # если спиок питомцев пустой, то срабатывает исключение с текстом об отсутствии своих питомцев
        raise Exception("Список моих питомцев пуст!")                    
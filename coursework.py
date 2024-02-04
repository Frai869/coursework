import requests
import json
from tqdm import tqdm
from pprint import pprint
from urllib.parse import urlencode


vk_token = ''
vk_id = int(input('Bведите id пользователя vk:\n'))
ya_token = input('Скопируйте токен с Полигона Яндекс.Диска:\n')


'''Получаем сведения о фотографиях ВК'''
class VKAPIClient:
    def __init__(self, vk_token, user_id):
        self.token = vk_token
        self.user_id = user_id

    def get_photos(self):
        params = {
            'owner_id': self.user_id,
            'album_id': 'profile',
            'rev': 0, #хронологический порядок
            'extended': 1,
            'access_token': self.token,
            'v': '5.131'
        }
        response = requests.get('https://api.vk.com/method/photos.get', params=params)
        return response.json()

if __name__ == '__main__':
    vk_client = VKAPIClient(vk_token, vk_id)
    photos_info = vk_client.get_photos()
    # pprint(photos_info)


'''Получаем пожелания пользователя'''
answer = str(input('Желаете задать количество фотографий для скачивания (y/n)?\n'))
number = int(input('Сколько фотографий с сайта vk.com скачаем?\n')) if answer == 'y' else 5
folder_name = str(input('В какую папку на Яндекс Диске будем сохранять?\n'))

'''Создаем папку на Яндекс Диске'''
base_url = 'https://cloud-api.yandex.net'
url_create_folder = f'{base_url}/v1/disk/resources'
params_dict = {
   'path': folder_name
}
headers_dict = {
    'Authorization': ya_token
}
response = requests.put(url_create_folder, params=params_dict, headers=headers_dict)

'''Скачиваем фотографии'''
# url_load = photos_info.get('response').get('items')
in_total = len(photos_info.get('response').get('items'))
for n in tqdm(range(min(number, in_total))):
    likes = photos_info.get('response').get('items')[n].get('likes').get('count')
    url_load_photos = photos_info.get('response').get('items')[n].get('sizes')
    width = 0
    url_photo_max = ''
    for i in (url_load_photos):
        if i.get('width') > width:
            width = i.get('width')
            url_photo_max = i.get('url')
    with open(f'{likes}.jpg', 'wb') as file:
        file.write(requests.get(url_photo_max).content)

        '''Сохраняем на Яндекс Диск'''
    url_get_link = f'{url_create_folder}/upload'
    params_dict = {
        'path': f'{folder_name}/{likes}.jpg',
        'overwrite': 'true'
    }
    headers_dict = {
        'Authorization': ya_token
    }
    response = requests.get(url_get_link, params=params_dict, headers=headers_dict)
    url_for_upload = response.json().get('href')
    with open (f'{likes}.jpg', 'rb') as file:
        response = requests.put(url_for_upload, headers=headers_dict, files={'File': file})

ans = input('Показать json-файл с информацией (y/n)?\n')
pprint(photos_info) if ans == 'y' else None
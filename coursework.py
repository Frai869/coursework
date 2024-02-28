import requests
import json
from tqdm import tqdm
from pprint import pprint
from urllib.parse import urlencode

# получить токен для ВК по ссылке:
app_id = '51845037'
oauth_base_url = 'https://oauth.vk.com/authorize'
params = {
    'client_id': app_id,
    'redirect_uri': 'https://oauth.vk.com/blank.html',
    'display': 'page',
    'scope': 'photos',
    'response_type': 'token',
    'v': '5.131'
}
oauth_url = f'{oauth_base_url}?{urlencode(params)}'
print(oauth_url)

vk_token = '' # вставить полученный токен
vk_id = int(input('Bведите id пользователя vk:\n'))
ya_token = input('Скопируйте токен с Полигона Яндекс.Диска:\n')

answer = str(input('Желаете задать количество фотографий для скачивания (y/n)?\n'))
input_number = int(input('Сколько фотографий с сайта vk.com скачаем?\n')) if answer == 'y' else 5
input_folder_name = str(input('В какую папку на Яндекс Диске будем сохранять?\n'))

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

def create_folder(folder_name):
    base_url = 'https://cloud-api.yandex.net'
    url_create_folder = f'{base_url}/v1/disk/resources'
    params_dict = {
       'path': folder_name
    }
    headers_dict = {
        'Authorization': ya_token
    }
    response = requests.put(url_create_folder, params=params_dict, headers=headers_dict)
    return response.json()

def saving_photos(folder_name, likes_, dates_):
    base_url = 'https://cloud-api.yandex.net'
    url_create_folder = f'{base_url}/v1/disk/resources'
    url_get_link = f'{url_create_folder}/upload'
    params_dict = {
        'path': f'{folder_name}/{likes_}-{dates_}.jpg'
    }
    headers_dict = {
        'Authorization': ya_token
    }
    response_ = requests.get(url_get_link, params=params_dict, headers=headers_dict)
    url_for_upload = response_.json().get('href')
    with open (f'{likes_}.jpg', 'rb') as file:
        requests.put(url_for_upload, headers=headers_dict, files={'File': file})
    return

def download_photos(photos_info, number):
    in_total = len(photos_info.get('response').get('items'))
    for n in tqdm(range(min(number, in_total))):
        likes = photos_info.get('response').get('items')[n].get('likes').get('count')
        dates = photos_info.get('response').get('items')[n].get('date')
        url_load_photos = photos_info.get('response').get('items')[n].get('sizes')
        width = 0
        url_photo_max = 0
        for i in (url_load_photos):
            if i.get('width') > width:
                width = i.get('width')
                url_photo_max = i.get('url')
        with open(f'{likes}.jpg', 'wb') as file:
            file.write(requests.get(url_photo_max).content)
        saving_photos(input_folder_name, likes, dates)
    return

if __name__ == '__main__':
    vk_client = VKAPIClient(vk_token, vk_id)
    photos_info = vk_client.get_photos()
    create_folder(input_folder_name)
    download_photos(photos_info, input_number)

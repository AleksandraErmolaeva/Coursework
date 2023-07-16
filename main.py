
    
import time
import requests
import json
from pprint import pprint
import datetime
from tqdm import tqdm

def upload_photos (id, vk_token, token_yandex, quantity_photos = 5):
    URL = 'https://api.vk.com/method/photos.get'
    params = {
        'owner_id': id,
        'album_id': 'profile',
        'extended': '1',
        'photo_sizes': '1',
        'access_token': vk_token, 
        'v':'5.131'
    }
    res = requests.get(URL, params=params)

    names = []
    list_sizes = ['w', 'z', 'y', 'r', 'q', 'p', 'o', 'x', 'm', 's']
    sizes_of_file = []
    sorted_photos_for_json = []
    sorted_photos_for_yandex =[]
    name_of_folder = 'vk_photos'

    for one_pic in res.json()['response']['items']:
        name_of_file = str(one_pic['likes']['count'])+'.jpg' 
        if name_of_file in names:
            name_of_file =str(one_pic['likes']['count'])+'.jpg'+ '_'+datetime.datetime.fromtimestamp(one_pic['date']).strftime('%d_%m_%Y')
        names.append(name_of_file)


        stop = 0
        for type in list_sizes:
            if stop != 0 : break
            for size_of_file in one_pic['sizes']:
                if stop != 0: break
                if size_of_file['type'] == type:
                    stop = 1
                    sizes_of_file.append({'file_name': name_of_file, 'size':size_of_file['type'], 'url': size_of_file['url']})
             

    for el in list_sizes:
        if len(sorted_photos_for_json) == quantity_photos: break
        for photo in sizes_of_file:
            if len(sorted_photos_for_json)== quantity_photos: break
            if photo['size'] == el:
                sorted_photos_for_json.append({'file_name':photo['file_name'], 'size':photo['size']})
                sorted_photos_for_yandex.append({'path': name_of_folder + '/' + photo['file_name'], 'url':photo['url']})
            

    
    url_folder ='https://cloud-api.yandex.net/v1/disk/resources'
    
    requests.put(url_folder, headers ={'Authorization': 'OAuth {}'.format(token_yandex)}, params = {'path' : name_of_folder})

    for one_photo_yandex in tqdm(sorted_photos_for_yandex):
        params_yandex = one_photo_yandex
        url_yandex = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        response = requests.post(url_yandex, headers={'Authorization': 'OAuth {}'.format(token_yandex)}, params=params_yandex)
    if 200 <= response.status_code < 300 :
        print(f'На Ваш Яндекс.Диск загружено {len(sorted_photos_for_yandex)} фото')
    else:
        print('Ошибка')

    with open (f'{name_of_folder}.json', 'w') as f:
        json.dump(sorted_photos_for_json,f, indent = 2)
    print(f'Создан файл {name_of_folder}.json')

id = 'требуется внести id VK'
token_yandex = 'требуется внести token yandex'
vk_token = 'требуется внести vk token'
upload_photos (id, vk_token, token_yandex, 5)





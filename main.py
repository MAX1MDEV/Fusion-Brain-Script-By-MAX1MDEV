import json
import time
import base64
import requests
from cursesmenu import CursesMenu
from cursesmenu.items import FunctionItem, SubmenuItem, CommandItem

class Text2ImageAPI:

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=8, width=1024, height=1024, style=3):
        styles = ["KANDINSKY", "UHD", "ANIME", "DEFAULT"]
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "style": styles[style],
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

    def generate_image():
        api = Text2ImageAPI('https://api-key.fusionbrain.ai/', 'API-KEY', 'SECRET-KEY')
        model_id = api.get_model()
        style = int(input("Введите номер стиля по порядку: KANDINSKY, UHD, ANIME, DEFAULT: "))
        style -= 1
        zapros = input("Введите ваш промпт: ")
        num_images = int(input("Введите количество изображений (1-8): "))
        print("Следующие два значения в сумме не должны превышать 2048!")
        width = int(input("Введите ширину изображения (<=1024):"))
        height = int(input("Введите высоту изображения (<=1024):"))
        racsh = int(input("Введите номер расширения изображения по порядку: .png, .jpg: "))
        if racsh == 1:
            for i in range(num_images):
                uuid = api.generate(zapros, model_id, 1, width, height, style)
                images = api.check_generation(uuid)
                image_base64 = images[0]
                image_data = base64.b64decode(image_base64)
                with open(f"image_{i}.png", "wb") as file:
                    file.write(image_data)
        else:
            for i in range(num_images):
                uuid = api.generate(zapros, model_id, 1, width, height, style)
                images = api.check_generation(uuid)
                image_base64 = images[0]
                image_data = base64.b64decode(image_base64)
                with open(f"image_{i}.jpg", "wb") as file:
                    file.write(image_data)
                    
        print("\nГотово!")
        print("Не забудьте перенести фотографии в любое место перед следующим запросом!")
        input("\nНажмите Enter для возврата в меню...")
            
    def get_styles():
        url = 'https://cdn.fusionbrain.ai/static/styles/api'
        response = requests.get(url)
        if response.status_code == 200:
            json_data = json.loads(response.text)
            for item in json_data:
                print(f'Название_ru: "{item["title"]}", \nНазвание_en: "{item["titleEn"]}", \nПример: "{item["image"]}"\n')
        else:
            print(f'Проверьте своё интернет подключение. Error {response.status_code}')
        input("Нажмите Enter для возврата в меню...")
     
    def get_info():
        print("Код написан: MaximDev a.k.a. MaxonKlaxon\n")
        print("Github:https://github.com/MAX1MDEV")
        print("Discord:https://discordapp.com/users/390102465586003978/\n")
        input("Нажмите Enter для возврата в меню...")
    
if __name__ == '__main__':
    menu = CursesMenu("Вас приветствует скрипт создания изображений Fusion Brain", "Выберите пункт меню: ")
    #command_item = CommandItem("Узнать информацию о стилях", "touch get_styles.py")
    function1_item = FunctionItem("Узнать информацию о стилях", Text2ImageAPI.get_styles)
    function2_item = FunctionItem("Начать создание изображения(-й)", Text2ImageAPI.generate_image)
    
    #submenu = CursesMenu("Код написан: MaximDev a.k.a. MaxonKlaxon")
    #submenu_item = SubmenuItem("Инфо", submenu)
    function3_item = FunctionItem("Инфо", Text2ImageAPI.get_info)
    menu.items.append(function1_item)
    menu.items.append(function2_item)
    menu.items.append(function3_item)
    menu.show()


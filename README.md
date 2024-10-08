# GenAI-image-cachine-service

Сервис для поиска похожих изображений. 
Алгоритм работы: 
1) Конвертирует диффузионный промпт в осмысленное предложение
2) Извлекает nsfw_tag 
3) Создает эмбединг предложения
4) Осуществляет поиск по базе загруженных изображений по эмбедингу и тегу



### Чтобы запустить все сервисы сразу достаточно 1й команды:
* docker-compose up --build

### Чтобы запустить только базы данных
* docker-compose up --build
* После этого можно запустить src/main.py локально, или в режиме дебагера, для удобной разработки
#### Swagger API будет доступен по адресу `http://0.0.0.0:8017/docs/`

### Туториал по добавлению новых фото в сервис и примеры обращений
`notebooks/Tutorial.ipynb` 


### Доступные методы сервиса (service methods):
* /get_image_candidate/ - получает найденные записи, которые удовлетворяют условию. Далее, их можно обработать на стороне клиента, и выбрать нужную картинку, по расстоянию или другим признакам.
* /add_image_usage_record/ - добавляем запись о том, что по этому user_id мы использовали картинку с этим img_uuid. Для того что бы одному юзеру не выдавались одинаковые картинки
* /upsert_cached_image/ - метод, позволяюищй добавить запись (или обновить существующую)
* /list_collections/ - показывает все коллекции добавленные в базу
* /remove_collection/ - удаляет коллекцию


### Вспомогательные функции клиента (client_utils):
* def upsert_cached_image(persona, img_uuid, img_path, prompt, emb, tags) - добавление изображения в базу
* def get_cached_image(persona, user_id, prompt, tags, n_results=1) - поиск релевантного изображения в базе
* def add_cached_record(user_id, img_uuid, img_path) - добавить запись об использовании изображения. Выполняется автоматически в get_cached_image если передан user_id



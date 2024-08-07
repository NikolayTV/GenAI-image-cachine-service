# GenAI-image-cachine-service

### Чтобы запустить все сервисы сразу достаточно 1й команды:
* docker-compose up --build

### Чтобы запустить только базы данных
* docker-compose up --build chroma-db mongo-db
После этого можно запустить src/main.py локально, или в режиме дебагера, для удобной разработки

Swagger API будет доступен по адресу `http://0.0.0.0:8017/docs/`
### Доступные методы:
* get_image_candidate - получает найденные записи, которые удовлетворяют условию. Далее, их можно обработать на стороне клиента, и выбрать нужную картинку, по расстоянию или другим признакам.
* add_image_usage_record - добавляем запись о том, что по этому user_id мы использовали картинку с этим img_uuid. Для того что бы одному юзеру не выдавались одинаковые картинки
* upsert_cached_image - метод, позволяюищй добавить запись (или обновить существующую)


### Вспомогательные материалы
`notebooks/1. create_table.ipynb` - подготовка данных перед загрузкой в БД + заполнение коллекции в chroma. Обязательные поля: 'img_path', 'prompt', 'img_uuid', 'embs'. Опциональные - различные тэги, начинаются с `tag_`


`notebooks/2.Service queries.ipynb` - примеры запросов в запущенный сервис




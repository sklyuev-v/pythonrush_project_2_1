# Второй проект по курсу Python Fullstack

#### JavaRush

Простой сервис для просмотра и хранения картинок в виде веб-приложения.

### Используемые технологии:

- backend: python
- server: nginx
- container: docker

### Что умеет сервис:

1. Можно загружать изображения
2. Выдает прямую ссылку на загруженное изображение, которой можно с кем-нибудь поделиться
3. Можно в галерее просмотреть все изображения загруженные на сайт

### Ограничения:

- Размер файла изображение не более 5 МБ
  - nginx не пропустит файлы более 5 МБ
- Поддерживаемые форматы: GIF, PNG, JPG
  - pillow проверит, что лежит в файле, перед сохранием

### Что и где лежит:

- логи лежат в томе `logs`
- изображения лежат в томе `images`

### Как запустить?

- `docker compose up --build`
- `make run`

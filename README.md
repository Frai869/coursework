# Курсовая работа по модулю ООП и работа c API
Программа для резервного копирования фотографий с профиля(аватарок) пользователя vk в облачное хранилище Яндекс.Диск.

**Задание: написать программу, которая будет:**

Получать фотографии с профиля VK.

Сохранять фотографии максимального размера(ширина/высота в пикселях) на Я.Диске.

Для имени фотографий использовать количество лайков.

Сохранять информацию по фотографиям в json-файл с результатами.

**Входные данные:**

Пользователь вводит:
 
id пользователя vk;

токен с Полигона Яндекс.Диска.

**Обязательные требования к программе:**

Использовать REST API Я.Диска и ключ, полученный с полигона.

Для загруженных фотографий нужно создать свою папку.

Сохранять указанное количество фотографий(по умолчанию 5) наибольшего размера (ширина/высота в пикселях) на Я.Диске.

Сделать прогресс-бар или логирование для отслеживания процесса программы.

Код программы должен удовлетворять PEP8.

У программы должен быть свой отдельный репозиторий.

Все зависимости должны быть указаны в файле requiremеnts.txt.​

---

***Этапы выполнения работы:***

**Запрошен пользовательский ввод id, токена и параметров загрузки**

**Создан класс для взаимодействия с API VK**

**Написана функция, создающая папку на Я.Диске (принимает на вход пользовательский ввод имени)**

**Написана функция для сохранения указанного количества фотографий на Я.Диске, генерируется уникальное имя из количества лайков и даты фотографии**

**Написана функция для загрузки фотографий максимального размера со страницы пользователя VK**

**Сгенерирован файл зависимостей requiremеnts.txt**


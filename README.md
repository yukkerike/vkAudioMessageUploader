# vkAudioMessageUploader
Отправка mp3/ogg/3gp аудиофайлов в качестве голосовых сообщений


## Начало

> **[python 3.4](https://python.org/) или новее**

    $ git clone https://github.com/ikozlovsky/vkAudioMessageUploader.git
    $ cd vkAudioMessageUploader
    $ pip3 install -r requirements.txt

> Либо скачайте отдельно файл audiomsg.py, разместите его в удобном месте и установите зависимость через pip: 

    $ pip3 install vk_api

## Запуск

> Подставьте своё значение переменной __ACCESS_TOKEN__ в __audiomsg.py__ и запустите скрипт:

    $ python3 audiomsg.py [ДИАЛОГ] [ПУТЬ ДО ФАЙЛА 1] ... [ПУТЬ ДО ФАЙЛА n]

> Так же токен можно передать первым аргументом, тогда скрипт не обязательно редактировать:

    $ python3 audiomsg.py [ACCESS_TOKEN] [ДИАЛОГ] [ПУТЬ ДО ФАЙЛА 1] ... [ПУТЬ ДО ФАЙЛА n]

> Аргумент [ДИАЛОГ] представляет собой либо числовой id диалога (id беседы можно указать в кратком формате, начав его с символа "@": @97, либо в полном формате: 2000000097), либо строку, входящую в название диалога (поиск осуществляется по 50 последним диалогам), пробелы в этом аргументе следует экранировать.

> Примеры:

    $ python3 audiomsg.py d1e45caf232775ada422fed97544cd2bc5bca69a918ac0f7b22d625d209a6bb9b6c2760767865111c3ed4 антон\ королёв /Users/ivan/Downloads/bbae553bfe.mp3
    $ python3 audiomsg.py сберкот /Users/ivan/Downloads/bbae553bfe.mp3 /Users/ivan/Downloads/f0ec2572a2.mp3
    $ python3 audiomsg.py @97 /Users/ivan/Downloads/bbae553bfe.mp3
    $ python3 audiomsg.py 2000000097 /Users/ivan/Downloads/bbae553bfe.mp3
    $ python3 audiomsg.py 94388048 /Users/ivan/Downloads/bbae553bfe.mp3

Получить токен можно тут: <http://oauth.vk.com/authorize?client_id=2685278&display=mobile&redirect_uri=https://oauth.vk.com/blank.html&scope=725086&response_type=token&v=5.101&revoke=1>

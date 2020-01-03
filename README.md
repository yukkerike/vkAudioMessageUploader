# vkAudioMessageUploader
Отправка mp3/ogg/3gp аудиофайлов в качестве голосовых сообщений


## Начало

> [python 3.4](https://python.org/) или новее

    $ git clone https://github.com/ikozlovsky/vkAudioMessageUploader.git
    $ cd vkAudioMessageUploader
    $ pip3 install -r requirements.txt

> Либо скачайте отдельно файл audiomsg.py, разместите его в удобном месте и установите библиотеку [vk_api](https://github.com/python273/vk_api) через pip: 

    $ pip3 install vk_api

## Запуск

> Запустите скрипт (все аргументы могут следовать в произвольном порядке):

    $ python3 audiomsg.py [ACCESS_TOKEN] [ДИАЛОГ] [ПУТЬ ДО ФАЙЛА 1] ... [ПУТЬ ДО ФАЙЛА n]

> Либо подставьте своё значение переменной __ACCESS_TOKEN__ в __audiomsg.py__, чтобы не указывать его в аргументах каждый раз и запустите скрипт  (все аргументы могут следовать в произвольном порядке):

    $ python3 audiomsg.py [ДИАЛОГ] [ПУТЬ ДО ФАЙЛА 1] ... [ПУТЬ ДО ФАЙЛА n]


> Аргумент [ДИАЛОГ] представляет собой либо числовой id диалога (id беседы можно указать в кратком формате, начав его с символа "@": @97, либо в полном формате: 2000000097), либо строку для поиска среди 50 последних диалогов.

> Примеры:

    $ python3 антон королёв audiomsg.py d1e45caf232775ada422fed97544cd2bc5bca69a918ac0f7b22d625d209a6bb9b6c2760767865111c3ed4  /Users/ivan/Downloads/bbae553bfe.mp3 
    Отправка в: 94388048
    $ python3 audiomsg.py d1e45caf232775ada422fed97544cd2bc5bca69a918ac0f7b22d625d209a6bb9b6c2760767865111c3ed4 антон королёв /Users/ivan/Downloads/bbae553bfe.mp3
    Отправка в: 94388048
    $ python3 audiomsg.py /Users/ivan/Downloads/bbae553bfe.mp3 /Users/ivan/Downloads/f0ec2572a2.mp3 сберкот
    Отправка в: -157369801
    $ python3 audiomsg.py @97 /Users/ivan/Downloads/bbae553bfe.mp3
    Отправка в: 2000000097
    $ python3 audiomsg.py 2000000097 /Users/ivan/Downloads/bbae553bfe.mp3
    Отправка в: 2000000097
    $ python3 audiomsg.py 94388048 /Users/ivan/Downloads/bbae553bfe.mp3
    Отправка в: 94388048

Получить токен можно тут: <http://oauth.vk.com/authorize?client_id=2685278&display=mobile&redirect_uri=https://oauth.vk.com/blank.html&scope=725086&response_type=token&v=5.101&revoke=1>

Чтобы не вводить каждый раз __python3 audiomsg.py__, можно создать alias под удобным именем в скрипте инициализации вашего интерпретатора (для __audiomsg.py__, лежащего в корне домашней папки, и интерпретатора bash, в конец __~/.bashrc__ добавить __alias audiomsg="python3 ~/audiomsg.py"__).

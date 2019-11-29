import vk_api
import sys
import random
import time

ACCESS_TOKEN = ""

file = []
audio_ids = []
chat_id=0

if len(sys.argv) == 1:
    print("usage: python3 audiomsg.py [ACCESS_TOKEN] [DIALOG SEARCH STRING] [[@]CHAT_ID] [FILE1] [FILE2] ... [FILEN]")
    exit()

try:
    if sys.argv[1][0] == "@":
        int(sys.argv[1][1:])
    else:
        int(sys.argv[1])
    sys.argv=sys.argv[1:]
except ValueError:
    if len(sys.argv[1]) > 50:
        try:
            int(sys.argv[1],base=16)
            ACCESS_TOKEN = sys.argv[1]
            sys.argv=sys.argv[2:]
        except ValueError:
            pass
    else:
        sys.argv=sys.argv[1:]
vk_session = vk_api.VkApi(token=ACCESS_TOKEN)
vk = vk_session.get_api()
upload = vk_api.upload.VkUpload(vk)
try:
    if sys.argv[0][0] == "@":
        int(sys.argv[0][1:])
    else:
        int(sys.argv[0])
    chat_id = sys.argv[0]
except ValueError:
    c = vk.messages.getConversations(count=50,extended=1,fields="first_name,last_name")
    p = []
    g = []
    try:
        p = c['profiles']
    except KeyError:
        pass
    try:
        g = c['groups']
    except KeyError:
        pass
    c = c['items']
    conversations = {}
    for i in c:
        if i['conversation']['peer']['type'] == "user" or i['conversation']['peer']['type'] == "group":
            conversations[i['conversation']['peer']['id']]=""
        elif i['conversation']['peer']['type'] == "chat":
            conversations[i['conversation']['peer']['id']]=i['conversation']['chat_settings']['title']
    for i in p:
        if i['id'] in conversations:
            conversations[i['id']] = i['first_name'] + " " + i['last_name']
    for i in g:
        if -i['id'] in conversations:
            conversations[-i['id']] = i['name']
    conversations = {j.lower(): i for i, j in conversations.items()}
    count = 0
    chat_id = 0
    for i, j in conversations.items():
        if i.find(sys.argv[0].lower()) != -1:
            chat_id = j
            count+=1
    if count == 0:
        print("Диалог не найден.")
        exit()
    elif count == 1:
        print("Отправка в", chat_id)
        chat_id = str(chat_id)
    else:
        print("Больше одного совпадения.")
        exit()

for i in range(1,len(sys.argv)):
    file.append(sys.argv[i])

for i in file:
    re = upload.audio_message(i)['audio_message']
    audio_ids.append("doc" + str(re['owner_id']) + "_" + str(re['id']))
if chat_id[0] == "@":
    for i in audio_ids:
        while True:
            try:
                vk.messages.send(chat_id=chat_id[1:], attachment=i,random_id=random.getrandbits(64))
            except vk_api.exceptions.Captcha:
                time.sleep(2)
                continue
            break
        time.sleep(0.7)
else:
    for i in audio_ids:
        while True:
            try:
                vk.messages.send(peer_id=chat_id, attachment=i,random_id=random.getrandbits(64))
            except vk_api.exceptions.Captcha:
                time.sleep(2)
                continue
            break
        time.sleep(0.7)
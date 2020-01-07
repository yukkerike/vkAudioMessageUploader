import vk_api
import sys
import random
import time
import os

ACCESS_TOKEN = ""

vk = upload = None

def sendAudio(peer_id, files):
    print("Отправка в:", peer_id)
    audio_ids = []
    for i in files:
        re = upload.audio_message(i)['audio_message']
        audio_ids.append("doc" + str(re['owner_id']) + "_" + str(re['id']))
    for i in audio_ids:
        while True:
            try:
                vk.messages.send(peer_id=peer_id, attachment=i,random_id=random.getrandbits(64))
            except vk_api.exceptions.Captcha:
                time.sleep(2)
                continue
            break
        time.sleep(0.7)

def parseArgs(args):
    searchSequence = ""
    files = []
    peer_id = 0
    if args[0].find(".py"):
        args=args[1:]
    for i in args:
        if isToken(i):
            authorize(i)
        elif isID(i):
            peer_id = i
        elif isFile(i):
            files.append(i)
        else:
            if i[0] == "@":
                peer_id = 2000000000 + int(i[1:])
            else:
                searchSequence += i + " "
    searchSequence = searchSequence[:-1]
    if searchSequence and not peer_id:
        peer_id = searchForId(searchSequence)
        if peer_id == True:
            print("Больше одного совпадения.")
            exit()
        elif peer_id == False:
            print("Диалог не найден.")
            exit()
    elif not searchSequence and not peer_id:
        peer_id = vk.users.get()[0]['id']
    return(peer_id, files)

def authorize(ACCESS_TOKEN):
    global vk, upload
    vk_session = vk_api.VkApi(token=ACCESS_TOKEN)
    vk = vk_session.get_api()
    upload = vk_api.upload.VkUpload(vk)

def isToken(s):
    try:
        int(s)
        return False
    except ValueError:
        try:
            int(s,16)
            return True
        except ValueError:
            return False


def isFile(s):
    return os.path.isfile(s)

def isID(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

def searchForId(s):
    s = s.lower()
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
            conversations[i['conversation']['peer']['id']]=i['conversation']['chat_settings']['title'].lower()
    for i in p:
        if i['id'] in conversations:
            conversations[i['id']] = (i['first_name'] + " " + i['last_name']).lower()
    for i in g:
        if -i['id'] in conversations:
            conversations[-i['id']] = i['name'].lower()
    count = 0
    peer_id = 0
    for i, j in conversations.items():
        if j.find(s) != -1:
            peer_id = i
            count += 1
    if count == 0:
        return False
    elif count == 1:
        return peer_id
    else:
        return True

if __name__ == "__main__":
    if ACCESS_TOKEN != "":
        authorize(ACCESS_TOKEN)
    sendAudio(*parseArgs(sys.argv))

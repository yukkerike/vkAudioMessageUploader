#!/usr/bin/env python3

import os
import random
import sys
import time

import vk_api
from vk_api.upload import VkUpload

ACCESS_TOKEN = ""  # Вставьте свой токен
vk_session = vk = upload = None

def send_audio(peer_id: int, files: list[str]) -> None:
    print(f"Получатель: {peer_id}")
    audio_ids = []
    files_count = len(files)
    success_count = 0

    print(f"Выгрузка [0/{files_count}]", end="")
    symbols_to_flush = len(str(files_count)) + 3
    faulty_files = []
    for i, file_path in enumerate(files):
        success_count += 1
        print("\b" * symbols_to_flush + f"{success_count}/{files_count}]", end="", flush=True)
        try:
            response = upload.audio_message(file_path)["audio_message"]
            audio_ids.append(f"doc{response['owner_id']}_{response['id']}")
            symbols_to_flush = len(str(success_count) + str(files_count)) + 2
        except Exception:
            faulty_files.append(file_path)
    print()
    if len(faulty_files):
        print("Возникли проблемы с отправкой файлов:", faulty_files)

    audios_count = len(audio_ids)
    success_count = 0
    print(f"Отправка [0/{audios_count}]", end="")
    symbols_to_flush = len(str(audios_count)) + 3
    for i, audio_id in enumerate(audio_ids):
        success_count += 1
        print("\b" * symbols_to_flush + f"{success_count}/{files_count}]", end="", flush=True)
        debounce(lambda p, a: vk.messages.send(peer_id=p, attachment=a, random_id=random.getrandbits(64)), peer_id, i)
        symbols_to_flush = len(str(success_count) + str(files_count)) + 2
        time.sleep(0.7)

    print()

def debounce(f, *args) -> None:
    while True:
        try:
            f(*args)
        except vk_api.exceptions.Captcha:
            time.sleep(2)
            continue
        break

def parse_args(args: list[str]) -> tuple[int, list[str]]:
    search_sequence = ""
    files = []
    peer_id = 0

    for arg in args:
        if get_id(arg):
            peer_id = get_id(arg)
        elif is_token(arg):
            authorize(arg)  # Update vk and upload objects
        elif is_file(arg):
            files.append(arg)
        else:
            search_sequence += arg + " "

    search_sequence = search_sequence.strip()

    if search_sequence and not peer_id:
        peer_id = search_for_id(search_sequence)
        if type(peer_id) is bool:
            print("More than one match found." if peer_id else "Dialogue not found.")
            sys.exit(1)
    elif not peer_id:
        peer_id = vk.users.get()[0]["id"]

    return peer_id, files

def authorize(access_token: str) -> None:
    global vk_session, vk, upload
    vk_session = vk_api.VkApi(token=access_token)
    vk = vk_session.get_api()
    upload = VkUpload(vk)

def is_token(string: str) -> bool:
    return string.startswith("vk") # пришло время отказаться от токенов старого образца

def is_file(path: str) -> bool:
    return os.path.isfile(path)

def get_id(string: str) -> int:
    if string[0] == "@":
        return int(string[1:]) + 2000000000
    return string.isnumeric() and int(string)

def search_for_id(query: str) -> int | bool:
    query = query.lower()
    conversations_response = vk.messages.getConversations(count=50, extended=1, fields="first_name,last_name")
    profiles = conversations_response.get("profiles", [])
    groups = conversations_response.get("groups", [])
    conversations = {}
    for item in conversations_response["items"]:
        peer_type = item["conversation"]["peer"]["type"]
        peer_id = item["conversation"]["peer"]["id"]
        conversations[peer_id] = item["conversation"]["chat_settings"]["title"].lower() if peer_type == "chat" else ""

    for profile in profiles:
        if profile["id"] in conversations:
            conversations[profile["id"]] = (profile["first_name"] + " " + profile["last_name"]).lower()

    for group in groups:
        if -group["id"] in conversations:
            conversations[-group["id"]] = group["name"].lower()

    matched = False
    peer_id = 0
    for id_, name in conversations.items():
        if matched:
            return matched
        matched = query in name
        if matched:
            peer_id = id_
    return matched and peer_id

if ACCESS_TOKEN:
    authorize(ACCESS_TOKEN)

if __name__ == "__main__":
    send_audio(*parse_args(sys.argv[1:]))
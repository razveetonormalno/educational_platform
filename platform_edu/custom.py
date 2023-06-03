import json
import os
import requests


def get_data(group):
    data = {
            'title': None,
            'sidebar': None,
            'content': None,
        }
    if group == "Students":
        a = [('Расписание', '/home/timetable'),
             ('Домашние задания', '/home/homework'),
             ('Группа', '/home/groups')]
        data['sidebar'] = a
    elif group == "Teachers":
        a = [('Расписание', '/home/timetable'),
             ('Домашние задания', '/home/homework'),
             ('Группа', '/home/groups')]
        data['sidebar'] = a
    elif group == "Administrators":
        a = [('Учителя', '/home/admin-teachers/'),
             ('Курсы', '/home/admin-courses/'),
             ('Группы', '/home/admin-groups/')]
        data['sidebar'] = a

    return data

def create_room():
    url = "https://easyedu.metered.live/api/v1/room"

    url_key = url + "?secretKey=Kxy0vx2zjvCvznvdE3r0jiufv2jQglbxh60XsFBi8HSDw2RN"

    payload = {
        "privacy": "public",
        "meetingEndedWebhook": "end",
        "ejectAtRoomExp": False,
        "enableRequestToJoin": True,
        "enableChat": True,
        "enableScreenSharing": True,
        "joinVideoOn": False,
        "joinAudioOn": False,
        "recordRoom": False,
        "audioOnlyRoom": False
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    response = requests.request("POST", url_key, json=payload, headers=headers)
    response_json = json.loads(response.text)
    print(os.path.abspath('.'))

    with open('platform_edu/static/json/rooms.json') as file:
        rooms_data = json.loads(file.read())

    new_room = {
        "roomName": response_json['roomName'],
        'created': response_json['created'],
    }

    rooms_data[response_json['_id']] = new_room
    with open("platform_edu/static/json/rooms.json", 'w') as file:
        file.write(json.dumps(rooms_data))

    return response_json

def delete_room(roomName: str):
    url = f"https://easyedu.metered.live/api/v1/room/{roomName}"
    url_key = url + "?secretKey=Kxy0vx2zjvCvznvdE3r0jiufv2jQglbxh60XsFBi8HSDw2RN"

    headers = {"Accept": "application/json"}

    response = requests.request("DELETE", url_key, headers=headers)
    print(response.text)
    print("=" * 15)

    res = json.loads(response.text)
    return res

def get_room(roomName: str):
    url = f"https://easyedu.metered.live/api/v1/room/{roomName}"
    url_key = url + "?secretKey=Kxy0vx2zjvCvznvdE3r0jiufv2jQglbxh60XsFBi8HSDw2RN"

    headers = {"Accept": "application/json"}

    response = requests.request("GET", url_key, headers=headers)
    print(response.text)
    print("=" * 15)

    res = json.loads(response.text)
    return res
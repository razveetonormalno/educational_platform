import csv
import json
import os
import re
import threading
from functools import wraps
import requests

from .models import *


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


def delete_all_rooms():
    with open('platform_edu/static/json/rooms.json') as file:
        rooms_data = json.loads(file.read())
        for i in rooms_data:
            new_thread = threading.Thread(target=delete_room, args=(rooms_data[i]['roomName'],))
            new_thread.start()


def get_room_(group: str):
    print(group)
    with open("platform_edu/static/json/rooms.json") as file:
        rooms_data = json.loads(file.read())
        for id_, val in rooms_data.items():
            if group in val['group']:
                return id_
    return ""


def get_schedule(row: list):
    group = []
    for day in row:
        if day:
            day = tuple(day.split('&'))
            group.append(day)
        else:
            group.append("")
    return group


def get_all_schedule():
    with open("platform_edu/static/csv/schedule.csv") as file:
        reader = csv.reader(file, delimiter=';')
        reader = list(reader)
        del reader[0]
        result = {}
        for row in reader:
            result[row[0]] = get_schedule(row[1:])
        return result


def get_group_schedule(group_number: str):
    with open("platform_edu/static/csv/schedule.csv") as file:
        reader = csv.reader(file, delimiter=';')
        reader = list(reader)
        del reader[0]
        for row in reader:
            if row[0] == group_number:
                return get_schedule(row[1:])

def to_table_format(func):
    @wraps(func)
    def wrapped(*args, **kwargs):
        res = func(*args, **kwargs)
        max_length = len(max(res, key=len))
        print("MAX >>>", max_length)

        new_res = []
        for j in range(max_length):
            row = []
            for i in range(7):
                if res[i]:
                    try:
                        row.append(res[i][j])
                    except IndexError:
                        row.append(("&nbsp;", "&nbsp;"))
                else:
                    row.append(("&nbsp;", "&nbsp;"))
            new_res.append(row)
        # print("=" * 15)
        # print(new_res)
        # print("=" * 15)

        return new_res
    return wrapped

@to_table_format
def get_for_student(group_number: str):
    schedule = get_group_schedule(group_number)
    print(schedule)
    schedule = list(map(lambda x: list(x), schedule))

    res = []
    teachers_id = {}
    for i, day in enumerate(schedule):
        gr_day = []
        for j, lesson in enumerate(day):
            search = re.search(r'^(\d{2}:\d{2})\((\d+)\)', lesson)
            l_time = search.group(1)
            t_id = search.group(2)

            if t_id not in teachers_id:
                t = Teacher.objects.get(id=t_id)
                name = f"{t.surname} {t.name[0]}. {t.patronymic[0]}."
                teachers_id[t_id] = name

            gr_day.append((l_time, teachers_id[t_id]))
        res.append(tuple(gr_day))

    return res


def get_for_teacher(teacher_id: str):
    res = []

    a = get_all_schedule()
    print(a)
    for group in a:
        print("=" * 15)
        print(group)
        for day in a[group]:
            print(day)
            gr_day = []
            for lesson in day:
                search = re.search(r'^(\d{2}:\d{2})\((\d+)\)', lesson)
                l_time = search.group(1)
                t_id = search.group(2)

                if t_id == teacher_id:
                    gr_day.append((l_time, group))

            if gr_day:
                res.append(gr_day)

    print(res)
    return res
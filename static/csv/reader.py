import json
import os
import requests
import threading
import csv
import re

def get_all_schedule():
    with open("schedule.csv") as file:
        reader = csv.reader(file, delimiter=';')
        reader = list(reader)
        del reader[0]
        result = {}
        for row in reader:
            result[row[0]] = get_schedule(row[1:])
        return result

def get_schedule(row: list[str]):
    group = []
    for day in row:
        if day:
            day = tuple(day.split('&'))
            group.append(day)
        else:
            group.append("")
    return group

def get_group_schedule(group_number: str):
    with open("schedule.csv") as file:
        reader = csv.reader(file, delimiter=';')
        reader = list(reader)
        del reader[0]
        for row in reader:
            if row[0] == group_number:
                return get_schedule(row[1:])

def get_for_student(group_number: str):
    schedule = get_group_schedule(group_number)
    res = []

    teachers_id = set()
    for day in schedule:
        for lesson in day:
            a = re.search(r'\(\d+\)', lesson)
            teachers_id.add(a[0][1:-1])
    teachers_id = list(teachers_id)
    # teachers = Teacher.objects.in_bulk(teachers_id)
    return res

if __name__ == '__main__':
    print(get_all_schedule())
    print(get_group_schedule("4312"))
    get_for_student("4312")
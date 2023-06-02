def get_data(group):
    data = {
            'title': None,
            'sidebar': None,
            'content': None,
        }
    if group == "Student":
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

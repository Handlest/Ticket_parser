import pathlib
import datetime
import matplotlib.pyplot as plt


def show_ticket_dict(dictionary):
    for key in dictionary:
        tmp = dictionary[key]  # Массив на 10 массивов внутри
        print(key, '\nБилет ', end='')
        print(*tmp, sep='\nБилет ')
        print()
    print('*'*60)


def refactor_files(list_of_files):
    for file in list_of_files:
        with open(file, 'r', encoding='utf-8') as f:
            arr = f.readlines()
        for i in range(len(arr)):
            arr[i] = arr[i].replace(' ', '').replace(' ', '')
        with open(file, 'w', encoding='utf-8') as f:
            f.writelines(arr)


def get_key_name(filename):
    filename = str(filename)
    filename = filename.split('_')
    return str(filename[0] + '_at_' + filename[1] + '_for_' + filename[3][:5])


def get_files_list():
    currentDirectory = pathlib.Path('.')
    list_of_files = []
    for currentFile in currentDirectory.iterdir():
        if str(currentFile).split('.')[-1] == 'txt' and str(currentFile).split('.')[0] != 'tmp':
            list_of_files.append(currentFile)
    return list_of_files


def get_tickets(filename):
    ticket_list = [[] for _ in range(10)]
    counter = 0
    with open(filename, 'r', encoding='utf-8') as file:
        line = file.readline().strip('\n')
        while line != '':
            if line == '\n':
                counter += 1
            if '₽' in line:
                ticket_list[counter].append(line.strip('\n'))  # Цена
                flight_time = file.readline().strip('\n') # Время вылета
                file.readline()
                ticket_list[counter].append(file.readline().strip('\n') + ' ' + flight_time) # Дата вылета и время
                ticket_list[counter].append(file.readline().strip('\n')) # Время в пути
                flight_time = file.readline().strip('\n') # Время прибытия
                file.readline()
                ticket_list[counter].append(file.readline().strip('\n') + ' ' + flight_time) # Дата прибытия и время
            line = file.readline()
    return ticket_list


def form_dictionary():
    files_lst = get_files_list()
    refactor_files(files_lst)
    amount_of_keys = len(files_lst)
    dictionary = dict()
    for i in range(amount_of_keys):
        dictionary[get_key_name(files_lst[i])] = get_tickets(files_lst[i])
    return dictionary


def get_date_for_url(offset_from_today: int):
    ordinal_date = datetime.date.toordinal(datetime.date.today())
    result = str(datetime.date.fromordinal(ordinal_date + offset_from_today)).split('-')
    return result[2] + result[1]


def generate_graph_from_dict(dictionary: dict):
    lists_of_tickets = []
    for date, info in dictionary.items():
        lists_of_tickets.append(info)
    list_of_prices = []
    list_of_dates = []
    for lst in lists_of_tickets:
        counter = 1
        for lst1 in lst:
            list_of_prices.append(int(lst1[0][:-1]))
            list_of_dates.append(lst1[1].split(',')[0] + str(counter))
            counter += 1
            print(lst1)
    plt.figure(figsize=(50, 5))
    plt.scatter(list_of_dates, list_of_prices)
    plt.grid(True)
    plt.plot(list_of_dates, list_of_prices)
    plt.show()

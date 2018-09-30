import csv


def inputReader(inputCsv):
    with open(inputCsv, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        inputRead = []
        for row in spamreader:
            inputRead.append(row)
    return inputRead


def defineDict(inputData):
    file = open(inputData)
    lines = file.readlines()
    dictionary = []
    for i in lines:
        i = i.replace('\n', '')
        dictionary.append(i)
    return dictionary


def buildDict(keys, values):
    dictionary = []
    for value in values:
        dictionary.append(dict(zip(keys, value)))
    return dictionary


'''ENTRY-POINT'''


def build():
    keys = defineDict('./file/inputHeading.txt')
    values = inputReader('./file/input.csv')
    return buildDict(keys, values)


def field_filter(dictionary, field, attribute):
    return [i for i in dictionary if i[field] == attribute]

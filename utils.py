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
    values = inputReader('./file/input_long.csv')
    return buildDict(keys, values)


def field_filter(dictionary, field, attribute):
    return [i for i in dictionary if i[field] == attribute]


def find_field_attribute(field, dictionary):
    tmp = []
    count = 0
    for obj in dictionary:
        tmp.append(obj[field])
    obj = {field: set(tmp)}
    return obj


built = build()
dimension = len(built)
over50k = 0
under50k = 0


for att in list(find_field_attribute('race', built).values()):
    for i in att:
        print(i)
        over50k = 0
        under50k = 0
        for j in built:
            if j['race'] == i:
                if j['result'] == '>50K':
                    over50k = over50k + 1
                else:
                    under50k = under50k + 1
        print("VALUE:" + str(i) + ", OVER 50K: " +
              str(over50k) + ", UNDER 50K: " + str(under50k) + ", TOTAL: " + str(over50k + under50k) + " TASSO OVER 50K: " +
              str(float(over50k)/(float(over50k) + float(under50k))) + " TASSO UNDER 50K: " +
              str(float(under50k)/(float(over50k) + float(under50k))))
        print("********")

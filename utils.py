import csv
import pandas as pd

'''def input_reader(inputCsv):
    with open(inputCsv, 'rb') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        inputRead = []
        for row in spamreader:
            inputRead.append(row)
    return inputRead

def define_dict(inputData):
    file = open(inputData)
    lines = file.readlines()
    dictionary = []
    for i in lines:
        i = i.replace('\n', '')
        dictionary.append(i)
    return dictionary
'''
def build_dict(keys, values):
    dictionary = []
    for value in values:
        dictionary.append(dict(zip(keys, value)))
    return dictionary

def build(keys, values):
    return build_dict(keys, values)

def field_filter(dictionary, field, attribute):
    return [i for i in dictionary if i[field] == attribute]

def find_field_attribute(field, dictionary):
    tmp = []
    count = 0
    for obj in dictionary:
        print(field)
        tmp.append(obj[field])
    obj = {field: set(tmp)}
    return obj

def column_reader(fileName):
    file = open(fileName)
    lines = file.readlines()
    dictionary = []
    for i in lines:
        i = i.replace('\n', '')
        dictionary.append(i)
    return dictionary

'''input: csvFile = path al file csv che contiene i dati da mappare
          headingFile = path al file txt che contiene il nome dei campi del file csv'''
def field_mapping(csvFile, headingFile):
    fields = column_reader(headingFile)
    df = pd.read_csv(csvFile, skipinitialspace=True, usecols=fields)
    mapped_fields = []
    obj = {}
    for column in df:
        if(len(set(df.loc[: , column]))<=10):
            obj = {column: {}}
            for i in list(set(df.loc[: , column])):
                obj[column].update({list(set(df.loc[: , column])).index(i): i})
            mapped_fields.append(obj)
    return mapped_fields


def data_transofmation(inputHeading, inputCsv):
    fields = column_reader(inputHeading)
    df = pd.read_csv(inputCsv, skipinitialspace=True, usecols=fields)
    mappedFields = field_mapping(inputCsv, inputHeading)
    for column in df:
        for current_field in mappedFields:
            if(list(set(current_field))[0] == column):
                for element in df.loc[: , column]:
                    for i in list(current_field.values()):
                        if(element in i.values()):
                            df.loc[df[column] == element, column] = list(i.keys())[list(i.values()).index(element)]
    return df

df = data_transofmation('./file/inputHeading_loan.txt', './file/Loan_payments_data.csv')
correlation = df.corr('pearson')
print(correlation)
                        
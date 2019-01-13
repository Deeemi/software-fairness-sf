import csv
import pandas as pd
import numpy as numpy

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
        if(len(set(df.loc[: , column]))<=50):
            obj = {column: {}}
            for i in list(set(df.loc[: , column])):
                obj[column].update({list(set(df.loc[: , column])).index(i): i})
            mapped_fields.append(obj)
    return mapped_fields


def data_transofmation(inputHeading, inputCsv):
    print("The software is mapping the datas")
    fields = column_reader(inputHeading)
    df = pd.read_csv(inputCsv, skipinitialspace=True, usecols=fields)
    categories = list(df.columns.values)
    for column in categories:
        df[column] = df[column].astype('category')
        cat_columns = df.select_dtypes(['category']).columns
        df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)
    print("Mapping complete!")
    return df

def find_dag(datafame, field, fields):
    print("The software is finding the maximum correlation for "+ field)
    returnVal = ""
    if(len(fields) == 0):
        return returnVal
    max = -1
    for j in correlation:        
        if(correlation[field][j]>max):
            if(j != field):
                max = correlation[field][j]
                max_field = j
                returnVal = dict({"field_1": field, "field_2": max_field, "correlation": max})
            else:
                continue
    return returnVal


datas = data_transofmation('./file/inputHeading.txt','./file/input_long.csv' )
print("Start analizing the dataset...")

print('-----PEARSON-----')
correlation = datas.corr('pearson')
fields = []
for field in correlation:
    fields.append(field)
casual_dag = []

first_node = find_dag(correlation, "result", fields)
casual_dag.append(first_node["field_1"])
field = first_node["field_2"]
datas.drop("result", axis = 1, inplace=True)
fields.remove("result")
i = len(fields)

while len(fields)>=2: 
    correlation = datas.corr('kendall')
    node = find_dag(correlation, field, fields)
    casual_dag.append(node["field_1"])
    field = node["field_2"]
    datas.drop(node["field_1"], axis = 1, inplace=True)
    fields.remove(node["field_1"])

casual_dag.append(fields[0])
result_string = ""

for i in casual_dag:
    result_string = result_string + "-->" + i

result_string = result_string.replace("-->", "", 1)

print("Finish!")
print("The casual dag computet using correlation is: ")
print(result_string)

print('-----KENDALL-----')
datas = data_transofmation('./file/inputHeading.txt','./file/input_long.csv' )
print("Start analizing the dataset...")
correlation = datas.corr('kendall')
fields = []
for field in correlation:
    fields.append(field)
casual_dag = []

first_node = find_dag(correlation, "result", fields)
casual_dag.append(first_node["field_1"])
field = first_node["field_2"]
datas.drop("result", axis = 1, inplace=True)
fields.remove("result")
i = len(fields)

while len(fields)>=2: 
    correlation = datas.corr('kendall')
    node = find_dag(correlation, field, fields)
    casual_dag.append(node["field_1"])
    field = node["field_2"]
    datas.drop(node["field_1"], axis = 1, inplace=True)
    fields.remove(node["field_1"])

casual_dag.append(fields[0])
result_string = ""

for i in casual_dag:
    result_string = result_string + "-->" + i

result_string = result_string.replace("-->", "", 1)

print("Finish!")
print("The casual dag computet using correlation is: ")
print(result_string)

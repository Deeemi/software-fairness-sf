import csv
import pandas as pd
import numpy as numpy
import requests

pd.options.mode.chained_assignment = None

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


def find_dependencies(df, first_field, fields, value):
    df_in = df.loc[df[first_field] == value]
    mapping = []
    max = 0
    return_value = {}
    for field in fields:
        if field != first_field:
            tmp = pd.crosstab(df_in[first_field],df_in[field])
            somma = tmp.sum(axis = 0)
            for b in tmp:
                for a in tmp.index:
                    if tmp[b][a]*len(df_in[field].unique()) == max and max != 0:
                        '''print(return_value["field2"] + " e " +field+ " sono uguali")'''
                    if tmp[b][a]*len(df_in[field].unique())>max:
                        max = tmp[b][a]*len(df_in[field].unique())
                        return_value = {"field2": field, "field1": first_field, "value1": a, "value2": b, "total": tmp[b][a], "count": tmp[b][a]*len(df_in[field].unique())}
                    '''mapping.append({"field2": "result", "field1": field, "value1": a, "value2": b, "total": tmp[a][b], "count": tmp[a][b]/somma[a]})'''
    return return_value
    '''return find_dependencies(df.drop(field, axis=1, inplace = True), return_value["field2"], fields)'''


inputCsv = "./file/input_long.csv"
fields = column_reader("./file/inputHeading.txt")
df = pd.read_csv(inputCsv, skipinitialspace=True, usecols=fields)
dag = []
current_field = ""
df_in = df.loc[df['result'] == '<=50K']
node = find_dependencies(df_in, 'result', fields, '<=50K')
dag.append(node)
df_in.drop('result', axis=1, inplace = True)
current_field = node["field2"]
value = node["value2"]
fields.remove('result')
df_in = df_in.loc[df_in[node["field2"]] == node["value2"]]

i = len(fields)

while i>=2:
    node = find_dependencies(df_in, current_field, fields, value)
    dag.append(node)
    df_in.drop(node["field1"], axis=1, inplace = True)
    df_in = df_in.loc[df_in[node["field2"]] == node["value2"]]
    current_field = node["field2"]
    value = node["value2"]
    fields.remove(node["field1"])
    i = i-1

    if(bool(node) == False):
        break
new_count = 0

for j in dag:
    new_count = j["count"]/len(df[j["field2"]].unique())/len(df.index)
    conditional_prob = df.groupby(["result"])[j["field2"]].value_counts() / df.groupby(["result"])[j["field2"]].count()
    j["count"] = new_count
    j["odds-ratio"] = (conditional_prob.loc["<=50K"][j["value2"]]/(1- conditional_prob.loc["<=50K"][j["value2"]]))/(conditional_prob.loc[">50K"][j["value2"]]/(1- conditional_prob.loc[">50K"][j["value2"]]))
    print(j)
    print("-----")

first = True
result_string = ""
for c in dag:
    if first == True:
        result_string = c["field1"]+": "+ str(c["value1"])
        first = False
    else:
        result_string = result_string + "--->" + c["field1"]+": "+ str(c["value1"]) 
        last = c 

result_string = result_string + "--->" + last["field1"]+": "+ str(last["value1"]) 
print(result_string)


'''NEXT LINES ARE WORK IN PROGRESS'''
fields = column_reader('./file/inputHeading.txt')
correlation_datas = pd.read_csv('./file/input_long.csv', skipinitialspace=True, usecols=fields)

print("Start analizing the dataset...")

print('-----PEARSON-----')
pearson_correlation = correlation_datas.corr('pearson')
for i in pearson_correlation:
    max = -1
    print("-----")
    tmp = pearson_correlation[i]
    for j in pearson_correlation[i]:
        if(j == 1):
            j = 0
            tmp[i] = 0
        if (j>max):
            max_row = str(tmp[i])
            max = j
    print(tmp)
    print("-----")
    print(max_row)
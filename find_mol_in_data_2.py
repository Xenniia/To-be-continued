import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt

# open data in the required format. if you have pdb or cif format file, convert to txt

def create_dataframe_from_file(path):

#Create new txt file from data txt file with necessary data

    a = open(path)
    b = []
    for i in a:
        if i.startswith('ATOM') or i.startswith('HETATM'):
            b.append(i.replace('\n', ''))
    d = pd.DataFrame(data=b, columns=['B'])

#Find number of data columns for dataframe, create dataframe

    v = [i for i in d.B[0].split(' ') if i != '']
    number_columns = len(v)
    name_columns = [ii for i, ii in enumerate('abcdefghijklmnopqrstuvwxyz') if i < number_columns]
    d[name_columns] = d.pop('B').str.split(n=number_columns, expand=True)

#find colums with coordinate

    d = d.convert_dtypes()
    name_coor = []
    for i in d.columns:
        if len(name_coor) < 3:
            if len(d[i][0]) >= 5 and d[i][0] not in ['ATOM', 'HETATM']:
                name_coor.append(i)


    d[name_coor] = d[name_coor].astype(float).round(3)
    d.columns = [i for i in ''.join(d.columns).replace(''.join(name_coor), 'xyz')]

#find colum with names of atoms:

    if len(set(d[d.columns[2]])) >= len(set(d[d.columns[3]])):
        name_atoms = d.columns[2]
    else:
        name_atoms = d.columns[3]
    d = d.rename({name_atoms:'name_atoms'}, axis='columns')
    return d

#finding the distances between all atoms
def get_distances(data):
    data = data.reset_index()
    name_distances = []
    distances = []
    for ii in range(len(data)-1):
       for i in range(len(data)-1):
           dist = math.hypot(data.x[ii] - data.x[i + 1], data.y[ii] - data.y[i + 1], data.z[ii] - data.z[i + 1])
           name_distances.append(f'{data.name_atoms[ii]} - {data.name_atoms[i + 1]}')
           distances.append(round(dist, 1))

    distances_table = pd.DataFrame({'name_distances': name_distances, 'distances': distances})
    return distances_table

path = input('Enter the path of your data:')[1:-1]
data = create_dataframe_from_file(path)
distans_table_data = get_distances(data)

path = input('Enter the path of molecule for finding:')[1:-1]
data_find = create_dataframe_from_file(path)
distans_table_find_mol = get_distances(data_find)

# checking molecule in all data



#representation of the found molecule

def show_mol(data, data_find):

    x = data.x
    y = data.y
    z = data.z

    x2 = data_find.x
    y2 = data_find.y
    z2 = data_find.z

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(x, y, z, s=10, c='g',marker='o',  label='data')
    ax.scatter(x2, y2, z2,s = 50, c='r', marker='o',  label='find molecule')
    ax.set_title('found molecule in all data ')
    plt.legend()
    plt.show()

# show_mol(data, data_find)
def ceck_molecule(all_data, find_data, error):
    all_data = all_data.reset_index()
    find_data = find_data.reset_index()
    sum_find = 0

    for i, ii in enumerate(find_data.name_distances):
        for j, jj in enumerate(all_data.name_distances):
            if ii == jj and find_data.distances[i] - error <= all_data.distances[j] <= find_data.distances[i] + error:
                sum_find += 1
                break

    if sum_find >=len(find_data):
        return 'Molecule found! Look at this', show_mol(data, data_find)
    else:
        return 'No this molecule'

print(ceck_molecule(distans_table_data, distans_table_find_mol, 1))
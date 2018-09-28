import os
import glob
import pandas as pd
import numpy as np
import csv

file_list = glob.glob('*.txt')
temp_list = []

with open('taxa_list.csv', 'rb') as file:
	taxa_list = file.read()

taxa_list = taxa_list.split(',')

for file in file_list:
	taxa_matrix = pd.read_table(file, header=None, index_col=False, sep='\t')
	taxa_matrix.columns = ['taxa', 'count']
	temp_list.append(taxa_matrix)

taxa_matrix = pd.DataFrame()
taxa_matrix['taxa'] = taxa_list


for i in temp_list:
	taxa_matrix = taxa_matrix.merge(i, how='left', on='taxa')

colnames = ['taxa'] + file_list
taxa_matrix.columns = colnames

taxa_matrix = taxa_matrix.transpose()
taxa_matrix.to_csv('taxa_matrix.csv')

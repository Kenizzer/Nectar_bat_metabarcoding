import os
import glob
import pandas as pd
import numpy as np
import csv

X = glob.glob('*_all-ex.txt')

with open('taxa_list.csv', 'rb') as file:
	Wordlist = file.read()

Wordlist = Wordlist.split(',')

lodf = []
for t in X:
	df = pd.read_table(t, header=None, index_col=False, sep='\t')
	df.columns = ['word', 'count']
	lodf.append(df)


print(len(lodf))
print(lodf[0].head())

#df.to_csv("temp.csv", sep='\t')

df = pd.DataFrame()
df['word'] = Wordlist
#print(df.head())

for i in lodf:
	df = df.merge(i, how='left', on='word')

#print(df.head())

colnames = ['word'] + X
df.columns = colnames

df = df.transpose()
df.to_csv('df.csv')

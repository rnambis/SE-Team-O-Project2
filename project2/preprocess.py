import pandas as pd
import sys

#filename=sys.argv[0]
df=pd.read_csv('teamp.csv')

#Used to sort rows based on issue_id
df=df.sort_values(by='issue_id', ascending = True)

#Used to replace [] by 'None'
def change(s):
	if s == '[]':
		s='None'
	else:
		pass
	return s


no_of_col = len(df.columns)

for column in df.columns:
	df[column]=[change(x) for x in df[column]]


# name=filename.split('.')[0]

# modified_name = name+"processed.csv"

df.to_csv('teampmodified.csv',sep=',')
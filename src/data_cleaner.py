import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer

data = pd.read_csv('Data\\raw\\dup.csv')
data.dtypes
def Handeling_null(output_file):
    data = pd.read_csv(output_file)
    missing_col = []
    for column in data:
        if data[column].dtype == np.number and data[column].isnull().any():
            missing_col.append(column)
        else:
             data = data[data[column].notna()]
    print(missing_col)
    for col in missing_col:
        imputer = SimpleImputer(strategy='mean')
        imputer.fit(data[[col]])
        data[[col]] = imputer.transform(data[[col]])
  
    data.to_csv(output_file,index= False)



def Remove_duplicate(output_file):
    data = pd.read_csv(output_file)
    data.drop_duplicates(inplace=True)
    data.to_csv(output_file,index= False)
    
    
    
def round_values(output_file):
    data = pd.read_csv(output_file)
    for var in data:
        if data[var].dtype == np.number:
            round(data[var],2)
    data.to_csv(output_file,index=False)
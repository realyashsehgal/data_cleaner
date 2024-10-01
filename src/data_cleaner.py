import pandas as pd
import numpy as np
from sklearn.impute import SimpleImputer
def clean_data(input_file, output_file):
    data = pd.read_csv(input_file)
    
    data.drop_duplicates(inplace=True)
    missing_col = []
    for column in data:
        if data[column].dtype == np.number and data[column].isnull().any():
            missing_col.append(column)
            print("hell")
            print(data[column])
    print(missing_col)
    for col in missing_col:
        imputer = SimpleImputer(strategy='mean')
        imputer.fit(data[[col]])
        data[[col]] = imputer.transform(data[[col]])
  
    data.to_csv(output_file,index= False)
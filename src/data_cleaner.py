import pandas as pd
def clean_data(input_file, output_file):
    data = pd.read_csv(input_file)
    
    data.drop_duplicates(inplace=True)
    
    
    data.fillna(data.mean(),inplace=True)
    print("data claend")
    data.to_csv(output_file,index= False)
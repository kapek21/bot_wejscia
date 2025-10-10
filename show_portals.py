import pandas as pd
df = pd.read_excel('../portale.xlsx', header=None)
print('PORTALE:')
for i, row in df.iterrows():
    print(f'{i+1}. {row[0]} - {row[1]}')


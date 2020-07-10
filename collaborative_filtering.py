import pandas as pd
import numpy as np

#Use specified file path and make day a date format
df_s = pd.read_csv('csv_file.csv')

#Create pivot table of number of purchases of each product by customers
cp = df_s.groupby(['cust_id', 'product_title'], as_index = False).agg({"date":"count"})

cp_pivot = cp.pivot(columns='product_title',index = 'cust_id',values='date')

#Create similarity function
def get_similarity(df, p1, p2):
    df = df.replace(np.nan, 0)
    df[df>0] = 1
    df['sum'] = df[p1] + df[p2]
    df['ints'] = df['sum']-1
    df[df<0] = 0
    intersection = np.sum(df['ints'])

    union = np.count_nonzero(df['sum'])
    if union > 0:
        sim = intersection / union
    else:
        sim = 0
    return sim

#Create matrix using similarity function between each product pair
def create_sim_table(df):
    ind = df.columns
    cols = df.columns
    st = pd.DataFrame(columns = cols, index = ind)
    for i in st.index:
        for c in st.columns:
            st.loc[i,c] = get_similarity(df,i,c)
    return st

sim_df = create_sim_table(cp_pivot)

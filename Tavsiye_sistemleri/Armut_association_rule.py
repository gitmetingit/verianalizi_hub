import  pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', '{:,.2f}'.format)

df_=pd.read_csv(r"Tavsiye_sistemleri/datasets/armut_data.csv")
df=df_.copy()

df.head(10)
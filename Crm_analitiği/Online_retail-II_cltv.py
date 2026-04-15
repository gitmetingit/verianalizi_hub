import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

pd.ExcelFile('Crm_analitiği/datasets/online_retail_II.xlsx').sheet_names
df_=pd.read_excel('Crm_analitiği/datasets/online_retail_II.xlsx',sheet_name=2010-2011)#['Year 2009-2010', 'Year 2010-2011']
df=df_.copy()
df.head()
df['Customer ID']=df['Customer ID'].astype(int)
df.dropna(inplace=True)
df=df[~df['StockCode'].astype(str).str.contains('C',na=False)]
df=df[df['Quantity']>0]
df['TotalPrice']=df['Quantity']*df['Price']
df['InvoiceDate'].max() #Timestamp('2010-12-09 20:01:00')
today_date =dt.datetime(2010,12,11)
cltv_c=df.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                               'Quantity': lambda x : x.sum(),
                               'TotalPrice': lambda x: x.sum()
                              })

#total_transaction:(toplam işlem sayısı) her bir müşterinin fatura sayısı\alışveriş sayısı\frequency
#total_unit:(toplam ürün sayısı) her bir müşterinin satın aldığı ürün sayısı
#total_price:(toplam harcama) herbir müşterinin yaptığı toplam harcama\monetary
#avarage_order_value:(toplam harcama/toplam işlem sayısı) herbir müşterinin fatura bazında yaptığı ortalama harcama\ortalama fatura
#purchase_frequency:(toplam işlem sayısı/müşteri sayısı) herbir müşterinin işlem sayısının değerini belirlemeye yarayan katsayı\işlem ağırlık katsayısı
#repeat_rate:(enaz 2 defa gelen müşteri sayısı / tüm müşteri sayısı) sadık müşteri oranı
#churn_rate:müşteri terk oranı
#profit_margin:kar marjı
#customer_value:(ortalama fatura * işlem ağırlık katsayısı) ağırlıklı müşteri değeri
#cltv:((ağırlıklı müşteri değeri/terk oranı) * kar marjı) müşteri yaşam boyu değeri

cltv_c.columns=['total_transaction','total_unit','total_price']
cltv_c['avarage_order_value']=cltv_c['total_price'] / cltv_c['total_transaction']
cltv_c['purchase_frequency']=cltv_c['total_transaction']/cltv_c.shape[0]
repeat_rate = cltv_c[cltv_c['total_transaction']>1].shape[0]/ cltv_c.shape[0]
churn_rate = 1 - repeat_rate
cltv_c['profit_margin'] = cltv_c['total_price'] * 0.10
cltv_c['customer_value']= cltv_c['avarage_order_value'] * cltv_c['purchase_frequency']
cltv_c['cltv']=(cltv_c['customer_value']/churn_rate) * cltv_c['profit_margin']
cltv_c.sort_values(by='cltv',ascending=False)
cltv_c['segments']=pd.qcut(cltv_c['cltv'],4,['D','C','B','A'])
cltv_c.groupby('segments').agg({'cltv':['count','mean','sum']})
cltv_c.to_csv("cltv_c.to_csv")

##########BONUS##########
def create_cltv_c(dataframe,profit=0.10):
    dataframe = dataframe[~dataframe['StockCode'].astype(str).str.contains('C',na=False)]
    dataframe =dataframe[dataframe['Quantity']>0]
    dataframe.dropna(inplace=True)
    dataframe['TotalPrice'] = dataframe['Quantity'] * dataframe['Price']
    cltv_c = dataframe.groupby('Customer ID').agg({'Invoice': lambda x:x.nunique(),
                                                   'Quantity': lambda x:x.sum(),
                                                   'TotalPrice': lambda x:x.sum() })
    cltv_c.columns = ['total_transaction','total_unit','total_price']
    cltv_c['avg_order_value']=cltv_c['total_price']/cltv_c['total_transaction']
    cltv_c['purchase_frequency']=cltv_c['total_transaction']/cltv_c.shape[0]
    repeat_rate = cltv_c[cltv_c['total_transaction']>1].shape[0]/ cltv_c.shape[0]
    churn_rate = 1 - repeat_rate
    cltv_c['profit_margin'] = cltv_c['total_price'] * profit
    cltv_c['customer_value']=cltv_c['avg_order_value'] * cltv_c['purchase_frequency']
    cltv_c['cltv'] = (cltv_c['customer_value']/churn_rate)* cltv_c['profit_margin']
    cltv_c['segments'] = pd.qcut(cltv_c['cltv'],4,['D','C','B','A'])
    return cltv_c

df = df_.copy()
clv = create_cltv_c(df)

clv.head()

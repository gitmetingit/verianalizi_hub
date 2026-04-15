import pandas as pd
import datetime as dt

from Crm_analitiği.FLO_rfm_müşteri_segmentasyonu import seg_map

pd.set_option('display.max_columns', None)
pd.set_option('display.float_format', lambda x: '%.2f' % x)
pd.set_option('display.width', 500)

##########GÖREV1##########
df_=pd.read_excel('Crm_analitiği/datasets/online_retail_II.xlsx',sheet_name=2010-2011)
df=df_.copy()
df.head()
df.info()
df.describe().T

df.isnull().sum()

df.dropna(inplace=True)

df['StockCode'].nunique()

df['StockCode'].value_counts()

df.groupby('StockCode').agg({'Quantity':'sum'}).sort_values(by='Quantity', ascending=False).head()

df['Invoice'].astype(str).str.contains("C").value_counts()
df['StockCode'].astype(str).str.contains("C").value_counts()
df=df[~df['StockCode'].astype(str).str.contains("C")]
df=df[~df['Invoice'].astype(str).str.contains("C")]
#Bazı hücrelerin StockCode bazılarının ise Invoice değişkenlerinde C mevcut

df['TotalPrice']= df['Price'] * df['Quantity']

##########GÖREV2##########
#Recency: Müşterinin yeniliği
#Frequency: Alış-veriş sıklığı
#Monetary: Toplam harcama

df['InvoiceDate'].max()#Timestamp('2011-12-09 12:50:00')
today_date =dt.datetime(2011,12,11)

rfm = df.groupby('Customer ID').agg({'InvoiceDate': lambda date : (today_date-date.max()).days,
                                     'Invoice': lambda x : x.nunique(),
                                     'TotalPrice' : 'sum'
                                    })

rfm.columns=['recency','frequency','monetary']
rfm=rfm[rfm['monetary']>0]
rfm.reset_index(inplace=True)
rfm.head()
rfm['Customer ID']=rfm['Customer ID'].astype(int)

##########GÖREV3##########
rfm['recency_score']=pd.qcut(rfm['recency'],5,[5,4,3,2,1])
rfm['frequency_score']=pd.qcut(rfm['frequency'].rank(method='first') ,5,[1,2,3,4,5])
rfm['monetary_score']=pd.qcut(rfm['monetary'],5,[1,2,3,4,5])

rfm['RF_SCORE'] = rfm['recency_score'].astype(str) + rfm['frequency_score'].astype(str)
rfm['RFM_SCORE']= rfm[['recency_score','frequency_score','monetary_score']].apply(lambda x: ''.join(x.astype(str)),axis=1)
#rfm isteğe bağlı kullandığımız bir yer yok.

##########GÖREV4##########
seg_map = {
            r'[1-2][1-2]':'hibernating',
            r'[1-2][3-4]':'at_Risk',
            r'[1-2]5':'cant_loose',
            r'3[1-2]':'about_to_sleep',
            r'33':'need_attention',
            r'[3-4][4-5]':'loyal_customers',
            r'41':'promising',
            r'51':'new_customers',
            r'[4-5][2-3]':'potential_loyalists',
            r'5[4-5]':'champions'
          }
rfm['SEGMENTS'] =rfm['RF_SCORE'].replace(seg_map,regex=True )

##########GÖREV5##########
rfm.head()
rfm.groupby('SEGMENTS').agg({'monetary':['mean','count',sum],
                              'recency':'mean'}).sort_values(by=('monetary','sum'),ascending=True)

"""   
                            monetary               recency
                     mean     count    sum           mean
SEGMENTS                                             
need_attention        892.31   186  165970.27        52.43
cant_loose           2783.89    63  175385.03       132.97
potential_loyalists  1035.98   484  501415.77        17.42

Ortalaması en yüksek 3 segment
cant_loose  kişi sayısı oldukça az özel ilgi alaka gösterilebilir.Özel hediye gönderilebilir. 
133 gün neredeyse terk edecekler
potential_loyalists alışverişe teşvik amaçlı yeni çıkan ürünlerle alakalı bir hatırlatma mesajı gönderilebilir.
17 gün alışverişe meyilli
need_attention daha önceden beğendiği ürünlerde  %30 ind yada daha önceden beğendiği ürünlerde kampanyalar yapılabilir.
52 gün tehlikeli 2 aydır yoklar

"""


rfm[rfm['SEGMENTS']=='loyal_customers'][['Customer ID']].to_excel("CRM_loyal_customers.xlsx",index =False)

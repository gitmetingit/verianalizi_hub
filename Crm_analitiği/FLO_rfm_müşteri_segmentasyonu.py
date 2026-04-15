import pandas as pd
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format',lambda x: '%.2f' % x )

##########GÖREV1##########
df_=pd.read_csv('Crm_analitiği/datasets/flo_data_20k.csv')
df=df_.copy()

def check_df(dataframe,head=5,quan=False):
    print('########## Head ##########')
    print(dataframe.head(head))
    print('########## Info ##########')
    print(dataframe.info)
    print('########## Dtype ##########')
    print(dataframe.dtypes)
    print('########## NA ##########')
    print(dataframe.isnull().sum())
    print('########## Columns ##########')
    print(dataframe.columns)
    print('########## Quantiles ##########')
    if quan :
        num_cols=dataframe.select_dtypes(include=['number'])
        print(num_cols.quantile([0,0.05,0.25,0.50,0.75,0.95,0.99,1]).T)
check_df(df,head=5,quan=True)

df['total_order_number']=df['order_num_total_ever_online'] +df['order_num_total_ever_offline']
df['customer_total_value']=df['customer_value_total_ever_offline'] + df['customer_value_total_ever_online']

df.head()
df.dtypes
date_columns=df.columns[df.columns.str.contains("date")]
df[date_columns]=df[date_columns].apply(pd.to_datetime)
df.dtypes

df.groupby("order_channel").agg({"master_id":"count",
                                  "total_order_number":["sum","mean"],
                                  "customer_total_value":["sum","mean"]})

df.sort_values(by='customer_total_value',ascending=False)[:10]

df.sort_values(by='total_order_number',ascending=False)[:10]

def veri_hazır(dataframe):
    dataframe['total_order_number'] = dataframe['order_num_total_ever_online'] + dataframe['order_num_total_ever_offline']
    dataframe['customer_total_value'] = dataframe['customer_value_total_ever_offline'] + dataframe['customer_value_total_ever_online']
    date_columns=dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] =dataframe[date_columns].apply(pd.to_datetime)
    return df

veri_hazır(df)

##########GÖREV2##########
#Recency : müşterinin ne kadar yeni olduğu
#Frequency : alışveriş sıklığı
#Monetary : parasal değer

df['last_order_date'].max()
düz_tarih=dt.datetime(2021,6,2)

rfm=pd.DataFrame()
rfm['customer_id']=df['master_id']
rfm['Recency']=(düz_tarih-df['last_order_date']).dt.days
rfm['Frequency']=df['total_order_number']
rfm['Monetary'] = df['customer_total_value']
rfm.head()

sütunlar=['Recency','Frequency','Monetary']
rfm.columns=[col.lower() if col in sütunlar else col for col in rfm.columns ]
rfm.head()

##########GÖREV3##########
rfm["recency_scores"]= pd.qcut( rfm["recency"].rank(method="first") ,5,[5,4,3,2,1])
rfm["frequency_scores"]=pd.qcut(rfm["frequency"].rank(method="first"),5,[1,2,3,4,5])
rfm["monetary_scores"]=pd.qcut(rfm["monetary"],5,[1,2,3,4,5])

rfm.head()
rfm["RF_SCORE"]=rfm["recency_scores"].astype(str) + rfm["frequency_scores"].astype(str)

##########GÖREV4##########
seg_map={r'[1-2][1-2]':'hibernating',
         r'[1-2][3-4]':'at_Risk',
         r'[1-2]5':'cant_loose',
         r'3[1-2]':'about_to_sleep',
         r'33':'need_attention',
         r'[3-4][4-5]':'loyal_customers',
         r'41':'promising',
         r'51':'new_customers',
         r'[4-5][2-3]':'potential_loyalists',
         r'5[4-5]':'champions' }

rfm['RF_SEGMENTS']=rfm["RF_SCORE"].replace(seg_map,regex=True)
rfm.head()

##########GÖREV5##########
rfm.groupby("RF_SEGMENTS").agg({"recency":"mean",
                                "frequency" :"mean",
                                "monetary":"mean"})
df.head()
rfm.head()
rfm_sadık = rfm[rfm["RF_SEGMENTS"].isin(["champions","loyal_customers"])]["customer_id"]
isim_listesi = df[(df["interested_in_categories_12"].str.contains("KADIN")) & (df["master_id"].isin(rfm_sadık))]["master_id"]
isim_listesi.to_csv(r"C:\Users\metin\PycharmProjects\VeriAnalizi\Crm_analitiği\datasets\Yeni_potansiyel_müş.csv",index=False)

rfm_iyi = rfm[rfm["RF_SEGMENTS"].isin(["about_to_sleep","new_customers"])]["customer_id"]
isim_listesi2 = df[(df["interested_in_categories_12"].isin(["ERKEK", "COCUK"])) & (df["master_id"].isin(rfm_iyi))]["master_id"]
isim_listesi2.to_csv(r"C:\Users\metin\PycharmProjects\VeriAnalizi\Crm_analitiği\datasets\Yeni_potansiyel_müş2.csv",index=False)

##########BONUS##########
def rfm_oluştur (dataframe):
    dataframe['total_order_number'] = dataframe['order_num_total_ever_online'] + dataframe[
        'order_num_total_ever_offline']
    dataframe['customer_total_value'] = dataframe['customer_value_total_ever_offline'] + dataframe[
        'customer_value_total_ever_online']
    date_columns = dataframe.columns[dataframe.columns.str.contains("date")]
    dataframe[date_columns] = dataframe[date_columns].apply(pd.to_datetime)

    dataframe['last_order_date'].max()
    düz_tarih = dt.datetime(2021, 6, 2)

    rfm = pd.DataFrame()
    rfm['customer_id'] = dataframe['master_id']
    rfm['Recency'] = (düz_tarih - dataframe['last_order_date']).dt.days
    rfm['Frequency'] = dataframe['total_order_number']
    rfm['Monetary'] = dataframe['customer_total_value']

    sütunlar = ['Recency', 'Frequency', 'Monetary']
    rfm.columns = [col.lower() if col in sütunlar else col for col in rfm.columns]

    rfm["recency_scores"] = pd.qcut(rfm["recency"].rank(method="first"), 5, [5, 4, 3, 2, 1])
    rfm["frequency_scores"] = pd.qcut(rfm["frequency"].rank(method="first"), 5, [1, 2, 3, 4, 5])
    rfm["monetary_scores"] = pd.qcut(rfm["monetary"].rank(method="first"), 5, [1, 2, 3, 4, 5])

    rfm["RF_SCORE"] = rfm["recency_scores"].astype(str) + rfm["frequency_scores"].astype(str)

    seg_map = {r'[1-2][1-2]': 'hibernating',
               r'[1-2][3-4]': 'at_Risk',
               r'[1-2]5': 'cant_loose',
               r'3[1-2]': 'about_to_sleep',
               r'33': 'need_attention',
               r'[3-4][4-5]': 'loyal_customers',
               r'41': 'promising',
               r'51': 'new_customers',
               r'[4-5][2-3]': 'potential_loyalists',
               r'5[4-5]': 'champions'}

    rfm['RF_SEGMENTS'] = rfm["RF_SCORE"].replace(seg_map, regex=True)
    return rfm[["customer_id","recency","frequency","monetary","RF_SCORE","RF_SEGMENTS"]]

rfm_df = rfm_oluştur(df)
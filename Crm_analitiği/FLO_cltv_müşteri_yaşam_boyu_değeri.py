import pandas as pd
import datetime as dt
from lifetimes import GammaGammaFitter
from lifetimes import BetaGeoFitter

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format',lambda x: '%.2f' % x)
##########GÖREV1##########
df_=pd.read_csv("Crm_analitiği/datasets/flo_data_20k.csv")
df=df_.copy()
df.head()

def outlier_thresholds(dataframe,variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range=quartile3-quartile1
    up_limit=quartile3+1.5*interquantile_range
    low_limit=quartile1-1.5*interquantile_range
    return up_limit,low_limit

def replace_with_thresholds(dataframe,variable):
    up_limit,low_limit=outlier_thresholds(dataframe,variable)
    dataframe.loc[(dataframe[variable] < low_limit),variable] =round(low_limit,0)
    dataframe.loc[(dataframe[variable] > up_limit),variable] =round(up_limit,0)

columns=['order_num_total_ever_online','order_num_total_ever_offline',
         'customer_value_total_ever_offline','customer_value_total_ever_online']

for col in columns:
    replace_with_thresholds(df,col)

df['order_num_total'] = df['order_num_total_ever_online']+df['order_num_total_ever_offline']
df['customer_value_total'] = df['order_num_total_ever_online']+df['order_num_total_ever_offline']

df.dtypes
#date_columns = df.columns[df.columns.str.contains("date")]
date_columns = df.select_dtypes(include=['datetime64', 'datetime']).columns

##########GÖREV2##########
df['last_order_date'].max()
analiz_tarihi = dt.datetime(2021,6,2)
df['first_order_date'] = pd.to_datetime(df['first_order_date'])
df['last_order_date'] = pd.to_datetime(df['last_order_date'])

df_cltv=pd.DataFrame()
df_cltv['customer_id']=df['master_id']
df_cltv['recency_cltv_weekly']=(df['last_order_date']-df['first_order_date']).dt.days/7
df_cltv['T_weekly']=(analiz_tarihi-df['first_order_date']).dt.days/7
df_cltv['frequency']=df['order_num_total']
df_cltv['monetary_cltv_avg']=df['customer_value_total'] / df['order_num_total']
df_cltv.head()

##########GÖREV3##########
bgf=BetaGeoFitter(penalizer_coef=0.001)
bgf.fit( df_cltv['frequency'],
         df_cltv['recency_cltv_weekly'],
         df_cltv['T_weekly'] )

df_cltv["exp_sales_3_month"]=bgf.predict(4*3,
                                 df_cltv['frequency'],
                                 df_cltv['recency_cltv_weekly'],
                                 df_cltv['T_weekly'] )

df_cltv["exp_sales_6_month"]=bgf.predict(4*6,
                                         df_cltv['frequency'],
                                         df_cltv['recency_cltv_weekly'],
                                         df_cltv['T_weekly'] )

df_cltv.sort_values(by='exp_sales_3_month',ascending=False)[:10]
df_cltv.sort_values(by='exp_sales_6_month',ascending=False)[:10]

ggf=GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(df_cltv['frequency'],df_cltv['monetary_cltv_avg'])
df_cltv['exp_average_value']=ggf.conditional_expected_average_profit(df_cltv['frequency'],df_cltv['monetary_cltv_avg'])
df_cltv.head()

cltv=ggf.customer_lifetime_value(bgf,
                                 df_cltv['frequency'],
                                 df_cltv['recency_cltv_weekly'],
                                 df_cltv['T_weekly'],
                                 df_cltv['monetary_cltv_avg'],
                                 time=6,
                                 freq='W',
                                 discount_rate=0.01)
df_cltv['cltv']=cltv
df_cltv.sort_values(by = 'cltv',ascending=False)[:20]
bgf.summary
df_cltv['cltv_segment']=pd.qcut(df_cltv['cltv'],4,['D','C','B','A'])
df_cltv.head()

df_cltv[df_cltv['cltv_segment']=='A'].sort_values(by='exp_sales_6_month',ascending=False)[:20]
df_cltv.groupby("cltv_segment").agg({"monetary_cltv_avg":["min","mean","max"],
                                     "exp_sales_3_month":["min","mean","max"],
                                     "exp_sales_6_month":["min","mean","max"],
                                     "exp_average_value":  ["min","mean","max"],
                                     "cltv":["min","mean","max"]}).sort_index(ascending=False)

#İki segment olabilir sanki çünkü B-C-D nin önümüzdeki 6 ay beklentisi bile 2'den  küçükoysaki  A nın neredeyse 9,5
#A ve diğerleri dersek A'ya sadakat programı kpsamında ücretsiz kargo yeni çıkan ürünlerden 24 saat önce haber verilmesi vb. ayrıcalıklar.
#B için 48 saat tanımlı indirim çekleri gibi uygulamalar yapılabilir.

##########BONUS##########
import pandas as pd
import datetime as dt
from lifetimes import GammaGammaFitter
from lifetimes import BetaGeoFitter

# Görüntü ayarları
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.2f' % x)


# 1. YARDIMCI FONKSİYONLAR (En üstte tanımlanmalı)
def outlier_thresholds(dataframe, variable):
    quartile1 = dataframe[variable].quantile(0.01)
    quartile3 = dataframe[variable].quantile(0.99)
    interquantile_range = quartile3 - quartile1
    up_limit = quartile3 + 1.5 * interquantile_range
    low_limit = quartile1 - 1.5 * interquantile_range
    return up_limit, low_limit


def replace_with_thresholds(dataframe, variable):
    up_limit, low_limit = outlier_thresholds(dataframe, variable)
    dataframe.loc[(dataframe[variable] < low_limit), variable] = round(low_limit, 0)
    dataframe.loc[(dataframe[variable] > up_limit), variable] = round(up_limit, 0)


# 2. ANA CLTV FONKSİYONU
def create_cltv_df(dataframe):
    # Orijinal veriyi bozmamak için kopya alıyoruz
    df_ = dataframe.copy()

    # Aykırı değer baskılama
    columns = ["order_num_total_ever_online", "order_num_total_ever_offline",
               "customer_value_total_ever_offline", "customer_value_total_ever_online"]
    for col in columns:
        replace_with_thresholds(df_, col)

    # Toplam değişkenlerin oluşturulması
    df_["order_num_total"] = df_["order_num_total_ever_online"] + df_["order_num_total_ever_offline"]
    df_["customer_value_total"] = df_["customer_value_total_ever_offline"] + df_["customer_value_total_ever_online"]

    # Tarih dönüşümleri
    date_columns = df_.columns[df_.columns.str.contains("date")]
    df_[date_columns] = df_[date_columns].apply(pd.to_datetime)

    # Analiz Tarihi ve Metrikler
    analysis_date = dt.datetime(2021, 6, 1)
    cltv_df = pd.DataFrame()
    cltv_df["customer_id"] = df_["master_id"]
    cltv_df["recency_cltv_weekly"] = (df_["last_order_date"] - df_["first_order_date"]).dt.days / 7
    cltv_df["T_weekly"] = (analysis_date - df_["first_order_date"]).dt.days / 7
    cltv_df["frequency"] = df_["order_num_total"]
    cltv_df["monetary_cltv_avg"] = df_["customer_value_total"] / df_["order_num_total"]

    # Filtreleme (Sıfır ve 1 olanları eliyoruz - Modellerin çalışması için şart)
    cltv_df = cltv_df[(cltv_df['frequency'] > 1)]
    cltv_df = cltv_df[(cltv_df['monetary_cltv_avg'] > 0)]

    # 3. BG-NBD MODELİ
    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df['frequency'], cltv_df['recency_cltv_weekly'], cltv_df['T_weekly'])

    cltv_df["exp_sales_3_month"] = bgf.predict(4 * 3, cltv_df['frequency'], cltv_df['recency_cltv_weekly'],
                                               cltv_df['T_weekly'])
    cltv_df["exp_sales_6_month"] = bgf.predict(4 * 6, cltv_df['frequency'], cltv_df['recency_cltv_weekly'],
                                               cltv_df['T_weekly'])

    # 4. GAMMA-GAMMA MODELİ
    ggf = GammaGammaFitter(penalizer_coef=0.01)
    ggf.fit(cltv_df['frequency'], cltv_df['monetary_cltv_avg'])
    cltv_df["exp_average_value"] = ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                           cltv_df['monetary_cltv_avg'])

    # 5. CLTV HESAPLAMA
    cltv_df["cltv"] = ggf.customer_lifetime_value(bgf,
                                                  cltv_df['frequency'],
                                                  cltv_df['recency_cltv_weekly'],
                                                  cltv_df['T_weekly'],
                                                  cltv_df['monetary_cltv_avg'],
                                                  time=6,  # 6 ay
                                                  freq="W",
                                                  discount_rate=0.01)

    # Segmentleme
    cltv_df["cltv_segment"] = pd.qcut(cltv_df["cltv"], 4, labels=["D", "C", "B", "A"])

    return cltv_df


# --- ÇALIŞTIRMA BÖLÜMÜ ---
# Veriyi oku (Dosya yolunu kendi bilgisayarına göre kontrol et)
df_raw = pd.read_csv("Crm_analitiği/datasets/flo_data_20k.csv")

# Fonksiyonu çağır
final_cltv_df = (create_cltv_df(df_raw))

# Sonuçları göster
print("--- CLTV Segment Özeti ---")
print(final_cltv_df.groupby("cltv_segment").agg({"cltv": ["mean", "min", "max", "count"]}))
print("\n--- İlk 10 Satır ---")
print(final_cltv_df.head(10))

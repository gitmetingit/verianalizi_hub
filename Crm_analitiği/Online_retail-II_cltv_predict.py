import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from lifetimes import BetaGeoFitter
from lifetimes import GammaGammaFitter
from lifetimes.plotting import plot_period_transactions

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format', lambda x: '%.3f' % x)

def outlier_thresholds(dataframe,variable):
    quartile1=dataframe[variable].quantile(0.01)
    quartile3=dataframe[variable].quantile(0.99)
    interquartile_range=quartile3-quartile1
    up_limit=quartile3 + 1.5 * interquartile_range
    low_limit=quartile1 - 1.5 * interquartile_range
    return low_limit,up_limit

def replace_with_threshold(dataframe,variable):
    low_limit,up_limit=outlier_thresholds(dataframe,variable)
    dataframe[variable]=dataframe[variable].astype(float)
    dataframe.loc[dataframe[variable]<low_limit,variable]=low_limit
    dataframe.loc[dataframe[variable]>up_limit,variable]=up_limit

df_ = pd.read_excel(r"C:\Users\metin\PycharmProjects\VeriAnalizi\Crm_analitiği\datasets\online_retail_II.xlsx")
df = df_.copy()
df.head()
df.describe().T
df.isnull().sum()

df.dropna(inplace=True)
df=df[~df['Invoice'].astype(str).str.contains('C')]
df=df[df['Price']>0]
df=df[df['Quantity']>0]
df['Customer ID']=df['Customer ID'].astype(int)


replace_with_threshold(df,'Price')
replace_with_threshold(df,'Quantity')

df['TotalPrice']=df['Price'] * df['Quantity']
today_date=dt.datetime(2011,12,11)

cltv_df = df.groupby('Customer ID').agg({'Invoice':lambda x:x.nunique(),
                                         'InvoiceDate':[ lambda x:(today_date-x.min()).days,
                                                         lambda x:(x.max()-x.min()).days],
                                         'TotalPrice':lambda x:x.sum()
                                        })
#burada rfm den farklı olarak recency değerini InvoiceDate.max()-InvoiceDate.min() şeklinde hesaplıyoruz

cltv_df.columns=cltv_df.columns.droplevel(0)
cltv_df.columns=['frequency','T','recency','monetary']
cltv_df.head()

cltv_df['monetary'] = cltv_df['monetary'] / cltv_df['frequency']
cltv_df = cltv_df[cltv_df['frequency']>1]
cltv_df['T'] = cltv_df['T'] / 7
cltv_df['recency'] = cltv_df['recency'] / 7

bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit (cltv_df['frequency'],
         cltv_df['recency'],
         cltv_df['T']     )
#<lifetimes.BetaGeoFitter: fitted with 2845 subjects, a: 1.98, alpha: 1.90, b: 6.19, r: 2.20>

# 1 hafta içinde en çok satın alma beklediğimiz 10 müşteri/müşteriler
#bgf.conditional_expected_number_of_purchases_up_to_time,bgf.predict ikiside aynı işlem yazım kolaylığı için predict kullanıyoruz
bgf.conditional_expected_number_of_purchases_up_to_time(1,
                                                        cltv_df['frequency'],
                                                        cltv_df['recency'],
                                                        cltv_df['T']).sort_values(ascending=False).head(10)
bgf.predict(1,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)
cltv_df['expected_purc_1_week'] = bgf.predict(1,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])

# 1 ay içinde en çok satın alma beklediğimiz 10 müşteri/müşteriler
bgf.predict(4,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sort_values(ascending=False).head(10)
cltv_df['expected_purc_1_month'] = bgf.predict(4,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])

# 3 ay içinde  beklediğimiz toplam ziyaret
bgf.predict(4*3,
            cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T']).sum()
cltv_df['expected_purc_3_month'] = bgf.predict(4*3,
                                               cltv_df['frequency'],
                                               cltv_df['recency'],
                                               cltv_df['T'])

#Tahminlerin değerlendirilmesi
plot_period_transactions(bgf)
plt.show()

ggf = GammaGammaFitter(penalizer_coef=0.01)
ggf.fit(cltv_df['frequency'],
        cltv_df['monetary'])
# Her bir müşterinin ziyaret başına bırakacağı yaklaşık değer.Yapılandırılmış harcama ortalaması diyebiliriz.
# Alışveriş alışkanlığı günden güne değişen müşterilerin tüm kitledeki durumu gibi unsurlar ele alınarak değerlendiriliyor.
ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary'])

ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                        cltv_df['monetary']).sort_values(ascending=False).head(10)

cltv_df['expected_average_profit']=ggf.conditional_expected_average_profit(cltv_df['frequency'],
                                                                           cltv_df['monetary'])

cltv_df.sort_values(by='expected_average_profit',ascending=False).head(10)

cltv = ggf.customer_lifetime_value(bgf,
                                      cltv_df['frequency'],
                                      cltv_df['recency'],
                                      cltv_df['T'],
                                      cltv_df['monetary'],
                                      time=3,
                                      freq='W',
                                      discount_rate = 0.01 )

# freq='W' dikkat bu değer ggf modelinin parametresi değil bgf in parametresidir.
# ggf modelinin time parametresi sabit ay cinsinden alınır.
cltv.head()
cltv=cltv.reset_index()

cltv_final = cltv_df.merge(cltv, on='Customer ID', how='left')
cltv_final.sort_values(by='clv' , ascending=False)
# clv ismini model kendi koyuyor.
#clv değeri  expected_average_profit x expected_purc_3_month

cltv_final['segments']=pd.qcut(cltv_final['clv'],4,['D','C','B','A'])
cltv_final.sort_values(by='clv',ascending= False)
cltv_final.groupby('segments').agg({'count',sum,'mean'})

##########FONKSİYONLAŞTIRMA##########
def create_cltv_p(dataframe,month=3) :
    dataframe.dropna(inplace=True)
    dataframe = dataframe[~dataframe['Invoice'].astype(str).str.contains('C')]
    dataframe = dataframe[dataframe['Price'] > 0]
    dataframe = dataframe[dataframe['Quantity'] > 0]

    replace_with_threshold(dataframe, 'Price')
    replace_with_threshold(dataframe, 'Quantity')

    dataframe['TotalPrice'] = dataframe['Price'] * dataframe['Quantity']
    today_date = dt.datetime(2011, 12, 11)

    cltv_df = dataframe.groupby('Customer ID').agg({'Invoice': lambda x: x.nunique(),
                                             'InvoiceDate': [lambda x: (today_date - x.min()).days,
                                                             lambda x: (x.max() - x.min()).days],
                                             'TotalPrice': lambda x: x.sum()                   })

    cltv_df.columns = cltv_df.columns.droplevel(0)
    cltv_df.columns = ['frequency', 'T', 'recency', 'monetary']
    cltv_df['monetary'] = cltv_df['monetary'] / cltv_df['frequency']
    cltv_df = cltv_df[cltv_df['frequency'] > 1]
    cltv_df['T'] = cltv_df['T'] / 7
    cltv_df['recency'] = cltv_df['recency'] / 7

    bgf = BetaGeoFitter(penalizer_coef=0.001)
    bgf.fit(cltv_df['frequency'],
            cltv_df['recency'],
            cltv_df['T'])

    cltv_df['expected_purc_1_week'] = bgf.predict(1,
                                                  cltv_df['frequency'],
                                                  cltv_df['recency'],
                                                  cltv_df['T'])

    cltv_df['expected_purc_1_month'] = bgf.predict(4,
                                                   cltv_df['frequency'],
                                                   cltv_df['recency'],
                                                   cltv_df['T'])


    cltv_df['expected_purc_3_month'] = bgf.predict(12,
                                                   cltv_df['frequency'],
                                                   cltv_df['recency'],
                                                   cltv_df['T'])

    cltv = ggf.customer_lifetime_value(bgf,
                                       cltv_df['frequency'],
                                       cltv_df['recency'],
                                       cltv_df['T'],
                                       cltv_df['monetary'],
                                       time=3,
                                       freq='W',
                                       discount_rate=0.01)

    cltv = cltv.reset_index()
    cltv_final = cltv_df.merge(cltv, on='Customer ID', how='left')
    cltv_final['segments'] = pd.qcut(cltv_final['clv'], 4, ['D', 'C', 'B', 'A'])
    cltv_final.sort_values(by='clv', ascending=False)
    cltv_final.groupby('segments').agg({'count', sum, 'mean'})

    return cltv_final

df = df_.copy()
cltv_final2 = create_cltv_p(df)
cltv_final2.to_csv("cltv_prediction.csv")




##########GÖREV1##########
import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.with',500)
df=pd.read_csv("Temel_python_projesi/datasets/persona.csv")

def check_df(dataframe, head=5):
    print("#################### Shape ####################")
    print(dataframe.shape)
    print("#################### Dtypes ####################")
    print(dataframe.dtypes)
    print("#################### Head ####################")
    print(dataframe.head(head))
    print("#################### Tail ####################")
    print(dataframe.tail(head))
    print("#################### NA ####################")
    print(dataframe.isnull().sum())
    print("#################### Quantiles ####################")
    print(dataframe.quantile([0,0.05,0.50,0.95,0.99,1]).T)
check_df(df, head=10 )


def check_df(dataframe, head=5,tail=5,quan=False ):
    print("#################### Shape ####################")
    print(dataframe.shape)
    print("#################### Dtypes ####################")
    print(dataframe.dtypes)
    print("#################### Head ####################")
    print(dataframe.head(head))
    print("#################### Tail ####################")
    print(dataframe.tail(tail))
    print("#################### NA ####################")
    print(dataframe.isnull().sum())
    if quan :
        num_cols= dataframe.select_dtypes(include=["number"])
        print("#################### Quantiles ####################")
        print(num_cols.quantile([0, 0.05, 0.50, 0.95, 0.99, 1]).T)
check_df(df, head=10,tail=3,quan=True )

import seaborn as sns
import matplotlib.pyplot as plt
def cat_summary(dataframe,col_name,plot=False) :
    print(pd.DataFrame({col_name:dataframe[col_name].value_counts(),
                     "Ratio":100*dataframe[col_name].value_counts()/len(dataframe)}))
    print("#################################")
    if plot:
        sns.countplot(x=dataframe[col_name],data=dataframe)
        plt.show()
cat_summary(df,"AGE",True)

def cat_summary(dataframe,col_name,plot=False,ratio=True):
    if ratio :
       print(pd.DataFrame({col_name:dataframe[col_name].value_counts(),
                           "Ratio": 100 * dataframe[col_name].value_counts()/len(dataframe)}))
       print("#############################")
    else :
        print(pd.DataFrame({col_name:dataframe[col_name].value_counts()}))
        print("##############################")

    if plot:
        sns.countplot(x=dataframe[col_name], data=dataframe)
        plt.show()
cat_summary(df,"AGE",True,True)

##########GÖREV2##########
def check_df(dataframe, head=5):
    """
    Girilen veri çerçevesinin boyut, veri tipi, ilk 5 gözlemi, son 5 gözlemi, boş değerleri toplamını ve yüzdelik
    dilimleri getirir.

    :param dataframe:
           Tanımlanan veri çerçevesi.

    :param head:
           int,isteğe bağlı
           Baştan ve sondan gösterilecek gözlem saysıdır.

    :return: Yok.

    :example: check_df(df,7)

    :notes: Sayısal olmayan kolonlarda sorun yaşanmaması için cat_cols ile kulanılabilir.

    """
    print("#################### Shape ####################")
    print(dataframe.shape)
    print("#################### Dtypes ####################")
    print(dataframe.dtypes)
    print("#################### Head ####################")
    print(dataframe.head(head))
    print("#################### Tail ####################")
    print(dataframe.tail(head))
    print("#################### NA ####################")
    print(dataframe.isnull().sum())
    print("#################### Quantiles ####################")
    print(dataframe.quantile([0,0.05,0.50,0.95,0.99,1]).T)

def cat_summary(dataframe,col_name,plot=False) :
    """
    "Seçilen değişkendeki kategorilerin, tüm veri çerçevesine (dataframe) oranla yüzde hesaplamasını verir."

    :param dataframe:
               Değişkenlerinin (sütunlarının) yüzde oranları hesaplanacak olan veri çerçevesi.

    :param col_name:[str]
               Yüzdelik hesaplaması yapılacak olan değişkenin adı.

    :param plot: bool,isteğe bağlı
               Veri sonuçlarının görselleştirilip görselleştirilmeyeceğine karar verir.

    :return: Yok.

    :example:
            import seaborn as sns
            df = sns.load_dataset("titanic")
            cat_summary(df, "Survived", plot=True)
    """
    print(pd.DataFrame({col_name:dataframe[col_name].value_counts(),
                     "Ratio":100*dataframe[col_name].value_counts()/len(dataframe)}))
    print("#################################")
    if plot:
        sns.countplot(x=dataframe[col_name],data=dataframe)
        plt.show()


import pandas as pd

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('float_format',lambda x: '%.2f' % x )

##########GÖREV1##########
df=pd.read_csv(r"C:\Users\metin\PycharmProjects\VeriAnalizi\Temel_python_projesi\datasets\persona.csv")
df.head()
df.info
df.columns
df.dtypes

df["SOURCE"].unique()
df["SOURCE"].value_counts()

df["PRICE"].nunique()
df["PRICE"].value_counts()

df["COUNTRY"].value_counts()
df.groupby("COUNTRY").agg({"PRICE":"count"})
df.pivot_table("PRICE","COUNTRY", aggfunc="count")

df.groupby("COUNTRY").agg({"PRICE":"sum"})
df.pivot_table("PRICE","COUNTRY",aggfunc="sum")

df["SOURCE"].value_counts()
df.groupby("SOURCE").agg({"PRICE":"count"})

df.groupby("COUNTRY").agg({"PRICE":"mean"})

df.groupby("SOURCE").agg({"PRICE":"mean"})

df.groupby(["COUNTRY","SOURCE"]).agg({"PRICE":"mean"})

##########GÖREV2##########
df.groupby(['COUNTRY','SOURCE', 'SEX',  'AGE']).agg({"PRICE":"mean"})

##########GÖREV3##########
agg_df=df.groupby(['COUNTRY','SOURCE', 'SEX',  'AGE']).agg({"PRICE":"mean"}).sort_values(by='PRICE', ascending=False)

##########GÖREV4##########
agg_df.reset_index(inplace=True)
agg_df.head()
##########GÖREV5##########
aralık = [0,18,23,30,40,agg_df["AGE"].max()]
etiket =['0_18', '19_23', '24_30', '31_40', '41_'+str(agg_df["AGE"].max())]
agg_df["AGE_CAT"]=pd.cut(agg_df["AGE"],labels=etiket,bins=aralık)
agg_df.sort_values(by='AGE_CAT', ascending=False)
agg_df.head(50)

##########GÖREV6##########
agg_df["customers_level_based"]=["_".join(i).upper() for i in agg_df.drop(["AGE", "PRICE"],axis=1).values]
agg_df["customers_level_based"]=agg_df[["COUNTRY" , "SOURCE","SEX" ,"AGE_CAT"]].apply(lambda x:"_".join(x).upper(),axis=1)

agg_df=agg_df.groupby("customers_level_based").agg({"PRICE":"mean"})
agg_df.reset_index(inplace=True)
agg_df.head(50)


##########GÖREV7##########
agg_df.sort_values(by="PRICE", ascending=False)
etiket_seg=["D","C","B","A"]
agg_df["SEGMENT"]=pd.qcut(agg_df["PRICE"],4,labels=etiket_seg)
agg_df.groupby("SEGMENT").agg({"PRICE":["mean","max","sum"]},inplace=True)
agg_df.head(50)


##########GÖREV8##########
new_user = "TUR_ANDROID_FEMALE_31_40"
#new_user = "FRA_IOS_FEMALE_31_40"
agg_df[agg_df["customers_level_based"] == new_user]


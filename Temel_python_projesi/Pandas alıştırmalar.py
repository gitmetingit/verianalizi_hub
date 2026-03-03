import seaborn as sns
import pandas as pd

pd.set_option('display.max_columns',500)
df=sns.load_dataset("titanic")
df.columns
df.head()
df.shape

df["sex"].value_counts()

df.nunique()

df["pclass"].nunique()

df[["parch","pclass"]].nunique()

df["embarked"].dtype
df["embarked"].dtype=df["embarked"].astype("category")
df["embarked"].dtype
df.info()

df[df["embarked"]=="C"].info
df.iloc[df["embarked"]=="C"].info

df[~(df["embarked"]=="S")].info
df.iloc[df["embarked"] != "S"].info

df[(df["age"]<30) & (df["sex"]=="female")].info
df.iloc[(df["age"] < 30) & (df["sex"] == "female")].info

df[(df["fare"] > 500) | (df["age"] < 70)].info
df.iloc[((df["fare"] > 500) | df["age"] < 70)].info

df.isnull().sum()

df.drop( columns=["who"],inplace=True)
df.drop("who",axis=1,inplace=True)

df["deck"].fillna(df["deck"].mode()[0],inplace=True)
df["deck"].isnull().sum()

df["age"].fillna(df["age"].median(),inplace=True)
df["age"].isnull().sum()

df.groupby(["pclass","sex"])["survived"].agg(["sum","mean","count"])
df.groupby(["pclass","sex"]).agg({"survived": ["sum","count","mean"]})

df["age_flag"]=df["age"].apply(lambda x:1 if x<30 else 0)
"""def otuz_yas (dizi) :
    age_flag=[]
    for age in dizi:
      if age < 30 :
         sonuc=1
      else :
        sonuc=0
      age_flag.append(sonuc)
    return age_flag
df["age_flag"] =otuz_yas(df["age"])"""
"""df["age_flag"]=0
df.loc[df["age"]<30,"age_flag"]=1"""
"""df["age_flag"]=[1 if x<30 else 0 for x in df["age"]]"""

df_=sns.load_dataset("tips")
df_.info

df_.groupby("time").agg({"total_bill": ["sum","min","mean","max"]})
df_.groupby("time")["total_bill"].agg(["sum","min","mean","max"])

df_.groupby(["day","time"]).agg({"total_bill": ["sum","min","mean","max"]})
df_.groupby(["day","time"])["total_bill"].agg(["sum","min","mean","max"])

df_[(df_["sex"]=="Female") & (df_["time"]=="Lunch")].groupby("day").agg({"total_bill":["sum","min","mean","max"],
                            "tip":["sum","min","mean","max"]})
df_[(df_["time"]=="Lunch") & (df_["sex"]=="Female")].groupby("day")[["total_bill","tip"]].agg(["sum","min","mean","max"])

df_.loc[(df_["size"] < 3) & (df_["total_bill"] > 10),"tip"].mean()

df_["total_bill_tip_sum"]=df_["total_bill"]+df_["tip"]
df_.head()

df_yeni=df_.sort_values("total_bill_tip_sum",ascending=False)[:30]
df_yeni.head()



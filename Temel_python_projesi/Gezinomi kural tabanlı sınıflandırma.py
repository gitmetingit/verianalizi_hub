import pandas as pd
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 500)
pd.set_option('display.float_format' , lambda x: '%.2f' % x)

##########GÖREV1##########
df=pd.read_excel(r"C:\Users\metin\PycharmProjects\PythonProject\Temel_python_projesi\datasets\miuul_gezinomi.xlsx")
df.head()
df.info
df.columns

df['SaleCityName'].nunique()
df['SaleCityName'].value_counts()

df['ConceptName'].nunique()

df['ConceptName'].value_counts()

df.groupby('SaleCityName')['Price'].sum()
df.groupby('SaleCityName').agg({'Price':"sum"})

df.groupby('ConceptName')['Price'].sum()

df.groupby('SaleCityName').agg({'Price':"mean"})

df.groupby('ConceptName')['Price'].mean()

df.groupby(['SaleCityName','ConceptName']).agg({'Price':"mean"})

##########GÖREV2##########
"""df['EB_Score']=df['SaleCheckInDayDiff'].apply(lambda x :"Last Minuters" if x<8
                                        else( "Potential Planners"
                                         if (8<=x<31 )
                                         else( "Planners" if (31<=x<90)
                                         else ( "Early Bookers" ))))

df['EB_Score'].value_counts()
df['SaleCheckInDayDiff'].value_counts()"""

etiket=["Last Minuters","Potential Planners","Planners","Early Bookers" ]
aralık=[-1,7,31,90,df["SaleCheckInDayDiff"].max()]
df['EB_Score']=pd.cut(df['SaleCheckInDayDiff'],bins=aralık,labels=etiket)
df['EB_Score'].value_counts()
df.head()
##########GÖREV3##########
df.groupby(['SaleCityName','ConceptName','EB_Score'])["Price"].agg(["mean","count"])
df.groupby(['SaleCityName','ConceptName','EB_Score']).agg({"Price":["mean","count"]})

df.groupby(['SaleCityName','ConceptName', 'Seasons']).agg({"Price":["mean","count"]})

df.groupby(['SaleCityName','ConceptName','CInDay']).agg({"Price":["mean","count"]})

##########GÖREV4##########
agg_df = df.groupby(['SaleCityName','ConceptName', 'Seasons']).agg({"Price":"mean"}).sort_values("Price",ascending=False)
agg_df.head(20)

##########GÖREV5##########
agg_df.reset_index(inplace=True)
agg_df.head(20)

##########GÖREV6##########
#agg_df["sales_level_based"]=(agg_df["SaleCityName"] + "_" + agg_df["ConceptName"]+ "_" + agg_df["Seasons"]).apply(lambda x: x.upper())

agg_df["sales_level_based"]=agg_df[["SaleCityName","ConceptName","Seasons"]].apply(lambda x: "_".join(x).upper(),axis=1)

##########GÖREV7##########
agg_df.sort_values("Price",ascending=False)
agg_df["SEGMENT"]=pd.qcut(agg_df["Price"],4,labels=["D","C","B","A"])
agg_df.head(20)
agg_df.groupby("SEGMENT").agg({"Price":["mean","max","sum"]})

##########GÖREV8##########
new_user="ANTALYA_HERŞEY DAHIL_HIGH"
agg_df[(agg_df["sales_level_based"]==new_user)]["Price"]

new_user="GIRNE_YARIM PANSIYON_LOW"
agg_df[agg_df["sales_level_based"]==new_user]["SEGMENT"]

# Genelde kullanılan o meşhur yapı:
def create_invoice_product_df(dataframe):
    return dataframe.groupby(['Invoice', 'StockCode'])['Quantity'].sum().unstack().fillna(0).applymap(lambda x: 1 if x > 0 else 0)
# Bu kod: "Hücre 0'dan büyükse True, değilse False yap; sonra bunları tam sayıya (1-0) çevir" der. applymap yerine
df_matrix = (df_matrix > 0).astype(int)
# Tüm tablodaki "Unknown" yazan hücreleri True, diğerlerini False yapar
mask = (df_matrix == "Unknown")
# Tablodaki her hücreye bakar; eğer 5, 10 veya 15 ise True döner
df_matrix.isin([5, 10, 15])
Tablodaki her hücrede "TEA" kelimesi geçiyor mu?
df.apply(lambda x: x.astype(str).str.contains("TEA"))
# Hem 0'dan büyük hem 100'den küçük hücreler 1, diğerleri 0 olur
yeni_matris = ((df_matrix > 0) & (df_matrix < 100)).astype(int)

def check_id(dataframe, stock_code):
    """
    ID'si verilen ürünün tam adını (Description) döndürür.
    """
    product_name = dataframe[dataframe["StockCode"] == stock_code][["Description"]].values[0].tolist()
    print(product_name)

# Örnek Kullanım:
# check_id(df, 21931)

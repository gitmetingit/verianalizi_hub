##########GÖREV1##########
x = 8
y = 3.2
z = 8j+18
a = "hello world"
b = True
c = 23<22
d  = {"name":"Jake",
   "age":27,
   "adress":"Downtown"}
s = ("machine learning","data science")
t = {"python","machine learning","data science"}
p = [1,2,"a"]

type(x)
type(y)
type(z)
type(a)
type(b)
type(c)
type(d)
type(s)
type(t)
type(p)

##########GÖREV2##########
text="the goal is to turn data into information, and information into insight"
text.upper().replace(","," ").replace("."," ").split()

##########GÖREV3##########
lst = ["D","A","T","A","S","C","I","E","N","C","E"]
len(lst)
lst[0]
lst[10]
data_list = lst[0:4]
data_list
lst.pop(8)
lst.append("m")
lst.insert(8,'N')

##########GÖREV4##########
dict = {'Christian':["America",18],
        'Daisy':["England",12],
        'Antonio':["Spain",22],
        'Dante':["Italy",25]}

dict.keys()
dict.values()
dict.update(Daisy = ["England",13])
dict.update({"Ahmet":["Turkey",24]})
dict.pop("Antonio")
dict.items()

##########GÖREV5##########
l=[2,13,18,93,22]

def tek_cift(sayı):
    tek = []
    cift = []
    for i in sayı:
        if i%2==0:
            cift.append(i)
        else:
            tek.append(i)
    return tek,cift

tekler,ciftler = tek_cift(l)
print(tekler,ciftler)

##########GÖREV6##########
ogrenciler = ["Ali","Veli","Ayşe","Talat","Zeynep","Ece"]

for i,isim in enumerate(ogrenciler,1):
    if i<4 :
       print(f" Mühendislik Fakültesi {i}. öğrenci: {isim} ")
    else :
       print(f" Tıp Fakültesi {i-3}. öğrenci: {isim} ")

##########GÖREV7##########
ders_kodu = ["CMP1005","PSY1001","HUK1005","SEN2204"]
kredi = [3,4,2,4]
kontenjan = [30,75,150,25]

for dk,kr,ko in zip(ders_kodu,kredi,kontenjan):
    print(f"kredisi {kr} olan {dk} kodlu dersin kontenjanı {ko} kişidir")

##########GÖREV8##########
kume1 =set(["data","python"])
kume2 =set(["data","python","miuul","function","cut","lambda"])

def kapsama (k1,k2):
     if k1.issuperset(k2) :
        k_int = k1.intersection(k2)
        print(k_int)
     else :
        k_dif = k2.difference(k1)
        print(k_dif)
     return k1,k2
kum1,kum2 = kapsama(kume1,kume2)
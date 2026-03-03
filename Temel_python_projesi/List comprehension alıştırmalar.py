##########GÖREV1##########
import seaborn as sns
df=sns.load_dataset("car_crashes")
df.columns
["NUM_"+ col.upper() if df[col].dtypes not in ["object","string"] else col.upper() for col in df.columns]

##########GÖREV2##########
[col.upper() + "_FLAG"  if "no" not in col else col.upper() for col in df.columns]

##########GÖREV3##########
og_list = ['no_previous', 'abbrev']
new_cols = [col for col in df.columns if col not in og_list ]
new_df=df[new_cols]
new_df
import pandas as pd

df_master = pd.read_csv("Clubs_master_v1.csv")
df_master['source'] = "master"
df_master = df_master.rename(columns={'Club / Association Name':'Club'})
df_master = df_master.dropna(subset='Club')

df_boats = pd.read_csv("Clubs_boats.csv")
df_boats['source'] = "boats"
df_boats = df_boats.dropna(subset='Club')

df = pd.concat([df_master, df_boats], ignore_index=True)

df['club_raw_name'] = df['Club']
df['canonical_club_name'] = None
df['status'] = 'pending'
df['confidence'] = None
df['notes'] = None


df = df.sort_values(by='club_raw_name')

final_columns=['club_raw_name','source','canonical_club_name','status','confidence','notes']

df[final_columns].to_csv("Clubs_master_v2.csv", index=False)

df_trial = df.sample(n=250, random_state=73)

df_trial[final_columns].to_csv("ClubsRawTrial.csv",index=False)
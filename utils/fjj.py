import instagrapi

from instagrapi import Client

cl = Client()
cl.login("ralph_masson1", "VFE9Z3D87R2U")

user_id = cl.user_id_from_username("hana.ne6489")

abonnes = cl.user_followers(user_id)
abonnements = cl.user_following(user_id)

medias = cl.user_medias(user_id, 20)


abonnement_name = [abonnements.get(list(abonnements)[i]).username for i in range(len(abonnements))]

abonnes_name = [abonnes.get(list(abonnes)[i]).username for i in range(len(abonnes))]

abonnes_sah = []
faux_abonnes = []
coordx = []
coordx1 = []
coordy = []
coordy1 = []

for i in range(len(abonnement_name)):
    if abonnement_name[i] in abonnes_name:
        abonnes_sah.append(abonnement_name[i])
        coordx.append(random.randint(1,1500))
        coordy.append(random.randint(1,500))

    else:
        faux_abonnes.append(abonnement_name[i])
        coordx1.append(random.randint(1,1500))
        coordy1.append(random.randint(1000,1500))


import pandas as pd


abonnes_sah_df = pd.DataFrame(abonnes_sah)
abonnes_sah_df['x'] = coordx
abonnes_sah_df['y'] = coordy

faux_abonnes_df = pd.DataFrame(faux_abonnes)
faux_abonnes_df['x'] = coordx1
faux_abonnes_df['y'] = coordy1

total_abonnes = pd.concat([abonnes_sah_df,faux_abonnes_df])
import plotly.express as px

fig = px.scatter(faux_abonnes_df,x='x',y='y',text = total_abonnes.columns[0],title="Abonnements non réciproques de Hanane")

fig.show()

fig = px.scatter(abonnes_sah_df,x='x',y='y',text = total_abonnes.columns[0],title="Abonnements  réciproques de Hanane")
fig.show()






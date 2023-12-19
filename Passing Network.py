import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch, VerticalPitch
import numpy as np

plt.style.use("Solarize_Light2")

#read in csv
data = pd.read_csv(r"D:\Work Stuff\Club Portfolio\PSIM\2022-10-01 Persegres vs PSIM\Persegres vs PSIM lengkap.csv")

unique_players = data['Player'].unique()
print(unique_players)

# Shuffle the unique players
np.random.shuffle(unique_players)

# Generate random numbers for each player
player_ids = np.random.choice(range(1, 100), size=len(unique_players), replace=False)

# Create a dictionary to map players to their IDs
player_id_dict = {player: player_id for player, player_id in zip(unique_players, player_ids)}

# Create a new column in the DataFrame with the player IDs
data['playerid'] = data['Player'].map(player_id_dict)

#filter
data['passer'] = data['playerid']
data['recipient'] = data['playerid'].shift(-1)

print(data)

passes = data.loc[(data["Event"]=="Pass (successful)")]
print(passes)

#average locations
average_locations = passes.groupby('passer').agg({'X':['mean'],'Y':['mean','count']})
average_locations.columns = ['x', 'y', 'count']

pass_between = passes.groupby(['passer','recipient']).size().reset_index()
pass_between.rename({'size':'pass_count'},axis='columns',inplace=True)

pass_between = pass_between.merge(average_locations, left_on='passer',right_index = True)
pass_between = pass_between.merge(average_locations, left_on='recipient',right_index = True,suffixes=['','_end'])

#create the pitch
pitch = Pitch(pitch_type='statsbomb', line_zorder=2, pitch_color='#22312b', line_color='gray')

#Draw the pitch
fig, ax = pitch.draw(figsize=(16, 11))

arrows = pitch.arrows(1.24*pass_between.x,0.84*pass_between.y,1.2*pass_between.x_end, 0.84*pass_between.y_end, ax=ax,
                      width = 3, headwidth =3, color='white', zorder =1, alpha = 0.5)

nodes = pitch.scatter(1.24*average_locations.x,0.84*average_locations.y,
                      s = 300, color = '#d3d3d3', edgecolors = 'black', linewidth = 2.5, alpha = 1, zorder = 1, ax = ax)

# Invert x axis
plt.gca().invert_xaxis()

plt.show()
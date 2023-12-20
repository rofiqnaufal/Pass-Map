import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch, VerticalPitch
import numpy as np
from adjustText import adjust_text

plt.style.use("Solarize_Light2")

#read in csv
data = pd.read_csv(r"D:\Work Stuff\Club Portfolio\PSIM\2022-09-27 PSIM vs Persela\PSIM vs Persela lengkap.csv")

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

# filter out rows where the passer and recipient are the same player
data = data[data['playerid'] != data['playerid'].shift(-1)]


#filter
data['passer'] = data['Player']
data['recipient'] = data['Player'].shift(-1)

print(data)

passes = data.loc[(data["Event"]=="Pass (successful)")]
# Specify the names to be removed
names_to_remove = ["Roni","Elina","Sugiyanto","Ocvian", "Andre"]
# Remove rows where the passer name is in the specified list
passes = passes[~passes['Player'].isin(names_to_remove)]
print(passes)

#Calculating vertices size and location
scatter_df = pd.DataFrame()
for i, name in enumerate(passes["Player"].unique()):
    passx = passes.loc[passes["passer"] == name]["X"].to_numpy()
    recx = passes.loc[passes["recipient"] == name]["X2"].to_numpy()
    passy = passes.loc[passes["passer"] == name]["Y"].to_numpy()
    recy = passes.loc[passes["recipient"] == name]["Y2"].to_numpy()
    scatter_df.at[i, "passer"] = name
    #make sure that x and y location for each circle representing the player is the average of passes and receptions
    scatter_df.at[i, "x"] = np.mean(np.concatenate([passx, recx]))
    scatter_df.at[i, "y"] = np.mean(np.concatenate([passy, recy]))
    #calculate number of passes
    scatter_df.at[i, "no"] = passes.loc[passes["passer"] == name].count().iloc[0]

#adjust the size of a circle so that the player who made more passes
scatter_df['marker_size'] = (scatter_df['no'] / scatter_df['no'].max() * 1500)


print(scatter_df)

#Drawing pitch
pitch = Pitch(line_color='grey')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
#Scatter the location on the pitch
pitch.scatter(1.24*scatter_df.x, 0.84*scatter_df.y, s=scatter_df.marker_size, color='red', edgecolors='grey', linewidth=1, alpha=1, ax=ax["pitch"], zorder = 3)
#annotating player name
for i, row in scatter_df.iterrows():
    text=pitch.annotate(row.passer, xy=(1.24*row.x, 0.84*row.y), c='black', va='center', ha='center',
                        weight = "bold", size=10, ax=ax["pitch"], zorder = 4)


fig.suptitle("Formasi PSIM", fontsize = 25)



#Calculating edges width
#counting passes between players
passes["pair_key"] = passes.apply(lambda X: "_".join(sorted([X["passer"], X["recipient"]])), axis=1)
lines_df = passes.groupby(["pair_key"]).X.count().reset_index()
lines_df.rename({'X':'pass_count'}, axis='columns', inplace=True)
#setting a treshold. You can try to investigate how it changes when you change it.
lines_df = lines_df[lines_df['pass_count']>0]

print(lines_df)

# Create a boolean mask indicating rows that do not contain the words to remove
mask = ~lines_df['pair_key'].str.contains('|'.join(names_to_remove), case=False)

# Apply the mask to filter out the rows
lines_df_filtered = lines_df[mask]

# Print the filtered dataframe
print(lines_df_filtered)


#plot once again pitch and vertices
pitch = Pitch(line_color='grey')
fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False,
                     endnote_height=0.04, title_space=0, endnote_space=0)
pitch.scatter(1.24*scatter_df.x, 0.84*scatter_df.y, s=scatter_df.marker_size, color='yellow', edgecolors='green', linewidth=1, alpha=1, ax=ax["pitch"], zorder = 3)
for i, row in scatter_df.iterrows():
    pitch.annotate(row.passer, xy=(1.24*row.x, 0.84*row.y), c='black', va='center', ha='center', weight = "bold", size=10, ax=ax["pitch"], zorder = 4)

for i, row in lines_df_filtered.iterrows():
        player1 = row["pair_key"].split("_")[0]
        player2 = row['pair_key'].split("_")[1]
        print("player1:", player1)
        print("player2:", player2)
        print(scatter_df)
        #take the average location of players to plot a line between them
        player1_rows = scatter_df.loc[scatter_df["passer"] == player1]
        player2_rows = scatter_df.loc[scatter_df["passer"] == player2]

        if len(player1_rows) == 0:
            print(f"No data found for player1: {player1}")
            # Handle the error or continue with a default value
        else:
            player1_x = player1_rows['x'].iloc[0]*1.24
            player1_y = player1_rows['y'].iloc[0]*0.84

        if len(player2_rows) == 0:
            print(f"No data found for player2: {player2}")
            # Handle the error or continue with a default value
        else:
            player2_x = player2_rows['x'].iloc[0]*1.24
            player2_y = player2_rows['y'].iloc[0]*0.84
        num_passes = row["pass_count"]
        #adjust the line width so that the more passes, the wider the line
        line_width = (num_passes / lines_df['pass_count'].max() * 10)
        #plot lines on the pitch
        pitch.lines(player1_x, player1_y, player2_x, player2_y,
                        alpha=1, lw=line_width, zorder=2, color="green", ax = ax["pitch"])



fig.suptitle("PSIM passing network vs Persela", fontsize = 25)
plt.show()
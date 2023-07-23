import pandas as pd
import matplotlib.pyplot as plt
from soccerplots.radar_chart import Radar


# Read the data
data = pd.read_excel(r"C:\Users\rofiq\Downloads\Pizza chart test.xlsx")


# Filter the player

data = data[(data["Nama"]=="Rifal Lastori") | (data["Nama"]=="Andre Agustiar Prakoso")].reset_index()


# List of accepted column names
accepted_columns = ['Nama', 'Goal', 'Total shots', 'Shot accuracy', 'Total passes', 'Pass accuracy',
                    'Key pass to overall pass ratio', 'Key pass', 'Total aerial duels',
                    'Aerial duels effectiveness', 'Total tackles', 'Tackling effectiveness',
                    'Pressure', 'Interception', 'Recovery']

# Filter the DataFrame based on the accepted columns
filtered_data = data[accepted_columns]

# Reset the index of the filtered DataFrame
filtered_data.reset_index(drop=True, inplace=True)

data=filtered_data


# Get parameters
params = list(data.columns)
params = params[1:]


# Add ranges to list
ranges = []
a_values = []
b_values = []

for x in params:
    a = min(data[params][x])
    a = a - (a*0.25)

    b = max(data[params][x])
    b = b + (b*0.25)

    ranges.append((a,b))

for x in range(len(data["Nama"])):
    if data["Nama"][x] == "Rifal Lastori":
        a_values = data.iloc[x].values.tolist()
    if data["Nama"][x] == "Andre Agustiar Prakoso":
        b_values = data.iloc[x].values.tolist()

a_values = a_values[1:]
b_values = b_values[1:]

values = [a_values,b_values]

# Title

title = dict(
    title_name="Rifal Lastori",
    title_color = "red",
    subtitle_name = "PSIM",
    subtitle_color = "red",
    title_name_2="Andre Agustiar Prakoso",
    title_color_2 = "green",
    subtitle_name_2 = "PSIM",
    subtitle_color_2 = "green",
    title_fontsize = 18,
    subtitle_fontsize=15
)

#endnote = "@rofiq_naufal \ndata via FBREF / Statsbomb"

# Plot the radar

radar = Radar()
fig,ax = radar.plot_radar(ranges=ranges, params=params, values=values,
                          radar_color=["red","green"],
                          alphas=[0.75,0.6],
                          title=title,
                          compare=True)

plt.show()

import pandas as pd
from mplsoccer import PyPizza, FontManager
from scipy import stats
import math
import matplotlib.pyplot as plt

# Load the data
data = pd.read_excel(r"C:\Users\rofiq\Downloads\Pizza chart test.xlsx")

# Load fonts
font_normal = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/roboto/'
                          'Roboto%5Bwdth,wght%5D.ttf')
font_italic = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/roboto/'
                          'Roboto-Italic%5Bwdth,wght%5D.ttf')
font_bold = FontManager('https://raw.githubusercontent.com/google/fonts/main/apache/robotoslab/'
                        'RobotoSlab%5Bwght%5D.ttf')


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

# parameter list
params = list(data.columns)
params = params[1:]

print(params)

# Player filter and value setting
for x in range(len(data["Nama"])):
    if data["Nama"][x] == "Rifal Lastori":
        playervalues = data.iloc[x].values.tolist()

playervalues=playervalues[1:]

values=[]
for x in range(len(params)):
    values.append(math.floor(stats.percentileofscore(data[params[x]],playervalues[x])))

print(values)

# instantiate PyPizza class
baker = PyPizza(
    params=params,                  # list of parameters
    straight_line_color="#000000",  # color for straight lines
    straight_line_lw=1,             # linewidth for straight lines
    last_circle_lw=1,               # linewidth of last circle
    other_circle_lw=1,              # linewidth for other circles
    other_circle_ls="-."            # linestyle for other circles
)

# plot pizza
fig, ax = baker.make_pizza(
    values,              # list of values
    figsize=(8, 8),      # adjust figsize according to your need
    param_location=110,  # where the parameters will be added
    kwargs_slices=dict(
        facecolor="cornflowerblue", edgecolor="#000000",
        zorder=2, linewidth=1
    ),                   # values to be used when plotting slices
    kwargs_params=dict(
        color="#000000", fontsize=12,
        fontproperties=font_normal.prop, va="center"
    ),                   # values to be used when adding parameter
    kwargs_values=dict(
        color="#000000", fontsize=12,
        fontproperties=font_normal.prop, zorder=3,
        bbox=dict(
            edgecolor="#000000", facecolor="cornflowerblue",
            boxstyle="round,pad=0.2", lw=1
        )
    )                    # values to be used when adding parameter-values
)

# add title
fig.text(
    0.515, 0.97, "Robert Lewandowski - FC Bayern Munich", size=18,
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

# add subtitle
fig.text(
    0.515, 0.942,
    "Percentile Rank vs Top-Five League Forwards | Season 2020-21",
    size=15,
    ha="center", fontproperties=font_bold.prop, color="#000000"
)

# add credits
# CREDIT_1 = "data: statsbomb viz fbref"
# CREDIT_2 = "inspired by: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"
#
# fig.text(
#     0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}", size=9,
#     fontproperties=font_italic.prop, color="#000000",
#     ha="right"
# )

plt.show()


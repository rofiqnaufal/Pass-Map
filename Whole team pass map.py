import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
plt.style.use("Solarize_Light2")


data = pd.read_csv(r"E:\Work Stuff\Analisis PSIM\2022-09-19 FC Bekasi City vs PSIM\FC Bekasi vs PSIM lengkap.csv")
data['X'] = data['X']*1.3
data['Y'] = data['Y']*0.9
data['X2'] = data['X2']*1.3
data['Y2'] = data['Y2']*0.9

print(data)

# Create figure
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)

# Pitch Outline & Centre Line
plt.plot([0, 0], [0, 90], color="black")
plt.plot([0, 130], [90, 90], color="black")
plt.plot([130, 130], [90, 0], color="black")
plt.plot([130, 0], [0, 0], color="black")
plt.plot([65, 65], [0, 90], color="black")

# Left Penalty Area
plt.plot([16.5, 16.5], [65, 25], color="black")
plt.plot([0, 16.5], [65, 65], color="black")
plt.plot([16.5, 0], [25, 25], color="black")

# Right Penalty Area
plt.plot([130, 113.5], [65, 65], color="black")
plt.plot([113.5, 113.5], [65, 25], color="black")
plt.plot([113.5, 130], [25, 25], color="black")

# Left 6-yard Box
plt.plot([0, 5.5], [54, 54], color="black")
plt.plot([5.5, 5.5], [54, 36], color="black")
plt.plot([5.5, 0.5], [36, 36], color="black")

# Right 6-yard Box
plt.plot([130, 124.5], [54, 54], color="black")
plt.plot([124.5, 124.5], [54, 36], color="black")
plt.plot([124.5, 130], [36, 36], color="black")

# Prepare Circles
centreCircle = plt.Circle((65, 45), 9.15, color="black", fill=False)
centreSpot = plt.Circle((65, 45), 0.8, color="black")
leftPenSpot = plt.Circle((11, 45), 0.8, color="black")
rightPenSpot = plt.Circle((119, 45), 0.8, color="black")

# Draw Circles
ax.add_patch(centreCircle)
ax.add_patch(centreSpot)
ax.add_patch(leftPenSpot)
ax.add_patch(rightPenSpot)

# Prepare Arcs
leftArc = Arc((11, 45), height=18.3, width=18.3, angle=0, theta1=310, theta2=50, color="black")
rightArc = Arc((119, 45), height=18.3, width=18.3, angle=0, theta1=130, theta2=230, color="black")

# Draw Arcs
ax.add_patch(leftArc)
ax.add_patch(rightArc)

# Tidy Axes
plt.axis('off')

# Invert y axis
plt.gca().invert_yaxis()

# Plotting the passes
for i in range(len(data)):
   if data["Event"][i] == "Pass (successful)":
        plt.scatter(data["X"][i], data["Y"][i], color="green",alpha=0.02, s=70)
        x,y= (data["X"][i]), (data["Y"][i])
        dx,dy = (float(data["X2"][i]))-(float((data["X"][i]))), (float(data["Y2"][i]))-(float((data["Y"][i])))
        successarrow=plt.arrow(x,y,dx,dy, width=0.7, head_width=2, color="green",alpha=0.02, linestyle="-", label="Successful")
   if data["Event"][i] == "Pass (failed)":
       plt.scatter(data["X"][i], data["Y"][i], color="red", alpha=0.02, s=70)
       x, y = (data["X"][i]), (data["Y"][i])
       dx, dy = (float(data["X2"][i])) - (float((data["X"][i]))), (float(data["Y2"][i])) - (float((data["Y"][i])))
       failedarrow=plt.arrow(x,y,dx,dy, width=0.7, head_width=2, color="red", alpha=0.02, linestyle=":", label="Failed")
   if data["Event"][i] == "Key pass":
       plt.scatter(data["X"][i], data["Y"][i], color="orange", marker="*", alpha=1, s=70)
       x, y = (data["X"][i]), (data["Y"][i])
       dx, dy = (float(data["X2"][i])) - (float((data["X"][i]))), (float(data["Y2"][i])) - (float((data["Y"][i])))
       keyarrow=plt.arrow(x,y,dx,dy, width=0.7, head_width=2, color="orange", alpha=1, linestyle="-", label="Key Pass")

#Legend
plt.legend(handles=[successarrow,failedarrow, keyarrow],bbox_to_anchor=(0.2, 0.05))

#Direction of attack text
text = "--------------------------->\nDirection of attack"
plt.text(70, 100, text, fontsize=12, ha='center')

#Title
plt.title("Trial pass map",color="black",size=20)

#Show
plt.show()
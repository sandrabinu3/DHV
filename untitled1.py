# -*- coding: utf-8 -*-
"""
Created on Wed Jan  3 01:13:31 2024

@author: bc975789
"""

for_china=forest[forest['Country Name']=='China']
for_china
for_yr=forest.iloc[:,1:]
tot_for=for_yr.sum(axis=0)

plt.subplot(3,2,2)
plt.ylim(4.220000e+08,4.300000e+08)
plt.bar(tot_for.index,tot_for.values,color=colors[5])
for i in range(1, len(tot_for)):
    if tot_for.values[i] < tot_for.values[i - 1]:
        plt.annotate('', xy=(tot_for.index[i - 1], tot_for.values[i - 1]),
                     xytext=(tot_for.index[i], tot_for.values[i]),
                     arrowprops=dict(facecolor='red', edgecolor='red', 
                                     arrowstyle='<-',linewidth=2))
plt.title('Forest area in the world over Years')
plt.xlabel('Year')
plt.ylabel('Forest Area (sq km)')




ax=plt.subplot(3, 2, )

# Define the arrow's starting and ending points
arrow_start = (0.8, 1)  # Starting point (x, y)
arrow_end = (0.8, 0)    # Ending point (x, y)

# Create a FancyArrowPatch
arrow = FancyArrowPatch(arrow_start, arrow_end, arrowstyle='-|>', 
                        mutation_scale=20, color='red',linewidth=3)

# Add the arrow to the plot
plt.gca().add_patch(arrow)

left = 0.1  # Adjust left margin
bottom = 0.4  # Adjust bottom margin
width = 0.1  # Adjust subplot width
height = 0.1  # Adjust subplot height
ax_position = [left, bottom, width, height]
ax.set_position(ax_position)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['bottom'].set_visible(False)
ax.spines['left'].set_visible(False)

# Remove ticks and labels
ax.tick_params(left=False, right=False, top=False, bottom=False, 
               labelleft=False, labelbottom=False)
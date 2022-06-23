import numpy as np
import pandas as pd
from scipy.stats import t
import matplotlib.pyplot as plt


# Create dataframe
df = pd.DataFrame({
    'effectiveness': [
        'Become more aware of cultural differences of people I met', 
        'Better understand the people and culture of my host country', 
        'Be more able to adapt to changes', 
        'Be more open-minded to new experiences', 
        'Enhance my interpersonal skills', 
        'Become more mature and independent'], 
    'mean': [4.3, 4.1, 4.26, 4.4, 4.1, 4.25], 
    'sd': [0.83, 0.87, 0.89, 0.83, 0.92, 0.9]
})
n = 274


# Compute t star with n-1 degrees of freedom
tstar_80 = t.ppf(.90, df=n-1)
tstar_95 = t.ppf(.975, df=n-1)
tstar_99 = t.ppf(.995, df=n-1)
print(tstar_80)
print(tstar_95)
print(tstar_99)


# Compute standard error
df['se'] = df['sd'] / np.sqrt(n)

# Compute confidence interval with 80% confidence
df['lcb80'] = df['mean'] - tstar_80 * df['se']
df['ucb80'] = df['mean'] + tstar_80 * df['se']

# Compute confidence interval with 95% confidence
df['lcb95'] = df['mean'] - tstar_95 * df['se']
df['ucb95'] = df['mean'] + tstar_95 * df['se']

# Compute confidence interval with 99% confidence
df['lcb99'] = df['mean'] - tstar_99 * df['se']
df['ucb99'] = df['mean'] + tstar_99 * df['se']

df = df.sort_values(by='mean')


# Define colors for plotting
BG = '#f9f7f5'
RED = '#b60024'
BLUE1 = '#0070a6'
BLUE2 = '#00adc6'
BLUE3 = '#7ed8e4'
BROWN = '#39240d'

# Set font for entire plot to Serif
plt.rcParams['font.family'] = 'Serif'


# Create 3 subplots, with ratio 1.5:2:1
# The 1st and 3rd subplots are to add spaces
# The 2nd subplot will be used to plot graph
# Set contrained layout to ensure the entire image has a size of 10x10
fig, (s1, ax, s2) = plt.subplots(3, 1, figsize=(10, 10), gridspec_kw={'height_ratios': [1.5, 2, 1]}, dpi=150, constrained_layout=True)


# Set bg color of plot
fig.set_facecolor(BG)
ax.set_facecolor(BG)

# Set 1st and 3rd subplots to invisible
s1.axis('off')
s2.axis('off')


# Plot 80%, 95% and 99% confidence intervals
line1 = ax.hlines(data=df, xmin='lcb80', xmax='ucb80', y='effectiveness', color=BLUE1, linewidth=6, zorder=4)
line2 = ax.hlines(data=df, xmin='lcb95', xmax='ucb95', y='effectiveness', color=BLUE2, linewidth=4, zorder=3)
line3 = ax.hlines(data=df, xmin='lcb99', xmax='ucb99', y='effectiveness', color=BLUE3, linewidth=2, zorder=2)

# Plot the mean
ax.scatter(data=df, x='mean', y='effectiveness', color=RED, linewidth=5, zorder=5)


# Set label of x-axis
ax.set_xlabel('Mean rating (out of 5)', labelpad=15, fontsize=12)

# Set fontsize of tick labels, and remove yticks
ax.tick_params(axis='x', labelsize=12)
ax.tick_params(axis='y', labelsize=12, left=False)

# Remove borders
ax.spines['left'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)


# Add horizontal grid lines
ax.grid(axis='y')

# Add legend
ax.legend(['80%', '95%', '99%',], 
          title='Confidence interval', 
          loc=8, ncol=3, fontsize=12, title_fontsize=12, 
          bbox_to_anchor=(0.5, 0.18), bbox_transform=fig.transFigure, 
          frameon=False)


# Add title
fig.suptitle('Effectivness of Inbound Exchange', y=.93, fontsize=24, fontweight='bold')

# Add subtitle
fig.text(s='The feedback survey results showed that the inbound exchange\nexperience was perceived positive', 
        x=0.5, y=0.83, 
        horizontalalignment='center',
        fontsize=14, 
        linespacing=1.5, 
        transform=fig.transFigure)

# Reference data source
fig.text(s='Source: "Expectations and Experiences of Inbound Exchange Students: \nInsights for Improving the University’s Image", by Annie W.Y. Ng, & Chung-Yee Lee, \nSEACE2020 Conference Proceedings, 2020', 
        x=0.2, y=0.03, 
        fontsize=12, 
        linespacing=2, 
        transform=fig.transFigure)

fig.text(s='Designed by H |\n\n', 
        x=0.05, y=0.03, 
        fontsize=12, 
        linespacing=2, 
        transform=fig.transFigure)


# Save the plot
fig.savefig('exchange', dpi=300)

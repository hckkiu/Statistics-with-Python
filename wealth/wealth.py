import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('dfa-networth-shares.csv')
df['Year'] = df['Date'].apply(lambda x: int(x[:4]))
df = df[['Net worth', 'Category', 'Year']].groupby(['Year', 'Category']).sum().unstack()
df = df.apply(lambda x: x/x.sum() * 100, axis=1)
df.loc[:, ('Net worth', 'Top10')] = df['Net worth']['Top1'] + df['Net worth']['Next9']
df.loc[:, ('Net worth', 'Bottom90')] = df['Net worth']['Next40'] + df['Net worth']['Bottom50']
df = df.stack()
df = df.reset_index()
plt_df = df[(df['Category'] == 'Top10') | (df['Category'] == 'Bottom90')]


plt.rcParams["font.family"] = "serif"

fig, ax = plt.subplots(figsize=(10, 10), facecolor='white', dpi=300)

COLORS = {
    'Top10': '#912d00', 
    'Bottom90': '#006595'
}

ax.tick_params(axis='y', left=False)
plt.ylim(0, 100)
plt.yticks([25, 50, 75, 100], fontsize=14)
plt.ylabel('Share of total wealth (%)', fontsize=14)

ax.tick_params(axis='x', bottom=False)
plt.xlim(1990, 2022)
plt.xticks([1990, 2000, 2010, 2020], fontsize=14)

ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)

for k, v in COLORS.items():
    year = plt_df.loc[(plt_df['Category'] == k), 'Year']
    worth = plt_df.loc[(plt_df['Category'] == k), 'Net worth']
    ax.plot(year, worth, c=v)
    ax.plot(year.iloc[-1], worth.iloc[-1], 'o', c=v)
    ax.annotate(k + ' percent', 
                xy=(year.iloc[-1]+1, worth.iloc[-1]),
                c=v, 
                fontsize=12)

plt.title('The U.S. Household Wealth Distribution', 
             fontsize=28, 
             loc='left', 
             x=-0.08, y=1.14)
ax.text(s='The 10 percent wealthiest households possess almost \n70 percent of the total household wealth', 
        x=-.08, y=1.06, 
        fontsize=18, 
        transform=ax.transAxes)

ax.text(s='H | Data: The Federal Reserve', 
        x=0.5, y=-0.1,
        horizontalalignment='center',
        fontsize=14, 
        transform=ax.transAxes, )

fig.savefig('wealth', bbox_inches='tight')

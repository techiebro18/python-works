import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings
import seaborn as sns
from operator import attrgetter
import matplotlib.colors as mcolors

df = pd.read_csv('vb_orders_20.csv',
                   dtype={'user_id': str,
                          'order_id': str},
                   parse_dates=['received_at'], 
                   infer_datetime_format=True)

#df = df.loc[df['received_at'] >= '2021-01-01 00:00:00' ]

#print(df)
#df.head()
n_orders = df.groupby(['user_id'])['order_id'].nunique()
mult_orders_perc = np.sum(n_orders > 1) / df['user_id'].nunique()
print(f'{100 * mult_orders_perc:.2f}% of customers ordered more than once.')

#Generate Plot/Chart
ax = sns.distplot(n_orders, kde=False, hist=True)
#ax = sns.histplot(n_orders, color="red", label="100% Equities", kde=True, stat="density", linewidth=0)
ax.set(title='Distribution of number of orders per customer',
       xlabel='# of orders', 
       ylabel='# of customers')
#plt.title("Histogram for Total Bill")
#plt.show()

#Cohort Analysis
df = df[['user_id', 'order_id', 'received_at']].drop_duplicates()

df['order_month'] = df['received_at'].dt.to_period('M')
df['cohort'] = df.groupby('user_id')['received_at'] \
                 .transform('min') \
                 .dt.to_period('M') 

df_cohort = df.groupby(['cohort', 'order_month']) \
              .agg(n_customers=('user_id', 'nunique')) \
              .reset_index(drop=False)
df_cohort['period_number'] = (df_cohort.order_month - df_cohort.cohort).apply(attrgetter('n'))

cohort_pivot = df_cohort.pivot_table(index = 'cohort',
                                     columns = 'period_number',
                                     values = 'n_customers')

cohort_size = cohort_pivot.iloc[:,0]
retention_matrix = cohort_pivot.divide(cohort_size, axis = 0)

with sns.axes_style("white"):
    fig, ax = plt.subplots(1, 2, figsize=(12, 8), sharey=True, gridspec_kw={'width_ratios': [1, 11]})
    
    # retention matrix
    sns.heatmap(retention_matrix, 
                mask=retention_matrix.isnull(), 
                annot=True, 
                fmt='.02%', 
                cmap='RdYlGn', 
                ax=ax[1])
    ax[1].set_title('Monthly Cohorts: User Retention', fontsize=16)
    ax[1].set(xlabel='# of periods',
              ylabel='')

    # cohort size
    cohort_size_df = pd.DataFrame(cohort_size).rename(columns={0: 'cohort_size'})
    white_cmap = mcolors.ListedColormap(['white'])
    sns.heatmap(cohort_size_df, 
                annot=True, 
                cbar=False, 
                fmt='g', 
                cmap=white_cmap, 
                ax=ax[0])

    fig.tight_layout()

    plt.show()
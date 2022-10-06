import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
df = pd.read_csv('orders.csv')
#print(df)

#Separate first time customers from returning customers
first_time = df['user_id'].unique()
final = df.loc[df['user_id'].isin(first_time)]

#final = final.drop(columns = ['customer_type'])
final['received_at']= pd.to_datetime(final['received_at'], dayfirst=True)

final = final.sort_values(['user_id','received_at'])
final.reset_index(inplace = True, drop = True)




def purchase_rate(customer_id):
       purchase_rate = [1]
       counter = 1
       for i in range(1,len(customer_id)):
              if customer_id[i] != customer_id[i-1]:
                     purchase_rate.append(1)
                     counter = 1
              else:
                     counter += 1
                     purchase_rate.append(counter)    
       return purchase_rate

def join_date(date, purchase_rate):    
       join_date = list(range(len(date)))    
       for i in range(len(purchase_rate)): 
          if purchase_rate[i] == 1:
                 join_date[i] = date[i]
          else:
                 join_date[i] = join_date[i-1]    
       return join_date

def age_by_month(purchase_rate, month, year, join_month, join_year):    
       age_by_month = list(range(len(year)))    
       for i in range(len(purchase_rate)):          
              if purchase_rate[i] == 1:              
                     age_by_month[i] = 0          
              else:              
                     if year[i] == join_year[i]:                 
                            age_by_month[i] = month[i] - join_month[i]              
                     else:                 
                            age_by_month[i] = month[i] - join_month[i] + 12*(year[i]-join_year[i])     
       return age_by_month


final['month'] =pd.to_datetime(final['received_at']).dt.month
final['Purchase Rate'] = purchase_rate(final['user_id'])
final['Join Date'] = join_date(final['received_at'], final['Purchase Rate'])
final['Join Date'] = pd.to_datetime(final['Join Date'], dayfirst=True)
final['cohort'] = pd.to_datetime(final['Join Date']).dt.strftime('%Y-%m')
final['year'] = pd.to_datetime(final['received_at']).dt.year
final['Join Date Month'] = pd.to_datetime(final['Join Date']).dt.month
final['Join Date Year'] = pd.to_datetime(final['Join Date']).dt.year

final['Age by month'] = age_by_month(final['Purchase Rate'], final['month'],final['year'],final['Join Date Month'],final['Join Date Year'])
cohorts = final.groupby(['cohort','Age by month']).nunique()
cohorts = cohorts.user_id.to_frame().reset_index()   # convert series to frame
cohorts = pd.pivot_table(cohorts, values = 'user_id',index = 'cohort', columns= 'Age by month')
cohorts.replace(np.nan, '',regex=True)

for i in range(len(cohorts)-1):
    cohorts[i+1] = cohorts[i+1]/cohorts[0]
cohorts[0] = cohorts[0]/cohorts[0]


cohorts_t = cohorts.transpose()
cohorts_t[cohorts_t.columns].plot(figsize=(10,5))
sns.set(style='whitegrid')
plt.figure(figsize=(20, 15))
plt.title('Cohorts: User Retention')
sns.set(font_scale = 1) # font size
sns.heatmap(cohorts, mask=cohorts.isnull(),cmap="Blues",annot=True, fmt='.01%')
plt.show()
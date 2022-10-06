from lifetimes import BetaGeoFitter
#import csv
import pandas as pd
from lifetimes.plotting import plot_frequency_recency_matrix, plot_probability_alive_matrix, plot_period_transactions
from matplotlib import pyplot as plt

#df = pd.read_csv('recency_frequency.csv', sep = ',', usecols=[''])
df = pd.read_csv('recency_frequency2.csv', sep = ',')
#print(df['frequency'])
# similar API to scikit-learn and lifelines.
#bgf = BetaGeoFitter(penalizer_coef=0.0)
#bgf = BetaGeoFitter(penalizer_coef=0.125)
bgf = BetaGeoFitter(penalizer_coef=0.001)
bgf.fit(df['frequency'], df['recency'], df['T'])
#print(bgf.summary)

#Visualizing our Frequency/Recency Matrix
#plot_frequency_recency_matrix(bgf)
#plot_probability_alive_matrix(bgf)

#Assessing model fit
#plot_period_transactions(bgf)
#plt.show()

#Ranking customers from best to worst 
t = 1
df['predicted_purchases'] = bgf.conditional_expected_number_of_purchases_up_to_time(t, df['frequency'], df['recency'], df['T'])
print(df.sort_values(by='predicted_purchases').tail(20))

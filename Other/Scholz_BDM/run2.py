# -*- coding: utf-8 -*-
"""
Created on Wed Apr  5 16:39:33 2017

@author: internet
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import itertools
import seaborn as sns
import scholz2

df = pd.read_excel(r'c:\Dropbox\Game Theory\Matlab\BDM\UK_EMU.xlsx', 'UK_EMU_1')
df.dtypes
df.Position = df.Position.astype(float)
df.Capability = df.Capability.astype(float)
#df.Salience = df.Salience/100.0
df.Salience = df.Salience
df.head()

game = scholz2.Game(df)

results = pd.DataFrame(index=df.index)
for i in range(10):
    results[i] = df.Position
    df = game.do_round(df)
    print('----------------------- ROUND:',i,'----------------------------------')
    print(df)
    print('---------------------------------------------------------------------')    
    print('weighted_median', game.weighted_median(), 'mean', game.mean())
    print('---------------------------------------------------------------------')
    
results =  results.T
results.columns = df.Actor
print(results)

plt.style.use('seaborn-whitegrid')
results.plot(figsize=(15,10), colormap='Set1')
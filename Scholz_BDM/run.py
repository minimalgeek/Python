import pandas as pd, sys
import numpy as np, matplotlib.pylab as plt
import scholz, itertools

if len(sys.argv) < 3:
    print "\nUsage: run.py [CSV] [ROUNDS]"
    exit()

df = pd.read_csv(sys.argv[1]); print df
df.Position = df.Position.astype(float)
df.Capability = df.Capability.astype(float)
df.Salience = df.Salience/100.

game = scholz.Game(df)

results = pd.DataFrame(index=df.index)
for i in range(int(sys.argv[2])):
    results[i] = df.Position
    df = game.do_round(df)
    print df
    print 'weighted_median', game.weighted_median(), 'mean', game.mean()

results =  results.T
results.columns = df.Actor
print results
results.plot()
plt.savefig('out-%s.png' % sys.argv[1])
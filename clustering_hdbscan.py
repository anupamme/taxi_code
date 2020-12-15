import hdbscan
import pandas as pd
import numpy as np
from dask import dataframe as dd
from pyspark.sql import SparkSession
import matplotlib.pyplot as plt

spark = SparkSession.builder \
    .master("local") \
    .appName("Word Count") \
    .config("spark.some.config.option", "some-value") \
    .getOrCreate()
    
df = dd.read_csv('/Users/laptop/data/CSPT/top_ten.csv')
print('starting to read')
#df = spark.read.csv('/Users/laptop/data/CSPT/yellow_tripdata_2015.csv')
print('ending to read')
import pdb
pdb.set_trace()
X = np.array(df[['pickup_longitude', 'pickup_latitude']], dtype='float64')
#X = np.array(df[['_c5', '_c6']], dtype='float64')
print('starting to hdbscan')
model = hdbscan.HDBSCAN(min_cluster_size=100, min_samples=5,
                        gen_min_span_tree=True)
#min_cluster_size
#min_samples
#cluster_slection_epsilon
print('starting fit')
model.fit(X)
print('drawing spanning tree')
#model.minimum_spanning_tree_.plot(edge_cmap='viridis',
#                                      edge_alpha=0.6,
#                                      node_size=80,
#                                      edge_linewidth=2)
#model.single_linkage_tree_.plot(cmap='viridis',
#                                      colorbar=True)
model.condensed_tree_.plot()

import pdb
pdb.set_trace()
plt.show()
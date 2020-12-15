import sys
from dask import dataframe as dd
import numpy as np
import geohash_hilbert as ghh

'''
1. Iterate over all the rows:
    1. encode lat long to 10 digit code for pickup and drop off
    2. If there is an entry for this code: increment or insert 1.
    3. sort the map values and plot them in some ways.
'''

def insert_or_increment(_map, _code, freq=1):
    if _code in _map:
        _map[_code] += freq
    else:
        _map[_code] = freq
    return _map

'''
input: list of pair (geohash, frequency).
sort the list on item [0]
iterate the list:
    if item[1] == 1:
        merge up.
'''
def reduce(item_list, freq_val_limit=3000):
    item_list.sort(key=lambda x: x[0])
    new_map = {}
    for geo, freq in item_list:
        if freq <= freq_val_limit:
            new_geo = geo[:-1]
            new_map = insert_or_increment(new_map, new_geo, freq)
        else:
            new_map[geo] = freq
    return list(new_map.items())

'''
Clustering strategies (1):
1. Static (based on number of requests so far)
    1. Minimum #requests (e.g. 10 requests )
    2. Minimum # requests in a time window (e.g. 10 requests in any particular hour)
    3. 

Step 0 (1 day)
If the number of requests in any region > 10
    1. That region qualifies as a leaf node.
    2. If any sibling node is a leaf node, you qualify as a leaf node as well.
    
Plot the number of requests as a function of leaf nodes:
    1. See what is the distribution over the leaf nodes
    2. And distribution at each of the internal nodes.
    

Step 1 (2 days)
Add time as a dimention:
If the number of requests per time interval (e.g. 10 mins) > 10:
    1. That region qualifies as a leaf node
    2. If any sibling node is a leaf node, that node also qualifies as a leaf node
    
Plot the distribution at each leaf node (and internal nodes) as a function of time.
Plot the total distribution as a function of time.

Step 2 (2 days)
Use existing tools for time based forcasting e.g. prphet, neuro-prophet.


(1 week)
Step 3: Temporal Graphs (when we keep the connection intact)
What is the representation? (Figure it out)

(2 days)
Step 4: Add Privacy




    
Explore the dataset and some early insights
0. Strategy for clustering? Min #requests in a day/month
    1. Clustering strategies: can be varied as well.
1. How many regions/clusters/leaf nodes?
    1. Should it depend on traffic density/ number of requests/ static
2. What is the depth of the tree?
3. Can we draw the tree and analyze it
4. Can we draw the pattern of requests in different regions
5. Employ techniques like neural prophet/prophet for this usecase
6. So far we deal with space and time separately.
7. If we decide to not keep the connections in place
8. Time affects the connections: Peak time smaller clusters, lesser peak implies bigger clusters

SHG0 fqw 9G5
'''

if __name__ == "__main__":
    filename = sys.argv[1]
    df = dd.read_csv(filename)
    X = np.array(df[['pickup_longitude', 'pickup_latitude', 'dropoff_longitude', 'dropoff_latitude']], dtype='float64')
    p_map = {}
    import pdb
    d_map = {}
    valid_count = 0
    for idx, item in enumerate(X):
        if item[0] == 0.0:
            continue
        if item[2] == 0.0:
            continue    
        _pcode = ghh.encode(item[0], item[1])
        _dcode = ghh.encode(item[2], item[3])
        p_map = insert_or_increment(p_map, _pcode)
        d_map = insert_or_increment(d_map, _dcode)
        valid_count += 1
    _plist = reduce(reduce(reduce(reduce(reduce(reduce(reduce(list(p_map.items()))))))))
    _plist.sort(key=lambda x: x[1], reverse=True)
    _dlist = reduce(list(d_map.items()))
    _dlist.sort(key=lambda x: x[1], reverse=True)
    pdb.set_trace()
    print(_plist)
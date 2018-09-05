# ===============================================================
#                         IMPORTS
# ===============================================================
import pandas as pd
import matplotlib.pyplot as plt
from math import factorial
from math import inf
import numpy as np
from sklearn.metrics import silhouette_score, adjusted_rand_score
from sklearn.neighbors import KNeighborsClassifier
from sklearn.mixture import GaussianMixture
from skimage.io import imread
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN

# ===============================================================
#                         CONSTANTS
# ===============================================================
RADIUS = 6371

# ===============================================================
#                         CALCULATE nCk
# ===============================================================
def ncr(n, k):
    return factorial(n) // (factorial(k) * factorial(n-k))

# ===============================================================
#                         READ DATA
# ===============================================================  
def read_data():
    
    data = pd.read_csv('tp2_data.csv')
    lat = data.latitude
    long = data.longitude
    faults = data.fault
    
    return lat, long, faults

# ===============================================================
#           CONVERT LAT AND LONG TO CART COORDENATES
# ===============================================================
def lat_long_to_cart(lat,long):
    
    x = RADIUS * np.cos(lat * np.pi/180) * np.cos(long * np.pi/180)
    y = RADIUS * np.cos(lat * np.pi/180) * np.sin(long * np.pi/180)
    z = RADIUS * np.sin(lat * np.pi/180)
    
    return x, y, z  

# ===============================================================
#                         DATA UPDATE
# ===============================================================   
def data_conversion(lat,long):
    
    data = np.zeros((lat.shape[0],3))
    x,y,z = lat_long_to_cart(lat,long)
    data[:,0] = x
    data[:,1] = y
    data[:,2] = z
    
    return data

# ===============================================================
#                      Calc TP,TN, FP, FN
# =============================================================== 
def calc_TP_TN_FP_FN(faults, cluster_labels, cluster_num):
    TP = 0
    TN = 0
    FP = 0
    FN = 0
    N = 0     
    
    aggregated_pairs_per_class = np.zeros((cluster_num+1, 97))
    
    
    for i in range(0, cluster_labels.shape[0]):
        if(cluster_labels[i] != -1 and faults[i] != -1):
            aggregated_pairs_per_class[cluster_labels[i]][faults[i]]+=1
        elif(cluster_labels[i] == -1 and faults[i] != -1):
            aggregated_pairs_per_class[cluster_num][faults[i]]+=1
        elif(cluster_labels[i] != -1 and faults[i] == -1):
            aggregated_pairs_per_class[cluster_labels[i]][96]+=1
        elif(cluster_labels[i] == -1 and faults[i] == -1):
            aggregated_pairs_per_class[cluster_num][96]+=1
        N+=1
    
    #TP
    for i in range(0, cluster_num):
        for j in range(0, 97):
            total_labels = aggregated_pairs_per_class[i][j]
            if(total_labels > 1):
                TP += ncr(total_labels, 2)
    
    #FP
    for i in range(0, cluster_num):
        for k in range(0, 97):
            total_labels = aggregated_pairs_per_class[i][k]
            if(total_labels > 0):
                for j in range(k+1, 97):
                    if(aggregated_pairs_per_class[i][j] > 0):
                        FP+=(total_labels*aggregated_pairs_per_class[i][j])
    
    #FN
    for k in range(0, 97):
        for i in range(0, cluster_num):
            total_labels = aggregated_pairs_per_class[i][k]
            if(total_labels > 0):
                for j in range(i+1, cluster_num):
                    if(aggregated_pairs_per_class[j][k] > 0):
                        FN+=(total_labels*aggregated_pairs_per_class[j][k])
                        
    #TN
    for i in range(0, cluster_num):
        for j in range(0, 97):
            total_labels = aggregated_pairs_per_class[i][j]
            if(total_labels > 0):
                for k in range(i+1, cluster_num):
                    for z in range(0, 97):
                        if((aggregated_pairs_per_class[i][j] > 0) and (j!=z)):
                            TN+=(total_labels*aggregated_pairs_per_class[k][z])

    return N, TP, FP, FN, TN
 
# ===============================================================
#                           SILHOUETTE
# ===============================================================
def intern_idx_silhouette(data, labels):
    
    return silhouette_score(data,labels)

# ===============================================================
#                             ARI
# ===============================================================
def extern_idx_ARI(labels_true, labels_pred):
    
    return adjusted_rand_score(labels_true, labels_pred)

# ===============================================================
#                            RECALL
# ===============================================================
def extern_idx_recall(TP,FN):
    
    return ( TP / (TP + FN) )

# ===============================================================
#                          RAND INDEX
# ===============================================================
def extern_idx_RAND(TP,TN, N):
    
    return ( TP + TN ) / ( ( N * (N - 1) ) / 2 )

# ===============================================================
#                           PRECISION
# ===============================================================
def extern_idx_precision (TP, FP):
    
    return ( TP / (TP + FP) )

# ===============================================================
#                             F1
# ===============================================================
def extern_idx_F1(TP,FP,FN):
    
    return ( 2 * ( (extern_idx_precision(TP,FP) * extern_idx_recall(TP,FN)) / (extern_idx_precision(TP,FP) + extern_idx_recall(TP,FN))))

# ===============================================================
#                             PLOT INDEXES
# ===============================================================
def plot_indexes(indexes, delta, title, x_label, x_fig_size, file_name):
    
    plt.figure(figsize=(x_fig_size, 4))
    silhouette, = plt.plot (indexes[:,0], indexes[:,1], linewidth=3, label = 'Silhouette')
    ari, = plt.plot (indexes[:,0], indexes[:,2], linewidth=3, label = 'ARI')
    rand, = plt.plot (indexes[:,0], indexes[:,3], linewidth=3, label = 'Rand')
    f1, = plt.plot (indexes[:,0], indexes[:,4], linewidth=3, label = 'F1')
    precision, = plt.plot (indexes[:,0], indexes[:,5], linewidth=3, label = 'Precision')
    recall, = plt.plot (indexes[:,0], indexes[:,6], linewidth=3, label = 'Recall')
    plt.xticks(np.arange(min(indexes[:,0]), max(indexes[:,0])+1, delta), fontsize=7, rotation=90)
    plt.grid(b=True, which='major', axis='both')
    plt.xlabel(x_label)
    plt.ylabel('Index Value')
    plt.title(title)
    plt.legend(handles=[silhouette, ari, rand, f1, precision, recall])
    plt.savefig(file_name, dpi=300)
    plt.show()
    plt.close()

# ===============================================================
#                            K_MEANS
# ===============================================================    
def K_Means (data, faults, max_clusters):
    
    indexes = np.zeros((max_clusters-2, 7))
    
    for k in range(2, max_clusters):
       
       kmeans = KMeans(n_clusters = k)
       kmeans.fit(data)
       predicted_labels = kmeans.predict(data)
       
       N, TP, FP, FN, TN = calc_TP_TN_FP_FN(faults, predicted_labels, k)
       
       indexes[k-2][0] = k 
       indexes[k-2][1] = intern_idx_silhouette(data, predicted_labels)
       indexes[k-2][2] = extern_idx_ARI(faults, predicted_labels)
       indexes[k-2][3] = extern_idx_RAND(TP,TN, N)
       indexes[k-2][4] = extern_idx_F1(TP,FP,FN)
       indexes[k-2][5] = extern_idx_precision (TP, FP)
       indexes[k-2][6] = extern_idx_recall(TP,FN)
       
    plot_indexes(indexes, 1, 'K-Means Indexes Variation in Function of K values', 'K Value', 14, 'k_means_indexes.png')
      
    return predicted_labels

# ===============================================================
#                         GAUSSIAN MIXTURE
# ===============================================================
def gaussian_mixture (data, faults, max_components):
    
    indexes = np.zeros((max_components-2, 7))
    
    for gc in range(2, max_components):
        
        gmixture = GaussianMixture(n_components = gc)
        gmixture.fit(data)
        predicted_labels = gmixture.predict(data)
        
        N, TP, FP, FN, TN = calc_TP_TN_FP_FN(faults, predicted_labels, gc)
        
        indexes[gc-2][0] = gc
        indexes[gc-2][1] = intern_idx_silhouette(data, predicted_labels)
        indexes[gc-2][2] = extern_idx_ARI(faults, predicted_labels)
        indexes[gc-2][3] = extern_idx_RAND(TP,TN, N)
        indexes[gc-2][4] = extern_idx_F1(TP,FP,FN)
        indexes[gc-2][5] = extern_idx_precision (TP, FP)
        indexes[gc-2][6] = extern_idx_recall(TP,FN)
     
    plot_indexes(indexes, 1, 'GMM Indexes Variation in Function of C Values', 'C Value', 14, 'gmm_indexes.png')
     
    return predicted_labels

# ===============================================================
#                       PLOT MIN DISTANCES
# ===============================================================  
def plot_min_distances(X, Y):
    
    plt.figure(figsize=(10, 11))
    distances, = plt.plot(X, Y,'-r')
    plt.xlabel('Fault')
    plt.ylabel('Distance (km)')
    plt.yticks(np.arange(0, np.ceil(max(Y))+1,50))
    plt.title('Distance of each point to its fourth-nearest neighbour')
    plt.savefig('min_distances.png', dpi=300)
    plt.show()
    plt.close()
    
# ===============================================================
#                      CALCULATE BEST EPSILON
# ===============================================================
def calc_best_eps(data,faults):
    
    KNN = KNeighborsClassifier(n_neighbors=4)
    KNN.fit(data,faults) 
    distances_to_points, points_indexes = KNN.kneighbors(data,return_distance=True)
    min_distances_to_points = np.zeros(distances_to_points.shape[0])
    
    for i in range (0, distances_to_points.shape[0]):
        min_distance = inf
        for j in range (1, distances_to_points.shape[1]): 
            if (distances_to_points[i][j] < min_distance):
                min_distance = distances_to_points[i][j]
        min_distances_to_points[i] = min_distance
        
    min_distances_to_points = np.sort (min_distances_to_points)
    min_distances_to_points = min_distances_to_points[::-1]
           
    plot_min_distances(np.arange(0,distances_to_points.shape[0]),min_distances_to_points)
    
# ===============================================================
#                           DBSCAN
# ===============================================================
def DB_SCAN (data, lat, lon, faults):
    
    indexes = np.zeros((int((500-50)/10), 7))
    i = 0
    
    for ep in range(50, 500, 10):
        dbscan = DBSCAN(eps = ep, min_samples = 4)
        predicted_labels = dbscan.fit_predict(data)
        
        cluster_num = -inf
        for j in range(0, predicted_labels.shape[0]):
            if(predicted_labels[j] > cluster_num):
                cluster_num = predicted_labels[j]
                
        N, TP, FP, FN, TN = calc_TP_TN_FP_FN(faults, predicted_labels, cluster_num)
        
        indexes[i][0] = ep
        indexes[i][1] = intern_idx_silhouette(data, predicted_labels)
        indexes[i][2] = extern_idx_ARI(faults, predicted_labels)
        indexes[i][3] = extern_idx_RAND(TP,TN, N)
        indexes[i][4] = extern_idx_F1(TP,FP,FN)
        indexes[i][5] = extern_idx_precision (TP, FP)
        indexes[i][6] = extern_idx_recall(TP,FN)
        i+=1
     
    plot_indexes(indexes, 10, 'DBSCAN Indexes Variation in Function of Eps Values', 'Eps Value', 14, 'dbscan_indexes.png')
    
    return predicted_labels
 
# ===============================================================
#                         PLOT GRAPH
# ===============================================================
def plot_classes(labels,lon,lat, alpha=0.5, edge = 'k'):
    
    img = imread("Mollweide_projection_SW.jpg")        
    plt.figure(figsize=(10,5),frameon=False)    
    x = lon/180*np.pi
    y = lat/180*np.pi
    ax = plt.subplot(111, projection="mollweide")
    print(ax.get_xlim(), ax.get_ylim())
    t = ax.transData.transform(np.vstack((x,y)).T)
    print(np.min(np.vstack((x,y)).T,axis=0))
    print(np.min(t,axis=0))
    clims = np.array([(-np.pi,0),(np.pi,0),(0,-np.pi/2),(0,np.pi/2)])
    lims = ax.transData.transform(clims)
    plt.close()
    plt.figure(figsize=(10,5),frameon=False)    
    plt.subplot(111)
    plt.imshow(img,zorder=0,extent=[lims[0,0],lims[1,0],lims[2,1],lims[3,1]],aspect=1)        
    x = t[:,0]
    y= t[:,1]
    nots = np.zeros(len(labels)).astype(bool)
    diffs = np.unique(labels)    
    ix = 0   
    for lab in diffs[diffs>=0]:        
        mask = labels==lab
        nots = np.logical_or(nots,mask)        
        plt.plot(x[mask], y[mask],'o', markersize=4, mew=1,zorder=1,alpha=alpha, markeredgecolor=edge)
        ix = ix+1                    
    mask = np.logical_not(nots)    
    if np.sum(mask)>0:
        plt.plot(x[mask], y[mask], '.', markersize=1, mew=1,markerfacecolor='w', markeredgecolor=edge)
    plt.axis('off')    

# ===============================================================
#                             MAIN
# ===============================================================   
def main():
    
    lat,long, faults = read_data()
    data = data_conversion(lat,long)
    predicted_labels = K_Means (data, faults, 110)
    plot_classes(predicted_labels, long, lat)
    print()
    predicted_labels = gaussian_mixture (data, faults, 110)
    plot_classes(predicted_labels, long, lat)
    print()
    calc_best_eps(data,faults)
    print()
    predicted_labels = DB_SCAN (data, lat, long, faults)
    plot_classes(predicted_labels, long, lat)
    
main()


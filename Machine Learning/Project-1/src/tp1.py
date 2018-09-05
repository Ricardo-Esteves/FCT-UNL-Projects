# ===============================================================
#                           Imports
# ===============================================================
import numpy as np
from sklearn.cross_validation import StratifiedKFold
from sklearn.cross_validation import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.neighbors.kde import KernelDensity
from sklearn.utils import shuffle
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt
import math

# ===============================================================
#                         Constants
# ===============================================================
FOLDS = 5
FEATS = 4

# ===============================================================
#                    Load data from csv file
# ===============================================================
def load_data ():
    
    return np.genfromtxt('TP1-data.csv', delimiter=',')

# ===============================================================
#                   Shuffle the imported data
# ===============================================================
def shuffle_data (data):
    
    return shuffle(data)

# ===============================================================
#                  Standarize the shuffled data
# ===============================================================
def standrize_data (data):
    
    data_values = data [:,:FEATS]
    class_values = data [:,FEATS]
    means = np.mean(data_values,axis=0)
    stdevs = np.std(data_values,axis=0)
    data_values = (data_values-means)/stdevs
    
    return data_values, class_values

# ===============================================================
#                           Split data
# ===============================================================
def split_data(data_values, class_values, size):
    
    return train_test_split(data_values, class_values, test_size = size, stratify = class_values)

# ===============================================================
#                        MacNemar's Test
# ===============================================================
def mac_nemar_test(pred_class_1, pred_class_2, class_test):
    
    e01 = 0
    e10 = 0
    
    for i in range(0, class_test.shape[0]):
        if(pred_class_1[i] == class_test[i] and pred_class_2[i] != class_test[i]):
            e01 += 1
        if(pred_class_1[i] != class_test[i] and pred_class_2[i] == class_test[i]):
            e10 += 1
    
    return float(((abs(e01-e10)-1)**2)/(e01+e10))
    
# ===============================================================
#
#                       Logistic Regression
#
# ===============================================================

# ===============================================================
#              Plot Logistic Regression Errors
# ===============================================================
def plot_logistic_regression_errors(X, Y):
    
    Y = np.array(Y)
    train_err, = plt.plot(X, Y[:,0],'-b',label = 'Training Error')
    valid_err, = plt.plot(X, Y[:,1],'-r',label = 'Valid Error')
    plt.xlabel('Number of Iterations')
    plt.ylabel('Error')
    plt.title('Logistic Regression Errors')
    plt.legend(handles=[train_err, valid_err])
    plt.savefig('logistic_regression_plot.png', dpi=300)
    plt.show()
    plt.close()
    
# ===============================================================
#   Return classification error for train and validation sets
# ===============================================================
def log_reg_calc_fold(X, Y, train_ix, valid_ix, c):
 
  reg = LogisticRegression(C=c, tol=1e-10)
  reg.fit(X[train_ix,:FEATS],Y[train_ix])
  prob = reg.predict_proba(X[:,:FEATS])[:,1]
  squares = (prob-Y)**2
  return np.mean(squares[train_ix]), np.mean(squares[valid_ix])

# ===============================================================
#                       Cross Validation
# ===============================================================
def log_reg_cross_validation (data_train, class_train, k_fold):

    c = 1
    best_c = 0
    min_valid_err = math.inf
    errors = []
    
    for i in range(0,20):
        train_err = valid_err = 0
        for train_ix, valid_ix in k_fold:
            r,v = log_reg_calc_fold(data_train, class_train, train_ix, valid_ix, c)
            train_err += r
            valid_err += v
            if(valid_err < min_valid_err):
                min_valid_err = valid_err
                best_c = c
        errors.append([train_err/FOLDS,valid_err/FOLDS])
        c = c * 2
        
    plot_logistic_regression_errors(np.arange(0, 20), errors)
    
    return best_c
 
# ===============================================================
#                 Train data with the best c
# ===============================================================
def train_log_reg_with_best_c(data_train, data_test, class_train, class_test, best_c):
    
    reg = LogisticRegression(C = best_c, tol = 1e-10)
    reg.fit(data_train,class_train)
    pred_class = reg.predict(data_test)
    
    return pred_class, reg.score(data_test, class_test, sample_weight=None) * 100

# ===============================================================
#                  Apply Logistic Regression
# ===============================================================
def do_logistic_regression(data_train, data_test, class_train, class_test, k_fold):

    best_c = log_reg_cross_validation(data_train, class_train, k_fold)
    pred_class, accuracy = train_log_reg_with_best_c(data_train, data_test, class_train, class_test, best_c)
    
    print("Regression Accuracy: {0:.4f}%".format(accuracy))
    print("Best c value:", best_c)
    print()
    
    return pred_class


# ===============================================================
#
#                       K-Nearest Neighbours
#
# ===============================================================

# ===============================================================
#              Plot K-Nearest Neighbours Errors
# ===============================================================
def plot_knn_errors(X, Y):
    
    Y = np.array(Y)
    train_err, = plt.plot(X, Y[:,0],'-b',label = 'Training Error')
    valid_err, = plt.plot(X, Y[:,1],'-r',label = 'Valid Error')
    plt.xlabel('K Values')
    plt.ylabel('Error')
    plt.title('K-Nearest Neighbours Errors')
    plt.legend(handles=[train_err, valid_err])
    plt.savefig('k_nearest_neighbours_plot.png', dpi=300)
    plt.show()
    plt.close()
    
# ===============================================================
# Return classification error for train and validation sets
# ===============================================================
def knn_calc_fold(X, Y, train_ix, valid_ix, k):

  classifier = KNeighborsClassifier(n_neighbors=k)
  classifier.fit(X[train_ix,:FEATS],Y[train_ix])
  train_err = 1 - classifier.score(X[train_ix,:FEATS], Y[train_ix], sample_weight=None)
  valid_err = 1 - classifier.score(X[valid_ix,:FEATS], Y[valid_ix], sample_weight=None)

  return train_err, valid_err
    
# ===============================================================
#                       Cross Validation
# ===============================================================
def knn_cross_validation(data_train, class_train, k_fold):
    
    best_k = 0
    min_valid_err = math.inf
    errors = []
    
    for k in range(1,39,2):
        train_err = valid_err = 0
        for train_ix, valid_ix in k_fold:
            r,v = knn_calc_fold(data_train, class_train, train_ix, valid_ix, k)
            train_err += r
            valid_err += v
            if(valid_err < min_valid_err):
                min_valid_err = valid_err
                best_k = k
        errors.append([train_err/FOLDS,valid_err/FOLDS])
  
    plot_knn_errors(np.arange(1, 39, 2), errors)
    
    return best_k


# ===============================================================
#                  Train data with the best k
# ===============================================================
def train_knn_with_best_k(data_train, data_test, class_train, class_test, best_k):
    
    knn = KNeighborsClassifier(n_neighbors = best_k)
    knn.fit(data_train,class_train)
    pred_class = knn.predict(data_test)
    
    return pred_class, knn.score(data_test, class_test, sample_weight = None) * 100

# ===============================================================
#                  Apply K-Nearest Neighbours
# ===============================================================
def do_knn(data_train, data_test, class_train, class_test, k_fold):

    best_k = knn_cross_validation(data_train, class_train, k_fold)
    pred_class, accuracy = train_knn_with_best_k(data_train, data_test, class_train, class_test, best_k)
    
    print("Knn Accuracy: {0:.4f}%".format(accuracy))
    print("Best k value:", best_k)
    print()
    
    return pred_class
 
# ===============================================================
#
#                        Naive Bayes
#
# ===============================================================   

# ===============================================================
#              Plot Naive Bayes Errors
# ===============================================================
def plot_naive_bayes_errors(X, Y):
    
    Y = np.array(Y)
    train_err, = plt.plot(X, Y[:,0],'-b',label = 'Training Error')
    valid_err, = plt.plot(X, Y[:,1],'-r',label = 'Valid Error')
    plt.xlabel('Bandwidth (step = 0.02)')
    plt.ylabel('Error')
    plt.title('Naive Bayes Errors')
    plt.legend(handles=[train_err, valid_err])
    plt.savefig('naive_bayes_plot.png', dpi=300)
    plt.show()
    plt.close()

# ===============================================================
#                     Calculate KDE's
# ===============================================================
def calc_kdes(X_train, Y_train, X_valid, bw):

    prob_matrix = np.zeros((2, X_valid.shape[0]))
    
    for i in range(0, 2):
        X_train_class_i = X_train[Y_train == i, :]
        for j in range(0, FEATS):
            kde = KernelDensity(kernel = 'gaussian', bandwidth = bw)
            kde.fit(X_train_class_i[:,[j]])
            log_prob = kde.score_samples(X_valid[:,[j]])
            prob_matrix[i] = np.add(prob_matrix[i], log_prob)

    return prob_matrix

# ===============================================================
#                       Classify data
# ===============================================================
def classify(prob_matrix):
   return np.argmax(prob_matrix, axis = 0)

# ===============================================================
#   Return classification error for train and validation sets
# ===============================================================
def nb_calc_fold(X, Y, train_ix, valid_ix, bw):
    
    X_train = X[train_ix,:FEATS]
    Y_train = Y[train_ix]
    X_valid = X[valid_ix,:FEATS]
    Y_valid = Y[valid_ix]
    
    prob_matrix_valid = calc_kdes(X_train, Y_train, X_valid, bw)
    prob_matrix_train = calc_kdes(X_train, Y_train, X_train, bw)
    
    y_pred_valid = classify(prob_matrix_valid)
    y_pred_train = classify(prob_matrix_train)
    
    train_err = 1 - accuracy_score(Y_train, y_pred_train)
    valid_err = 1 - accuracy_score(Y_valid, y_pred_valid)
    
    return train_err, valid_err 

# ===============================================================
#                       Cross Validation
# ===============================================================
def nb_cross_validation (data_train, class_train, k_fold):
    
    bw = 0.01
    best_bw = 0
    min_valid_err = math.inf
    errors = []
    
    for i in range(0, 50):
        train_err = valid_err = 0
        for train_ix, valid_ix in k_fold:
            r,v = nb_calc_fold(data_train, class_train, train_ix, valid_ix, bw)
            train_err += r
            valid_err += v
            if(valid_err < min_valid_err):
                min_valid_err = valid_err
                best_bw = bw
        errors.append([train_err/FOLDS, valid_err/FOLDS])
        bw = bw + 0.02
        
    plot_naive_bayes_errors(np.arange(0.01, 1, 0.02), errors)
    
    return best_bw
 
# ===============================================================
#             Train data with the best bandwidth
# ===============================================================
def train_nb_with_best_bw(data_train, data_test, class_train, class_test, best_bw):
    
    prob_matrix = calc_kdes(data_train, class_train, data_test, best_bw)
    y_pred = classify(prob_matrix)
    
    return y_pred, accuracy_score(class_test, y_pred) * 100

# ===============================================================
#                      Apply Naive Bayes
# ===============================================================
def do_naive_bayes(data_train, data_test, class_train, class_test, k_fold):
    
    best_bw = nb_cross_validation(data_train, class_train, k_fold)
    pred_class, accuracy = train_nb_with_best_bw(data_train, data_test, class_train, class_test, best_bw)
    
    print("Naive Bayes Accuracy: {0:.4f}%".format(accuracy))
    print("Best bandwidth value: {0:.2f}\n".format(best_bw))
    
    return pred_class
    
# ===============================================================
#                           Main
# ===============================================================
def main ():
    print()
    
    data_values, class_values = standrize_data(shuffle_data(load_data()))
    
    data_train, data_test, class_train, class_test = split_data(data_values, class_values, 0.33)
    k_fold = StratifiedKFold(class_train, n_folds = FOLDS)
    
    reg_log_pred_class = do_logistic_regression(data_train, data_test, class_train, class_test, k_fold)      
    knn_pred_class = do_knn(data_train, data_test, class_train, class_test, k_fold)
    nb_pred_class = do_naive_bayes(data_train, data_test, class_train, class_test, k_fold) 

    print("MacNemar's test between the classifiers:")
    print("> Logistic Regression Vs K-Nearest Neighbours: {0:.4f}".format(mac_nemar_test(reg_log_pred_class, knn_pred_class, class_test)))
    print("> Naive Bayes Vs Logistic Regression: {0:.4f}".format(mac_nemar_test(nb_pred_class, reg_log_pred_class, class_test)))
    print("> K-Nearest Neighbours Vs Naive Bayes: {0:.4f}".format(mac_nemar_test(knn_pred_class, nb_pred_class, class_test)))

    
main()
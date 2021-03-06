# Machine Learning <img align="right" width="100" height="50" src="https://camo.githubusercontent.com/b2029ffe76b249d5bdd72d48611937651db6a96a/68747470733a2f2f692e696d6775722e636f6d2f4c304e4c616a582e706e67">

    - In this course, we had to develop two projects in groups of two students.
    - The language used was Python.

## Project 1

The goal of this project was to parametrize, fit and compare ***Logistic Regression***, ***K-Nearest Neighbours*** and ***Naïve Bayes*** classifiers, given a data set from the ***UCI machine learning*** repository. To accomplish this, we had to select the best regularization parameter for the ***Logistic Regression***, select the best K value for the ***K-Nearest Neighbours*** classifier and select the best bandwidth parameter for the Kernel Density Estimators used in the ***Naïve Bayes*** classifier. Besides, we had to make our own implementation of the ***Naïve Bayes*** classifier.

Finally, to compare the performance of the three classifiers and select the best one, we use the ***McNemar's test*** with a 95% confidence interval.

## Project 2

In this project the goal was to examine the performance of three different clustering algorithms in the problem of clustering seismic events, given an excel dataset with all seismic events of magnitude at least 6.5 in the last 100 years, obtained from the ***USGS catalog***. The three clustering algorithms that we use were: ***K-Means***, ***DBSCAN*** and ***Gaussian Mixture Models***. First, we started by varying the main parameter of each algorithm and then using an internal index, the silhouette score, and external indexes: Rand index, Precision, Recall, F1 measure, and the adjusted Rand index. 

Finally, we had to choose what is the best clustering algorithm by comparing the most relevant test that we made to the tree algorithm.

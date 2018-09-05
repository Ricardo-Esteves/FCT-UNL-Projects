# Machine Learning

In this course we had to develop two projects in groups of two students. The language used was Python.
Also, we mainly used the Scikit-learn library to complement some of the projects' goals.

## Project 1

The goal of this project is to parametrize, fit and compare ***Logistic Regression***, ***K-Nearest Neighbours*** and ***Naïve Bayes*** classifiers, given a data set from the ***UCI machine learning*** repository. To do this, we had to select the best regularization parameter for the ***Logistic Regression***, select the best k value for the ***K-Nearest Neighbours*** classifier and select the best bandwidth parameter for the Kernel Density Estimators used in the ***Naïve Bayes*** classifier. Furthermore, we had to make our own implementation of the ***Naïve Bayes*** classifier by using the Scikit-learn library for the Kernel Density Estimators.

Finally, to compare the performance of the three classifiers and select the best one, we resorted to the ***McNemar's test*** with a 95% confidence interval.

## Project 2

In this project the goal is to examine the performance of three different clustering algorithms in the problem of clustering seismic events, given a data set with all seismic events of magnitude at least 6.5 in the last 100 years, obtained from the ***USGS catalog***. These three clustering algorithms are: ***K-Means***, ***DBSCAN*** and ***Gaussian Mixture Models***. We started by varying the main parameter of each algorithm and then using an internal index, the silhouette score, and external indexes: Rand index, Precision, Recall, F1 measure and the adjusted Rand index, to compare each clustering algorithm.

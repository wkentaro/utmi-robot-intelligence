#!/usr/bin/env python
#-*- coding: utf-8 -*-
# test_mnist.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

import numpy as np

from sklearn.datasets import fetch_mldata
from sklearn.preprocessing import LabelBinarizer
from sklearn.cross_validation import train_test_split
from sklearn.metrics import (
        classification_report,
        accuracy_score,
        confusion_matrix
        )

import nn


def test_mnist(corruption_level=0.0, epochs=10000, verbose=False):
    # load train data
    mnist = fetch_mldata('MNIST original')
    X = mnist.data
    y = mnist.target
    target_names = np.unique(y)

    # standardize
    X = X.astype(np.float64)
    X /= X.max()

    clf = nn.NN(ni=X.shape[1], nh=100, no=len(target_names), corruption_level=0.0)

    X_train, X_test, y_train, y_test = train_test_split(X, y)

    # convert train data to 1-of-k expression
    label_train = LabelBinarizer().fit_transform(y_train)
    label_test = LabelBinarizer().fit_transform(y_test)

    clf.fit(X_train, label_train, epochs=epochs)

    y_pred = np.zeros(len(X_test))
    for i, xt in enumerate(X_test):
        o = clf.predict(xt)
        y_pred[i] = np.argmax(o)
    # print y_pred

    score = accuracy_score(y_true=y_test, y_pred=y_pred)
    if verbose is True:
        print classification_report(y_true=y_test, y_pred=y_pred)
        print confusion_matrix(y_true=y_test, y_pred=y_pred)
        print score

    return score


if __name__ == '__main__':
    test_mnist()
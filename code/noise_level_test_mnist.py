#!/usr/bin/env python
# -*- coding: utf-8 -*-
# noise_level_test_mnist.py
# author: Kentaro Wada <www.kentaro.wada@gmail.com>

from __future__ import print_function
import time
import cPickle
import gzip

import numpy as np
import matplotlib.pyplot as plt
from termcolor import cprint

from test_mnist import test_mnist


def noise_level_test_mnist():
    print("... doing noise_level test")
    scores, x = [], []
    epochs = 150000
    corruption_level=0.1
    for nl in np.arange(0, 13) * 0.02:
        try:
            print("...... noise_level: {0}".format(nl), end='')
            score, _ = test_mnist(corruption_level=corruption_level,
                                  noise_level=nl,
                                  learning_rate=0.3,
                                  inertia_rate=0.12,
                                  nh=0.16,
                                  epochs=epochs,
                                  verbose=False)
            scores.append(score)
            x.append(nl)
            print(" score: {0}".format(score))
        except KeyboardInterrupt:
            break
    scores = np.array(scores)
    x = np.array(x)
    print("--- done")

    print("... plotting test result")
    print("...... plotting scores")
    # plot graph
    ax1 = plt.subplot()
    ax1.plot(x, scores)
    ax1.set_title('noise_level and score with {0}'.format(epochs))
    ax1.set_xlabel('noise_level')
    ax1.set_ylabel('score')
    # for label
    ax2 = plt.subplot()
    label_text = r"""
        $\mu = %.5f$
        $\sigma = %.5f$
        """ % (scores.mean(), scores.std())
    label = ax2.text(0.05, 0.05, label_text,
            horizontalalignment='left',
            verticalalignment='bottom',
            transform=ax2.transAxes)
    plt.savefig('../output/noise_level_test_mnist_nsmpl{0}_cl{1}.png'.format(epochs, corruption_level))
    print("--- done")

    print("... saving the results")
    dump_data = {'noise_level': x,
                 'score': scores}
    with gzip.open('../output/noise_level_test_mnist.pkl.gz', 'wb') as f:
        cPickle.dump(dump_data, f)
    print("--- done")


if __name__ == '__main__':
    noise_level_test_mnist()
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)

from nose.plugins.attrib import attr
from nose.tools import assert_raises, raises

import numpy as np
from numpy.random import RandomState
from numpy.testing import assert_equal, assert_almost_equal, assert_array_less
from scipy.stats import hypergeom, binom
from cryptorandom.cryptorandom import SHA256

from ..ksample import (k_sample, 
                       one_way_anova,
                       bivariate_k_sample,
                       two_way_anova)
import permute.data as data
from permute.utils import get_prng


def test_worms_ksample():
    worms = data.worms()
    res = k_sample(worms.x, worms.y, stat='one-way anova', reps=1000, seed=1234)
    assert_array_less(0.006, res[0])
    assert_array_less(res[0], 0.02)


def test_one_way_anova():
    group = np.ones(5)
    x = np.array(range(5))
    xbar = np.mean(x)
    assert_equal(one_way_anova(x, group, xbar), 0)
    
    group = np.array([1]*3 + [2]*2)
    expected = 3*1**2 + 2*1.5**2
    assert_equal(one_way_anova(x, group, xbar), expected)


def test_two_way_anova():
    prng = get_prng(100)
    group1 = np.array([1]*5 + [2]*5)                                              
    group2 = np.array(list(range(5))*2)                                           
    x = prng.randint(1, 10, 10)
    xbar = np.mean(x)
    val = two_way_anova(x, group1, group2, xbar)
    assert_almost_equal(val, 0.296, 3)
    
    x = group2 + 1
    xbar = 3
    assert_equal(two_way_anova(x, group1, group2, xbar), 1)


def test_testosterone_ksample():
    testosterone = data.testosterone()
    x = np.hstack(testosterone.tolist())
    group1 = np.hstack([[i]*5 for i in range(len(testosterone))])
    group2 = np.array(list(range(5))*len(testosterone))
    assert_equal(len(group1), 55)
    assert_equal(len(group2), 55)
    assert_equal(len(x), 55)
    res = bivariate_k_sample(x, group1, group2, reps=5000, seed=5)
    assert_array_less(res[0], 0.0002)

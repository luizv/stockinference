from durable.lang import *
import redis
import numpy as np
import pandas as pd
import time
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

### REDIS
# We need Redis to work. Just install redis on your computer.
#
# Redis install tutorial (mac):
# https://medium.com/@petehouston/install-and-config-redis-on-mac-os-x-via-homebrew-eb8df9a4f298
#
# To run Redis local server, type on Terminal (mac):
# redis-server /usr/local/etc/redis.conf
#
# Port 6379 is default. To change it, just edit redis.conf


pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
r.flushall()

with statechart('stock'):

    with state('input'):
        @to('start')
        @when_all(+m.close)
        def test1(c):
            print('input -> start')

    with state('start'):
        @to('step1')
        @when_all(+m.close)
        def test2(c):
            print('input -> start')

    with state('step1'):
        @to('step2')
        @when_all(+m.low and +m.high)
        def test3(c):
            min_touches = 2
            stat_likeness_percent = 1.2
            bounce_percent = 5
            sup = None
            res = None

            # Identifying local high and local low
            maxima = np.array(c.m.high).max()
            minima = np.array(c.m.high).min()

            # Calculating distance between max and min (total price movement)
            move_range = maxima - minima

            # Calculating bounce distance and allowable margin of error for likeness
            move_allowance = move_range * (stat_likeness_percent / 100)
            bounce_distance = move_range * (bounce_percent / 100)

            # Test resistance by iterating through data to check for touches delimited by bounces
            touchdown = 0
            awaiting_bounce = False
            for x in range(0, np.array(c.m.high).size):
                if abs(maxima - np.array(c.m.high)[x]) < move_allowance and not awaiting_bounce:
                    touchdown = touchdown + 1
                    awaiting_bounce = True
                elif abs(maxima - np.array(c.m.high)[x]) > bounce_distance:
                    awaiting_bounce = False
            if touchdown >= min_touches:
                res = maxima

            # Test support by iterating through data to check for touches delimited by bounces
            touchdown = 0
            awaiting_bounce = False
            for x in range(0, np.array(c.m.low).size):
                if abs(np.array(c.m.low)[x] - minima) < move_allowance and not awaiting_bounce:
                    touchdown = touchdown + 1
                    awaiting_bounce = True
                elif abs(np.array(c.m.low)[x] - minima) > bounce_distance:
                    awaiting_bounce = False
            if touchdown >= min_touches:
                sup = minima
            c.assert_fact({'res': res, 'sup': sup})

    with state('step2'):
        @to('step3')
        @when_all(+m.res > 0)
        def test4(c):
            average_fast = pd.Series(np.array(c.m.close)).rolling(window=20).mean()
            mm20Close = average_fast[pd.Series(average_fast).last_valid_index()]
            average_slow = pd.Series(np.array(c.m.close)).rolling(window=5).mean()
            mm5Close = average_slow[pd.Series(average_slow).last_valid_index()]
            mm5Close_previous = pd.Series(m.mm5Close).shift(1)
            mm20Close_previous = pd.Series(m.mm20Close).shift(1)
            c.assert_fact({"mm20Close": mm20Close, "mm5Close": mm5Close, "mm5Close_previous": mm5Close_previous, "mm20Close_previous": mm20Close_previous})

    with state('step3'):
        @to('step4')
        @when_all((m.mm5Close <= m.mm20Close) and (m.mm5Close_previous >= m.mm20Close_previous))
        def test6(c):
            print("Buy")

    with state('step4'):
        @to('step5')
        @when_all((m.mm5Close >= m.mm20Close) and (m.mm5Close_previous <= m.mm20Close_previous))
        def test8(c):
            print("Sell")

    with state('step5'):
        @to('start')
        @when_all(+m.close)
        def test10(c):
            print("return")

    @when_start
    def start(host): pass

run_all([{'host': 'localhost', 'port': 6379}])

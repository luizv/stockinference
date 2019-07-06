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


def mm(period, data, shift=1):
	return pd.Series(np.array(data)).rolling(window=period).mean().iloc[-shift]

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
            print('start -> step1')

    with state('step1'):
        @to('step2')
        @when_all(m.low.allItems(item > 0) and m.high.allItems(item > 0))
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

            print("resistence %0.2f" % res)
            print("support %0.2f" % sup)

            c.post({'res': res, 'sup': sup})

    with state('step2'):
        @to('step3')
        @when_all(+m.close)
        def test4(c):
            print('step2 -> step3')
            # average_fast = pd.Series(np.array(c.m.close)).rolling(window=20).mean().iloc[:-1]
            # average_slow = pd.Series(np.array(c.m.close)).rolling(window=5).mean()
            mm5close = mm(5, c.m.close, 1) #average_fast.iloc[:-1] #average_slow[pd.Series(average_slow).last_valid_index()]
            mm20close = mm(20, c.m.close, 1) #average_slow.iloc[:-1] #average_fast[pd.Series(average_fast).last_valid_index()]
            print("OK")
            mm5close_previous = mm(5, c.m.close, 2) #average_fast[pd.Series(average_fast).last_valid_index()-1]
            mm20close_previous = mm(20, c.m.close, 2) #average_slow[pd.Series(average_slow).last_valid_index()-1]
            print("passou:%0.2f" % mm20close)
            c.post({"mm20Close": float(mm20close), "mm5Close": float(mm5close), "mm5Close_previous": float(mm5close_previous), "mm20Close_previous": float(mm20close_previous)})

    with state('step3'):
        @to('step4')
        @when_all((m.mm5Close <= m.mm20Close) and (m.mm5Close_previous >= m.mm20Close_previous))
        def test6(c):
            print("Buy")

        @to('step4')
        @when_all(+m.close)
        def test6(c):
            print("testa sell")


    with state('step4'):
        @to('step5')
        @when_all((m.mm5Close >= m.mm20Close) and (m.mm5Close_previous <= m.mm20Close_previous))
        def test8(c):
            print("Sell")

        @to('start')
        @when_all(+m.close)
        def test6(c):
            print("return")

    with state('step5'):
        @to('start')
        @when_all(+m.close)
        def test10(c):
            print("return")

    @when_start
    def start(host): pass

run_all([{'host': 'localhost', 'port': 6379}])

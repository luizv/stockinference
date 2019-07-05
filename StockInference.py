from durable.lang import *
import redis
import numpy as np
import pandas as pd
import time

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
def testetrue():
    return True

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
r.flushall()




with statechart('stock'):
    with state('input'):
        @to('start')
        @when_all(+m.close)
        def test(c):
            print('input -> start')

    with state('start'):
        @to('next')
        @when_all(+m.low)
        def test1(c):
            #print(c.m.low)
            mm5 = pd.Series(np.array(c.m.close)).rolling(window=5).mean()
            print(mm5)
            print('start -> next')

    with state('next'):
        @to('finish')
        @when_all(+m.low)
        def test2(c):
            print('next -> finish')

    with state('finish'):
        @to('buy')
        @when_all(+m.low)
        def test3(t):
            print('finish -> buy')

    with state('buy'):
        @to('start')
        @when_all(+m.low)
        def test4(t):
            print('buy -> start')




    @when_all(m.close.allItems(item > 185) & m.open.allItems(item > 150) & m.high.allItems(item > 185))
    def rule0(c):
        print("entrou")


    # # matching primitive array
    # @when_all(m.values.anyItem(item > 0))
    # def rule1(c):
    #     print('fraud 1 detected {0}'.format(c.m.values))
    #
    #
    # # matching object array
    # @when_all(m.values.allItems((item.amount < 250) | (item.amount >= 300)))
    # def rule2(c):
    #     print('fraud 2 detected {0}'.format(c.m.values))
    #
    #
    # # pattern matching string array
    # @when_all(m.cards.anyItem(item.matches('three.*')))
    # def rule3(c):
    #     print('fraud 3 detected {0}'.format(c.m.cards))
    #
    #
    # # matching nested arrays
    # @when_all(m.values.anyItem(item.allItems(item < 100)))
    # def rule4(c):
    #     print('fraud 4 detected {0}'.format(c.m.values))


    @when_start
    def start(host): pass
        # host.post('stock', {'value': [150], 'open': [150], 'high': [150], 'low': [150], 'volume': [150]})
        # host.post('stock', {'open': [100]})
        # host.post('stock', {'high': [100]})
        # host.post('stock', {'low': [100]})
        # host.post('stock', {'volume': [100]})

run_all([{'host': 'localhost', 'port': 6379}])
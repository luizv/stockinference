from durable.lang import *
import redis
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

pool = redis.ConnectionPool(host='localhost', port=6379, db=0)
r = redis.Redis(connection_pool=pool)
r.flushall()

with ruleset('stock'):

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
    def start(host):
        host.post('stock', {'value': [150], 'open': [150], 'high': [150], 'low': [150], 'volume': [150]})
        # host.post('stock', {'open': [100]})
        # host.post('stock', {'high': [100]})
        # host.post('stock', {'low': [100]})
        # host.post('stock', {'volume': [100]})

run_all([{'host': 'localhost', 'port': 6379}])
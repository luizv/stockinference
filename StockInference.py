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

with ruleset('risk'):
    # matching primitive array

    @when_all(m.values.allItems((item > 100) | (item < 150)))
    def rule1(c):
        print('fraud 1 detected {0}'.format(c.m.values))


    # matching object array
    @when_all(m.values.allItems((item.amount < 250) | (item.amount >= 300)))
    def rule2(c):
        print('fraud 2 detected {0}'.format(c.m.values))


    # pattern matching string array
    @when_all(m.cards.anyItem(item.matches('three.*')))
    def rule3(c):
        print('fraud 3 detected {0}'.format(c.m.cards))


    # matching nested arrays
    @when_all(m.values.anyItem(item.allItems(item < 100)))
    def rule4(c):
        print('fraud 4 detected {0}'.format(c.m.values))


    @when_start
    def start(host):
        host.post('risk', {'values': [150, 300]})
        host.post('risk', {'values': [{'amount': 200}, {'amount': 300}, {'amount': 450}]})
        host.post('risk', {'cards': ['one card', 'two cards', 'three cards']})
        host.post('risk', {'values': [[10, 20, 30], [30, 40, 50], [10, 20]]})


run_all([{'host': 'localhost', 'port': 6379}])
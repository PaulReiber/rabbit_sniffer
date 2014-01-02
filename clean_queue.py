#!/usr/bin/env python
from kombu import Connection, Exchange, Queue
import json

import sys
import signal

user = 'guest'
password = 'guest'
host = 'localhost'
port = '5672'

exchange_name = 'nova'
routing_key_name = '*'

queue_name = 'tracing-nova-all'

tracing_exchange = Exchange(exchange_name, 'topic', durable=False, auto_delete=False, internal=False)
compute_queue = Queue(queue_name, exchange=tracing_exchange, routing_key=routing_key_name)

full_path = 'amqp://%(user)s:%(password)s@%(host)s:%(port)s//' \
          % { 'user'     : user \
            , 'password' : password \
            , 'host'     : host \
            , 'port'     : port }

with Connection(full_path) as conn:
    compute_queue_bound = compute_queue(conn)

    compute_queue_bound.delete()
    print "Cleaned up queues"

# vim: ts=4 sw=4 et



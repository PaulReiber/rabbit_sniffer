#!/usr/bin/env python
from kombu import Connection, Exchange, Queue

import sys

if len(sys.argv) < 2:
    print >> sys.stderr, "Need one argument: [routing_key]"
    sys.exit(1)

#user = 'nova'
user = 'guest'
#password = 'D0xwYTR1'
password = 'guest'
host = 'localhost'
port = '5672'

exchange_name = 'nova'
routing_key_name = sys.argv[1]

queue_name = 'tracing-queue-' + routing_key_name

tracing_exchange = Exchange(exchange_name, 'topic', durable=False, auto_delete=False, internal=False)
compute_queue = Queue(queue_name, exchange=tracing_exchange, routing_key=routing_key_name)

def process_media(body, message):
    print "------ message start --------"
    print "delivery info:    %s" % message.delivery_info
    print "headers:          %s" % message.headers
    print "properties:       %s" % message.properties
    print "body:             %s" % message.body
    print "------ message end ----------"
    message.ack()

full_path = 'amqp://%(user)s:%(password)s@%(host)s:%(port)s//' \
          % { 'user'     : user \
            , 'password' : password \
            , 'host'     : host \
            , 'port'     : port }

with Connection(full_path) as conn:
    with conn.Consumer(compute_queue, callbacks=[process_media]) as consumer:
        while True:
            conn.drain_events()

# vim: ts=4 sw=4 et

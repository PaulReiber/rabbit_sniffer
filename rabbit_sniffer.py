#!/usr/bin/env python

from kombu import Connection, Exchange, Queue
from contextlib import nested

import json
import sys
import signal

# Configuration section

user = 'guest'
password = 'guest'
host = 'localhost'
port = '5672'

# Main code

nova_exchange = Exchange('nova', 'topic', durable=False, auto_delete=False, internal=False)
nova_queue = Queue('tracing-nova-all', exchange=nova_exchange, routing_key="*")

openstack_exchange = Exchange('openstack', 'topic', durable=False, auto_delete=False, internal=False)
openstack_queue = Queue('tracing-openstack-all', exchange=openstack_exchange, routing_key="*")

def process_nova(body, message):
    with open('nova.log', 'a') as f:
        process_message(f, body, message)

def process_openstack(body, message):
    with open('openstack.log', 'a') as f:
        process_message(f, body, message)

def process_message(f, body, message):
    f.write("------ message start --------\n")
    f.write("delivery info:    %s\n" % message.delivery_info)
    f.write("headers:          %s\n" % message.headers)
    f.write("properties:       %s\n" % message.properties)
    f.write("body:\n")
    bb = json.loads(message.body)
    f.write(json.dumps(bb, sort_keys=True, indent=4, separators=(',', ': ')))
    f.write("\n------ message end ----------\n")
    message.ack()

full_path = 'amqp://%(user)s:%(password)s@%(host)s:%(port)s//' \
          % { 'user'     : user \
            , 'password' : password \
            , 'host'     : host \
            , 'port'     : port }

with Connection(full_path) as conn:
    nova_queue_bound = nova_queue(conn)
    openstack_queue_bound = openstack_queue(conn)

    def handler(signum, frame):
        nova_queue_bound.delete()
        openstack_queue_bound.delete()
        print "Cleaned up queues"

    signal.signal(signal.SIGINT, handler)
    consumers = [ conn.Consumer(nova_queue, callbacks=[process_nova])
                , conn.Consumer(openstack_queue, callbacks=[process_openstack])
                ]
    with nested(*consumers):
        while True:
            conn.drain_events()

# vim: ts=4 sw=4 et ai

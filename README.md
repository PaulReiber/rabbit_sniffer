Rabbitmq Sniffer
================

This sniffer allows you to dump all messages from nova exchange on your
rabbitmq server.

Usage
-----

- Copy rabbit_sniffer.py and run_sniffer.sh to the controller node.
- Edit user and password variables in rabbit_sniffer.py under
Configuration section.
- Modify host and port in rabbit_sniffer.py if necessary.
(Normally it's not required)
- Run sniffer with the following command:

```
 # ./rabbit_sniffer.py
```

This command will dump messages from nova exchange to nova.log and all messages
from openstack exchange to openstack.log file. If you want to interrupt the
sniffer press ctrl-c.

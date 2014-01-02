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

If you want to collect all messages from nova, then run

```
 # run_sniffer.sh "*"
```

If you want to specify routing key, then put routing key instead of "*". Make
sure you put your routing key pattern inside quotes, otherwise bash can expand
*.

You can list all available routing keys using the following command:

```
 # rabbitmqctl list_bindings | grep nova
```

This command prints all bindings which are already present
on the rabbitmq server for nova exchange.

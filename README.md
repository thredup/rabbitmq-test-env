## RabbitMQ Test Environment
This repository is a local sandbox for developers to experiment with, providing 2 Rabbitmq hosts, 1 producer, and 1 consumer.


### Setup
1. Run `docker-compose up` to setup all containers.
*  The rabbitmq containers take a while to start up, resulting in consumers and producers terminating with connection errors until a connection is established.
*  In order to consume messages from both hosts, federation queue must be setup
3. To setup federations queues, run `sync.py` in the `scripts` directory.

Note: rabbitmq configuration is kept in a set of volumes. For a restart with clean configs, the volumes associated with the container must be deleted.

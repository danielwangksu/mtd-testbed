## Intro

The controller is where all the magic lives, so there's a lot of stuff on it

This guide relies on the host having a static IP address (through DHCP or whatever) and a set
hostname (for the Puppet CA and ActiveMQ)

## Components

First, we'll install MongoDB, Python and pysphere

    apt-get install mongodb python python-dev python-pip
    pip install mongo mongoengine
    pip install pysphere

Next, we'll install everything for Puppet, MCollective and ActiveMQ

    apt-get install puppet puppetmaster mcollective activemq

Let's clear out the included cert for the Puppetmaster

    puppet cert clean --all
    puppet cert generate hurricane.mgmt.nw.com --dns_alt_names=puppet,puppet.mgmt.nw.com
    service puppetmaster restart

Next, we'll setup the configuration for ActiveMQ

    cd /etc/activemq/instances-available
    mkdir mcollective
    cd mcollective
    nano activemq.xml
    nano log4j.properties
    cd ../instances-enabled
    ln -s ../instances-available/mcollective mcollective
    service activemq restart

Alternatively, here's how to setup RabbitMQ with STOMP support

	apt-get install rabbitmq-server
	rabbitmq-plugins enable rabbitmq_stomp rabbitmq_management
	nano /etc/rabbitmq/rabbitmq.config
	rabbitmqctl add_user mcollective marionette
	rabbitmqctl add_user admin secret
	rabbitmqctl delete_user guest
	rabbitmqctl set_user_tags mcollective mcollective
	rabbitmqctl set_user_tags admin mcollective administrator
	rabbitmqctl set_permissions -p / mcollective ".*" ".*" ".*"
	rabbitmqctl set_permissions -p / admin ".*" ".*" ".*"

Finally, we'll update the configuration for MCollective

    nano /etc/default/mcollective
    nano /etc/mcollective/server.conf
    service mcollective restart

Test out your config using `mco ping`
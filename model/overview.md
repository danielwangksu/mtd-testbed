## Moving-Target Defense Model

Modeling something complex as MTD requires a set of layered models that are specialized
for different aspects of the system.

### Requirement Model

This is the highest view of the system that the stakeholder is typically exposed to. This
model consists of the following elements:

* Services
* Dependencies
* Resources

A service is a process or set of processes, in the Linux sense. This would be like an
Apache HTTP server, MongoDB, RabbitMQ, NFS, MySQL, etc. Services are what the 
organization requires to fulfill its mission.

A dependency represents a connection between two services. An example of this would be
a web application depending on a MySQL server.

A resource is a bare-metal server, virtualization resource (VMware, LXC, EC2, etc.)
or network link (WAN, inter-datacenter links).

Services and dependencies are applied to resources using different adaptation and
clustering strategies.

*TODO* How do we define clusters of services? 1 master + n slaves, many master, etc.
The term cluster is used in terms of failover/fault tolerance and load balancing. As in,
multiple instances that provide the same service.

### Logical Model

This model represents a snapshot of the state that the network is currently in.

* Instances
* Interfaces
* Switches
* Roles

An instance is anything that contains an operating system and one or more services.

An interface is simply a network interface (NIC) that exists on an instance. These
are either physical or virtual.

A switch is either a physical or virtual switch. Ideally, a physical switch would support
VLAN management via OpenFlow. 
*TODO* Is there a more generic term we could use instead of switch? (perhaps a network, 
subnet, boundary, zone)

An instance can have one or more roles; a role is simply a service that the instance
provides.



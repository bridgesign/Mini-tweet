# Mininet Experiment

The experiment is defined in `experiment.py`. Before running the experiment, the DB server uses postgres. It is necessary to change the configuration files to allow database login to the specific hosts. For simplicity, it is best to allow for all hosts. The changes need to be made in the postgres configuration file. Its better to make a copy and pass the postgres server the directory with the config files. Also, the required path changes need to be made in the config file path given to the DB server in experiment file.

## Details of Experiment

The `client.py` file is used to simulate clients. Each client signs-up itself and then makes some tweets. Then they follow a few set of users and request for the feed. As such the experiment is carried out with 4 server instances and 100 clients, each client having 7Mbps link. The load is equally balanced hence each server instance is handling 25 clients.

It is important to note that the consistency is maintainied by using a common database server. Each thread of the server is given a connection to the DB. This makes sure that the number of connections to the DB server is limited and there is no issue of overflowing the max-pool allowed connections.

In the experiment, every client SignsUp and accquires the token required for futher actions. After this, each client makes a fixed but different tweet. All clients then follow all other clients which belong to the same client cluster (explained in next section). After this, the clients request for feed from the server. As such, all clients are going to parallely and which request gets processes first is not fixed and hence the output can change each time though.

## Details of Topology

For a good simulation, there is a single router, named main gateway, that connects the servers and the DB server. The main gateway is connected to another switch called main switch. The main switch is connected to a set of b-switches. Each b-switch has connections to a fixed number of switches. Each switch is attached to a cluster of clients. From the topology, it is clear that the bottleneck is the bandwidth between main gateway and main switch, which is kept as 1Gbps.

## Further experiments

The size of client cluster, number of client clusters and server instances can be varied. Hence, `experiment.py` can be used to check the scaling of the servers. The client files can be modified to create more complicated user interactions.

## Notes for running the Experiment

Internally, the DB server starts postgresql server. For this, it is important to make sure that no other instance of postgres server is running and all related sessions are closed. Moreover, after the experiment is completed, it is possible that the postgres server does not get properly terminated as this is only an emulation. In such cases, it is necessary to terminate the postgres instances left intact. There will be a mininet CLI prompt after the DB server starts the DB process. This can be used to make sure that the DB server is properly running and clients and servers are able to communicate with each other.

The simulation for 1000 clients was not possible due to hardware constraints.
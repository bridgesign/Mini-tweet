# Mininet Experiment

The experiment is defined in `experiment.py`. Before running the experiment, the DB server uses postgres. It is necessary to change the configuration files to allow database login to the specific hosts. For simplicity, it is best to allow for all hosts. The changes need to be made in the postgres configuration file. Its better to make a copy and pass the postgres server the directory with the config files. Also, the required path changes need to be made in the config file path given to the DB server in experiment file.

## Details of Experiment

The `client.py` file is used to simulate clients. Each client signs-up itself and then makes some tweets. Then they follow a few set of users and request for the feed. As such the experiment is carried out with 4 server instances and 100 clients. The load is equally balanced hence each server instance is handling 25 clients.

It is important to note that the consistency is maintainied by using a common database server. Each thread of the server is given a connection to the DB. This makes sure that the number of connections to the DB server is limited and there is no issue of overflowing the max-pool allowed connections.

## Details of Topology

For a good simulation, there is a single router, named main gateway, that connects the servers and the DB server. The main gateway is connected to another switch called main switch. The main switch is connected to a set of b-switches. Each b-switch has connections to a fixed number of switches. Each switch is attached to a cluster of clients.

## Further experiments

The size of client cluster, number of client clusters and server instances can be varied. Hence, `experiment.py` can be used to check the scaling of the servers. The client files can be modified to create more complicated user interactions.
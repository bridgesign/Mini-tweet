# Mini-tweet
[Demo Video](https://drive.google.com/file/d/1C3gVeFz8uUYy6ZR1keTnxTZ2CW59v46d/view?usp=sharing)

Mini-twitter project for Computer Networks (CS 433) course at IITGN.

As being a networks project, the development focus is more on the modularity of the server, the API framework and scalability of the implementation. For this reason, the complete project is distributed into two major parts: The server and the API module.

To start the server run `python3 main.py`. It will start the server at http://localhost:8080

## Requirements

1. Python 3
2. Pyscopg2
3. Requests
4. PostgreSQL
5. Mininet (Python 2 required for this)

Only python3 is a hard requirement. Psycopg2 and PostgreSQL is required only for the implementation of twitter-like functionalities. Similarly, requests library and Mininet are required for client side testing purpose. Otherwise, the server and API implementation are independent of these requirements. 

## Philosophy

All modules must be independent of the other as much possible. For this reason everything is modelled as objects routing outputs to other objects which may be shared by multiple threads. Specifically, any request-response is seen as individual objects and there is an object responsible for handling them and routing any inputs coming from previous work.

For clarity, consider a stack of layers L1, L2 and L3. Then only one layer is allowed to directly interact with outside (client). Suppose that to be L1. L1 is responsible for forwarding information to L2. Moreover, L1 is responsible for starting any kind of execution at L2. It cannot start by itself. Any kind of information transferred from L1 to L2 is not copied unless another copy is explicity required. In contrast L3 (the last layer) is allowed to interact on its own violation with the inside (database).

The reason for this is that it can allow server side pushing of data. Another reason for this is to make sure that there are no dependency loops. A number of modules can be at the same level but there cannot be communication directly between two modules in the same layer. It should be noted that a module's existence (in the sense that it is actively participating) is a primary condition for actually considering the module. Also, a module in any layer is free to bring another module in existence or destroy it in another layer below it (L1 module is allowed to create or destory a module in L2). The actual heirarchy of the modules is dependent on how they came into existence. What this implies is that the heirarchy is fluid and can be changing during execution.

## Server

The server is implemneted purely using sockets. It creates a thread pool for handling the incoming requests. How the server will handle these requests depends on the handlers provided for handling. The deafult provided handlers are for an HTTP server. As such the server can be easily decoupled to use with custom handlers. Similarly, the server only handles a request which is then given response handler. When the server handles returned response handler, only then the response is sent to the client.

The current server implementation also ties itself with the provided `views.py`. Similar to the django framework, the views module allows creating url patterns and routes the requests from the handler to the target definition. The `settings.py` allow to set globals and shared settings for the server, for exmaple the static files folder.

### Handlers

There are two handlers: `httprequest` and `httpresponse`

The *httprequest* handler is responsible for parsing the HTTP header and constructing a request object that can be returned back to the server.

The *httpresponse* handler is responsible for constructing the object that will properly reply back to the client when it is handled.

### Views

The views can be used to process an *httprequest* and return a *httpresponse* object.

## API

The API module is largely inspired from GraphQL. Though the views module can be directly used to create a REST API, the API module provides a parser that can be used for easily developments of API calls. The `shcema.py` file can be used for defining the various methods. In the parser, it is possible to extend the number of base schema types.

Following the philosophy of GraphQL, the same endpoint can be used for all the queries. Moreover, the API call is oblivious to the number of different connections it is maintaing to the database or a number of databases. The developer is free to use a number of databases at a time which may not be of the framework.

## Structure

The following shows the layer structure of the current implementation:

|Layer | Module |
|------|--------|
|1| Server   |
|2| Handler  |
|3| Views    |
|4| API      |
|5| Database |

In terms of file structure, the https package contains the server module and the api package the API module. Further documentation can be found for each package in its folder. The documentation folder contains the details of Twitter Specific implementation and the Mininet Testing.

## Notes

The DB name used throughout is *twitter*. The credentials used by the server is taken from environment variables: HOST, DB, USER and PASS. These are hard-coded in `experiment.py` while under normal run it is needs to be set by the user.

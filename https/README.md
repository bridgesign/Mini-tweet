# Server Package

The server package is divided into the server module, handler module and views module.

## Server Module

The server module creates a pool of threads. It has two methods: serve and handle. The serve method is used to accept connections and then use the thread pool to handle the connection using handle method. It is dependent on the Handler and Views Modules. Though it can directly interact with both, the Views Module is at a lower layer than Handler Module because a view cannot operate without a handler.

## Handler Module

The handler module consists of *httprequest* and *httpresponse* handles. The request object extracts out the headers and the body. The header consists of the HTTP method, url, cookies and other meta data passed from the client. The response object takes the request as one of its arguments. The response can either be a string or binary string. Other options to set the reply headers and return code is also provided as arguments.

## Views Module

The views module can be separated into patterns and view handlers. The patterns are just a mapping of regular expressions for url and the view handler. The view handlers are passed the handler request object by the server module. In response, the view handler gives back a handler response object.

## Settings and Utils File

The settings file is used to define constants and Package wide settings. The utils file contains helper functions or helper abstractions. Currently, an abstraction for HTTP cookie is provided which can be used by handler response object to construct set-cookie header.
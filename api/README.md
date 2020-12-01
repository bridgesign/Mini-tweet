# API Package

The API package is split into parser and schema. Though these are not separate entities. The schema only provides the methods that can be used by the parser. Hence, the whole can be seen as a single API Module.

## Schema

The schema can be used to define as many basic classes as required. The classes need to be registered to the parser by adding it to the parser schema mapping. GraphQL has three main classes: Query, Mutation and Subscription. In the same format, it is defined in the schema file. In addition, there is an Error abstraction provided which can be used to pass on errors to the parser.

The classes define the scope of the function i.e. a query is supposed to only read data. It is only for developmental ease and there is no direct check on it. Each class method is passed the context which is extracted from the request by the View module. Further more, the parser when declared can be given all the resources it going to use such as DB cursor and connection objects which are passed on to the classes, and are shared across API requests. To understand how this works, let us take an example of `login` method. It requires the arguments `username` and `password`. The expected output is the login `token`. The POST query of the client will thus require the following json data:

```{"Query":"login":({"username":some_username, "password":some_password}, "token")}```

On successful login, the server will reply with the following data:

```{"data":{"token":generated_token}}```

In current implementation, this token can be used as cookie in the following requests to prove the identity of the user. The token will be extracted and passed into the context object (ctx) in the class methods.

If there is an error, the reply will be of the form:

```{"Error":error_message, "code":some_integer_code}```

## Parser

The parser is responsible for calling the proper schema method from the request data. Moreover, the parser can handle nested request. It is possible that one needs to get data about your friends or followers. But you only need the names of the followers, which are also users. In such a case, it is possible to construct a query that will only return the names. This does not require any kind of extra work on the server side. The server is capable of returning all the data using a single method yet the parser can enforce a query structure to allow client to query only the required data.

## Example Queries

```{"Mutation":{"create_profile":({"username":username, "password":pass}, "token")}}```

SignsUp the user and returns the token

```
{"Mutation":{
	"create_tweet":(
		{"tweet_content":"Hi! I am Banri", "tags":[], "mentions_list":[]}, ('tweet_post',{'user':'user_name'}
		))
	}
}
```

This will return the following response

```{"data":{"tweet_post":"Hi! I am Banri", "user":{"user_name":Tada}}}```

As such, the information requested by the client is only the posted content and the username of the one who has posted.

```{"Mutation":{"follow":({"username":"Yana Koko"}, "status")}}```

Here the client only requires to know the status of the request.

```{"Query":{"twitter_feed":({}, (['tweets', ('tweet_post',{'user':'user_name'})],))}}```

Here, the feed will return a list of tweets. This is indicated by putting a list inside the return arguments. The client is requesting for the tweet content given by `tweet_post` and the username of the user who posted it. The nested dictionary directs the parser tp understand that the object given by a tweet on user call is *User object* and hence it needs to further query data to get the username.
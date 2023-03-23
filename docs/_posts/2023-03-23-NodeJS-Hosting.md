---
layout: post
title:  "NodeJS Hosting"
summary: "From Client to Server"
author: moomoohorse
date: '2023-03-23 12:32:08 -0500'
category: ['web']
thumbnail: /assets/img/posts/covidweb2.png
keywords: NodeJS
permalink: /blog/nodejs-hosting
usemathjax: true
---

# NoeJS Hosting Tutorial 

In this tutorial I'm going to cover the following objective with a simple NodeJS hosting website as an example.

## Example Structure

The website is basically in following structure.


```bash

.
├── app.js
├── bin
│   └── www
├── docs
│   ├── documents
├── node_modules
│   ├── a bunch of packages
├── package-lock.json
├── package.json
├── public
│   ├── javascripts
│   └── stylesheets
├── routes
│   ├── account.js
│   ├── contributors.js
│   ├── dashboard.js
│   ├── dbconfig.js
│   ├── index.js
│   ├── main.js
│   ├── papers.js
│   └── users.js
└── views
    ├── account.ejs
    ├── contributors.ejs
    ├── dashboard.ejs
    ├── error.ejs
    ├── index.ejs
    ├── main.ejs
    └── menu.ejs

84 directories, 21 files
```

The website basically have 4 tabs (pages), each of which contains a certain generic functionality. Many websites (actually most websites) do this. So I think this website can be a really nice example as a starting point to develop a NodeJS hosting service.

<img src="..\assets\img\posts\covidweb1.png" alt="image-20230323123720211" style="zoom: 50%;" />

The account page can be used to log user in and register users. It's very nice example because it involves Client side and Server operations. It also provides us with a template to leverage the communication between server - server (our NodeJS hosting server and SQL server) and server to client. 

<img src="..\assets\img\posts\covidweb2.png" alt="image-20230323124019913" style="zoom:50%;" />


## Objectives 

* What's `/views` `/routes` `/public` 
    * Pattern shifting : from HTML, CSS, JS to NojeJS hosting

* Why app.js? 
    * What's its relation with public / router / views folders?

* What's EJS?
    * what's the relations between EJS and HTML?

* What's API? What's require('path/to/API')? 
    * What's module.exports?
    * Client asks for a specific path to some API, but you can't see API stored in our server, so what exactly is API? What are we doing with API?

* Why can two router file both have get('/',...)? 
    * Won't they cause some conflicts because they both intercept requests for root directory? 

* What's root directory ('/') to request? 
    * Hint : understand app.use('/', indexRouter);

* How does app.js know our views are in format of .ejs and how does it know that our view engine is in views directory?

### From HTML, CSS, JS to NodeJS hosting

When we create a website using HTML, CSS, and JavaScript, we typically have a directory structure that includes folders such as `/public`, `/views`, and `/routes`. These folders are used to organize our website's static assets, dynamic templates, and server-side logic.

The /public folder is where we store all our static assets, such as CSS and JavaScript files. These files are served directly to the client's web browser, without any processing or modification by the server.

The /views folder is where we store our dynamic templates, which are used to generate HTML content using server-side data. In a NodeJS hosting website, we typically use a view engine such as EJS or Handlebars to generate dynamic content.

The /routes folder is where we store all the server-side logic for handling HTTP requests. In a NodeJS hosting website, we typically use a web framework such as Express to handle routing and middleware.

When we shift from a traditional HTML/CSS/JavaScript website to a NodeJS hosting website, we need to make some changes to our directory structure and code organization. We need to create an app.js file that serves as the entry point for our NodeJS hosting server. We also need to install and configure various packages and modules that are required to run our server and handle HTTP requests.

In addition, we need to refactor our HTML/CSS/JavaScript code to work with the view engine and server-side data. This involves breaking up our HTML code into smaller, reusable components that can be dynamically rendered using EJS or Handlebars. We also need to organize our CSS and JavaScript code into separate files and folders, and load them dynamically using server-side code.

Overall, the transition from a traditional HTML/CSS/JavaScript website to a NodeJS hosting website involves a significant amount of restructuring and refactoring. However, the benefits of using a NodeJS hosting architecture can include faster development, better scalability, and more efficient resource utilization.

### Understanding app.js
app.js is the entry point for our NodeJS hosting website. It's where we define our server and all its routes. When we run the app.js file, our NodeJS hosting server will start listening to incoming HTTP requests. In the context of our example website, app.js is the file that sets up our server and ties together all the other components of our website.

### What's EJS?
EJS stands for Embedded JavaScript, which is a template language that enables us to generate dynamic HTML content. EJS templates are written in HTML, but with additional syntax for injecting dynamic content. We can use EJS to generate dynamic pages based on data we fetch from our database, or based on some user input.

### What's API?
API stands for Application Programming Interface, which is a set of protocols, routines, and tools for building software applications. In the context of our NodeJS hosting website, an API is a way for us to expose certain functionality to other developers or to other parts of our website.

When we use `require('path/to/API')`, we are importing a module into our `app.js` file. This module contains functions or classes that we can use to perform certain actions. We typically use module.exports to expose these functions or classes to other parts of our website.

HTTP requests are used to communicate between the client-side and server-side of a web application. In a NodeJS hosting environment, the client-side typically sends HTTP requests to the server-side using the Axios library, while the server-side handles these requests using the Express framework.

There are several types of HTTP requests, but the most common ones are GET and POST. The GET request is used to retrieve data from the server-side, while the POST request is used to submit data to the server-side for processing.

In the context of an API, HTTP requests are used to exchange data between the client-side and server-side.

When we use an API in a NodeJS hosting environment, we typically define routes or endpoints that handle different types of HTTP requests. For example, we might define a route for handling GET requests to retrieve user data, and a separate route for handling POST requests to create new users.

The Express framework provides a simple and flexible interface for defining these routes and handling different types of HTTP requests. We can use the `router.get()` function to define a route that handles GET requests, and the `router.post()` function to define a route that handles POST requests.

For example, suppose we have an API endpoint `/api/users` that handles GET and POST requests for user data. We can define this endpoint in our Express server using a router like this:

```javascript
const express = require('express');
const router = express.Router();

// Handle GET request for user data
router.get('/api/users', (req, res) => {
  // Retrieve user data from database or other source
  res.send(users);
});

// Handle POST request for creating a new user
router.post('/api/users', (req, res) => {
  // Process POST request and create new user
  res.send(newUser);
});

module.exports = router;
```
In this example, we define a route for handling GET requests to `/api/users`, and a separate route for handling POST requests to create new users. When the client-side sends a GET request to `/api/users`, the server-side code in the `router.get()` function will retrieve user data and send it back to the client-side. When the client-side sends a POST request to `/api/users`, the server-side code in the `router.post()` function will create a new user and send back the newly created user to the client-side.

By using GET and POST requests in combination with Express and Axios in our NodeJS hosting environment, we can create a powerful and flexible API that allows different applications to communicate with each other and exchange data.

### Express and Axois : Communication between server and client

In a NodeJS development environment, the router plays a critical role in handling incoming HTTP requests and routing them to the appropriate server-side code. The router is responsible for matching URLs to specific server-side functions or modules, and for handling different HTTP methods such as GET, POST, and DELETE.

In the context of a React application, we typically use a web framework such as Express to handle routing and middleware. Express is a popular web framework for NodeJS hosting that provides a simple and flexible interface for handling HTTP requests and responses.

When the client-side of a React application sends a request to the server-side, it typically uses the Axios library to send HTTP requests such as GET and POST. Axios is a popular client-side library for making HTTP requests from a web browser, and it provides a simple and flexible interface for sending and receiving data from the server-side.

For example, suppose we have a website with a route `/api/users` that handles requests for user data. We can define this route in our Express server using a router like this:

```javascript
const express = require('express');
const router = express.Router();

router.get('/api/users', (req, res) => {
  // Handle GET request for user data
});

router.post('/api/users', (req, res) => {
  // Handle POST request for creating a new user
});

module.exports = router;

```
In this example, we define two routes for handling GET and POST requests to `/api/users`. When the client-side sends a GET request to `/api/users`, the server-side code in the `router.get()` function will handle the request and return user data. When the client-side sends a POST request to `/api/users`, the server-side code in the `router.post()` function will handle the request and create a new user.

By using Express and Axios in our NodeJS hosting environment, we can create a flexible and scalable architecture for handling HTTP requests and responses between the client-side and server-side of our React application.

### Why can two router file both have get('/',...)?
In Express, the `app.use()` method is used to mount middleware functions at a specified path. When we mount a router using `app.use('/', router)`, it means that the router will be used to handle all incoming HTTP requests that match the root directory `'/'`.

It's okay to have two router files both have `get('/',...)` because they are mounted at different paths. For example, we could have a mainRouter that handles the root directory `'/'` and a usersRouter that handles `'/users'`. These routers can have different logic for handling incoming HTTP requests, but they won't conflict because they are mounted at different paths.

### What's root directory ('/') to request?
In HTTP, the root directory `'/'` refers to the home directory of the website. When a client sends an HTTP request to `'/'`, they are essentially asking for the default page of the website.

In the context of our NodeJS hosting website, we use `app.use('/', indexRouter)` to mount our indexRouter at the root directory. This means that any incoming HTTP requests to `'/'` will be handled by the indexRouter.

### How does app.js know our views are in format of .ejs and how does it know that our view engine is in views directory?

When we create a NodeJS hosting website, we typically use a view engine to render dynamic content. The view engine is a module that allows us to generate HTML content using dynamic data. In our case, we're using EJS as our view engine.

To tell our app.js file that we're using EJS as our view engine, we use the following line of code:

```javascript
app.set('view engine', 'ejs');
```
This line of code tells Express that we'll be using EJS as our view engine. Now, when we render a view using `res.render()`, Express will know to look for an EJS file in our views folder.

To tell Express where our views folder is located, we use the following line of code:

```javascript
app.set('views', path.join(__dirname, 'views'));
```
This line of code sets the location of our views folder to be in the same directory as our app.js file. Now, when we render a view using `res.render()`, Express will know to look for the view file in the views folder.

In summary, we use `app.set('view engine', 'ejs')` to tell Express that we're using EJS as our view engine, and we use `app.set('views', path.join(__dirname, 'views'))` to tell Express where our views folder is located. This allows us to render dynamic content using EJS templates in our NodeJS hosting website.


### Asyc nature of React (Express and Axois)

React is an asynchronous JavaScript library, which means that it can handle multiple operations at once without blocking the execution of other code. This allows React to be fast and responsive, even when dealing with complex user interfaces and large amounts of data.

When we make HTTP requests using Axios in a React application, the response data is typically handled using the `then()` method of a Promise. The `then()` method is a callback function that is executed when the Promise is resolved, which means that the response data has been received from the server-side.

For example, suppose we have a React component that makes a GET request to an API endpoint to retrieve user data:

```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios.get('/api/users')
      .then(response => {
        setUsers(response.data);
      });
  }, []);

  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```
In this example, we use the `useEffect()` hook to make a GET request to `/api/users` and set the user data in the component state using `setUsers()`. When the Promise returned by `axios.get()` is resolved, the `then()` method is executed with the response data as its argument. The response data is then passed to `setUsers()` to update the component state.

One issue with asynchronous operations like this is that they can introduce timing issues and unexpected behavior. For example, if we have code that relies on the response data being available before it can be executed, we might run into issues if the response data has not yet been received.

To resolve this problem, we can use Promises to ensure that the response data is available before executing any dependent code. Promises are objects that represent the eventual completion (or failure) of an asynchronous operation, and they can be used to chain multiple asynchronous operations together in a predictable and reliable way.

For example, suppose we have a React component that makes a GET request to an API endpoint to retrieve user data, and then makes a POST request to create a new user using the retrieved user data:

```javascript
import React, { useState, useEffect } from 'react';
import axios from 'axios';

function UserList() {
  const [users, setUsers] = useState([]);

  useEffect(() => {
    axios.get('/api/users')
      .then(response => {
        setUsers(response.data);

        return axios.post('/api/users', {
          name: response.data[0].name,
          email: response.data[0].email
        });
      })
      .then(response => {
        console.log('New user created:', response.data);
      });
  }, []);

  return (
    <div>
      {users.map(user => (
        <div key={user.id}>{user.name}</div>
      ))}
    </div>
  );
}
```
In this example, we use the `then()` method of the Promise returned by `axios.get()` to chain a POST request using the retrieved user data. The POST request is executed only after the GET request has successfully completed and the response data has been received. The response data from the POST request is then logged to the console.

By using Promises in this way, we can ensure that our code executes in a predictable and reliable way, even when dealing with complex asynchronous operations in our React application.
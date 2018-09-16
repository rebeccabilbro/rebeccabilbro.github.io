---
layout: post
title:  The Actor Model, for Actors and Models
image:
  feature: pepper_crop.png
tags:   programming
date:   2018-08-23 10:37
---

Lately I've been thinking a lot about use cases for parallelism and concurrency, which has led me to thinking about models of computation that can make operations happen faster and be more tolerant to large amounts of data throughput. In this post, I'll attempt to describe the Actor Model at a very high level, at the expense of much detail and some precision of language, but hopefully in a simple enough way for a layperson to understand.

## Turning Big Problems into Small Problems

At a really high level, computer programming is about breaking up big computation tasks into smaller ones. There are a number of different frameworks for thinking about computation, and there are a number of different paradigms for how to break it down (e.g. functional programming, object-oriented programming). These frameworks and paradigms have different benefits and tradeoffs.

For instance, object-oriented programming features the combining of data and methods (aka encapsulation) in a way that makes it easy to mathematically model the behavior of everyday things like cars and calculators. Cars have data, like mileage, and can also do things, like go forward and stop. Calculators have data, constants like the value of pi, and can also do things, like add and exponentiate.

However, sometimes storing data together with methods can be problematic, like when there's a lot of data, or when certain methods need to get used a lot more than others (which button of your calculator are you most likely to wear out first?).

One strategy for dealing with these challenges is parallelism, which is a way of breaking calculations down so that a lot can be done at the same time. Another approach is concurrency. Concurrency is a way of breaking the big problem down into pieces that don't depend on happening in a specific order.

## The Actor Model

Let's imagine that we're going to make a calculator. In an object-oriented framework, we might imagine the calculator as a class that has some data and some methods. In an actor model approach, we might instead imagine a collection of independent actors that each know how to do one certain kind of computation.

To perform more complex series of computations, it would be most natural for the object-oriented approach to perform them one after another. The actor model could achieve a similar sequence of operations by passing messages between the actors.

![object-oriented vs. actor model](https://raw.githubusercontent.com/rebeccabilbro/rebeccabilbro.github.io/master/images/2018-08-23-actor-model-example.png)

However, if we imagine a context where there is a lot of data flowing through our calculation system, one nice advantage of the actor model approach is that the different actors don't each need to hold data the way the `Calculator` class might, or even need to know much about the full data picture at all. They only need to know what numbers were in the most recent message they received, and they are only responsible for doing one kind of computation on those numbers. Moreover, if certain kinds of operations need to happen a lot more than others (say, adding), it would be pretty easy to just clone the `Adder` to distribute the work to multiple `Adders` and speed up the computation process. Now imagine that we also have a lot of people who want to use the calculator at the same time; sometimes their calculations will affect each other's, but not always. The actor model gives us a way to cleverly perform computations concurrently when possible, and out-of-order whenever that's an option.


## Plan for Implementing a Simple Version of the Actor Model

So here's an idea for how we might go about implementing the actor model approach:

 - create an `Actor` template
     - the `Actor` should have a `queue`
     - the `Actor` should have two functions, `send()` and `run()`
        - `send()` should add messages to a `queue`
        - `run()` should consume messages from its `queue`
     - an `Actor` should have an action handler and an error handler
        - the action handler should deal with the `Actor's` expected messages (e.g. adding, squaring, etc.)
        - the error handler should deal with exceptions (e.g. requests to add things that aren't numbers, divide by zero, etc.)


## Resources

Some of the things I read/watched while musing on this post:

 - [The Actor Model](https://bbengfort.github.io/snippets/2018/08/03/actor-model.html)
  - [Programming Actors with Akka](https://www.safaribooksonline.com/videos/programming-actors-with/9781491990247/9781491990247-video313673)
 - [The Actor Model Explained (video)](https://finematics.com/actor-model-explained/)
 - [Race Conditions and the Actor Model (video)](https://youtu.be/un-pSOlTaY0?t=1m)
 - [Pulsar: The Actor Model implemented in Python](https://github.com/quantmind/pulsar)
 - [Introduction to the Actor Model for Concurrent Computation](https://www.youtube.com/watch?v=lPTqcecwkJg)
 - [Using the Actor Model with Domain-Driven Design (DDD) in Reactive Systems](https://www.youtube.com/watch?v=rMv4sul0RwU)

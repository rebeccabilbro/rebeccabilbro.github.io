---
layout: post
title:  Lessons Learned from Effective Go, Part 2
image:
  feature: pepper_crop.png
tags:   class_notes
date:   2018-08-27 11:25
---

This second post on [Effective Go](https://golang.org/doc/effective_go.html), captures my notes on reading the second half of the official documentation (from initialization through panic and recovery).

Notes on the first half [here](https://rebeccabilbro.github.io/effective-go-pt-1/).

## More Takeaways from Effective Go

### Declaring Constants and Setting State

 - `enum` groups related constants together in one type - timezones, weekdays, etc. (more [here](https://blog.learngoprogramming.com/golang-const-type-enums-iota-bc4befd096d3))
 - `iota` automates `enum` values with a numeric universal counter (more [here](https://blog.learngoprogramming.com/golang-const-type-enums-iota-bc4befd096d3)).
 - Use `iota + 1` to be sure that the `enum` type is initialized.

    ```
    const (
        Sleeping = iota + 1
        Walking
        Running
    )

    func main() {
        var activity Activity
        // activity will be zero,
        // so it's not initialized

        activity = Sleeping
        // now you know that it's been
        // initialized
    }
    ```
 - Unknown state pattern: Start with an `Unknown` to be sure of `enum`’s initialization.

    ```
    const (
        Unknown = iota
        Sleeping
        Walking
        Running
    )
    ```
 -  Use `init` (no args) in a source file to set up whatever state is required

## Pointers
 - A pointer holds the memory address of a value.
 - Type `*T` is a pointer to a T value.
 - The `&` operator generates a pointer to its operand.
 - The `*` operator denotes the pointer's underlying value.
 - pointers vs. values
    - for receivers, value methods can be invoked on pointers and values, but pointer methods can only be invoked on pointers.
 - More [here](https://tour.golang.org/moretypes/1).

## Interfaces
 - Interfaces in Go provide a way to specify the behavior of an object; if the object can do `X`, then it can be used in `Y`.
 - For example, if you create a type `Z` and want to be able to sort it, you have to implement each of the required functions for the sort interface; telling sort what `len`, `less`, and `swap` mean in the context of a `Z`.
 - A type can implement multiple interfaces.

## Blank Identifier in Multiple Assignment
 - Always check error returns; it is bad practice to discard the error value in order to ignore the error.


## Concurrency

> Do not communicate by sharing memory; instead, share memory by communicating.

 - A goroutine is a function executing concurrently with other goroutines in the same address space.
 - Function literals make sure the variables referred to by the function survive as long as they are active.
 - Unbuffered channels give a way to exchange values while guaranteeing that two goroutines are in a known state.
 - Receivers block until there is data to receive. If the channel is unbuffered, the sender blocks until the receiver has received the value.
 - If the channel is buffered, the sender blocks only until the value has been copied to the buffer; if the buffer is full, this means waiting until some receiver has retrieved a value.
 - If the calculation can be broken into separate pieces that can execute independently, it can be parallelized, with a channel to signal when each piece completes.

## Errors

 - The built-in function `panic` creates a run-time error that will stop the program.
 - Real library functions should avoid panic. If the problem can be masked or worked around, it's always better to let things continue to run rather than taking down the whole program.
 - A call to `recover` stops the unwinding and returns the argument passed to panic.
 - `recover` always returns nil unless called directly from a deferred function; deferred code can call library routines that themselves use `panic`, and `recover` without failing.

---
layout: post
title:  Lessons Learned from Effective Go, Part 2
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

---
layout: post
title:  Lessons Learned from Effective Go, Part 1
image:
  feature: pepper_crop.png
tags:   class_notes
date:   2018-08-25 19:07
---

Lately I've been diving into the Golang docs in earnest, trying to get a feel for what it means to write idiomatic Go code. Here are a few of my notes from reading the first half of [Effective Go](https://golang.org/doc/effective_go.html).


## Some Takeaways from Effective Go

From ["Formatting"](https://golang.org/doc/effective_go.html#formatting) through ["Append"](https://golang.org/doc/effective_go.html#append):

 - Because Go programmers are expected to use `go fmt` judiciously, there's not a ton of focus on formatting.
 - In Go, comments > variable/function names when it comes to communication.
 - Short, obvious names are king. The examples in the docs are things like naming a read function `Read` or one that turns things into strings `String`. I think this might be more challenging with functions that more complex or that do less common/recognizable tasks.
 - `switch` is cool; I particularly like the way that each potential outcome is actually called a `case`, which I think will encourage slightly more deliberate control flow usage on my part.
 - I like the idea of using multiple return values for functions to more smoothly anticipate and handle errors. There's something interesting about treating errors as the default for nearly everything.
 - Multiple return values are also useful for differentiating between a `map` lookup that results in nothing found vs. an actual zero value (the "comma ok" idiom).
 - `defer` is a bit new for me, but the [example in the docs}(https://golang.org/doc/effective_go.html#defer) shows it being used a bit like I might use `with open("text.txt") as file: ` in Python so that I don't have to explicitly call `file.close()` after I'm done. Interestingly, deferred functions are executed LIFO.
 - `new` vs. `make`; use `new` for data structures that can be initialized with their zero value (e.g. variables, constants); use `make` for more complex ones that require explicit initializations (e.g. channels, maps, and slices). `new` returns a pointer; `make` does not.
 - In Go, `slices` > `arrays`.
 - `len` and `cap` are legal when applied to a nil `slice`, and return 0.
 - By default, arrays and slices are 1D. For multi-dimensionality, you have to define an array-of-arrays or slice-of-slices.
 - Go was definitely not designed with ML or natural language processing tasks in mind; those are going to be a lot harder, even to emulate some of the functionalities I've grown used to in Python (e.g. allocating 2D slices, nD arrays).
 - Go `maps` ~ Python `dicts` (unordered though, like Python 3 before 3.6)
 - For formatted printing, I love that in Go, `%v` will print anything including arrays, slices, structs, and maps. `%+v` annotates fields with their names;` %#v` prints the value in full Go syntax.
 - `%T` prints the type of the value - handy!
 - `append` in Go is somewhat similar to Python, except you have to pass in whatever you're appending *to* as the first arg.  Use `...` to append a `slice` to a `slice`!

Ok, that's all for now!

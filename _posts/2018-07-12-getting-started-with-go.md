---
layout: post
title:  Getting Started with Go
image:
  feature: pepper_crop.png
tags:   programming
date:   2018-07-12 11:09
---

Over the last year, I've been slowly teaching myself Go. As a Python programmer who previously studied Java and Perl (veeeery briefly), I wanted to know what learning Go would teach me about programming and problem solving in general (à la the [Blub Paradox](http://www.paulgraham.com/avg.html)). However, as I've continued learning Go, I've become increasingly curious about some of the unique features of the language (e.g. automatic memory management and Goroutines), and how they might help me to solve classes of problems I haven't yet encountered. But... before we get to all that, this is just a quick post that goes over some of the basics of getting started with Go, including notes on installation, the go tool, and workspaces.

## Notes on Installing Go (Assuming OSX)

When you download and open the [Go distribution](https://golang.org/dl/), and follow the installation prompts, the package installs the Go distribution to `/usr/local/go` and puts the `/usr/local/go/bin` directory in your PATH environment variable. Check by opening up your bash profile:

```bash
cd ~
open .bash_profile
```

After installation, you should see a new line:

```md
# Golang
export PATH=$PATH:/usr/local/go/bin
```

## The Go Tool

The current distribution of Go comes packaged with the go tool, a command line interface for performing common tasks like running, building, and installing code, and also retrieving public packages and necessary dependencies from distributed version control systems like GitHub.

Some commands include (in the below examples, imagine that `add.go` is an example source file that has `package main` as the first line, and `ballast` is a local Go package, potentially with multiple files):

 - **`go run`**: `go run add.go` runs the code from the hypothetical `add.go` file. It uses a temporary directory to build, execute, and clean up, but does not produce an executable artifact. _Note: this can be useful for development._
 - **`go build`**: assuming our `add.go` file is package `main`, `go build add.go` explicitly compiles the file to produce an executable that can be deployed and run without the go tool. `go build` puts the executable in the current directory.
 - **`go install`**: `go install add.go` also compiles `add.go` and produces an executable, but puts it in  $GOPATH/bin.
 - **`go get`**: `go get github.com/rebeccabilbro/ballast` will clone the `ballast` repo from GitHub user `rebeccabilbro` onto our local machine, placing it inside $GOPATH/src, in a local folder `src/github.com/rebeccabilbro/ballast`. It will also automatically build and install `ballast` into $GOPATH/pkg, storing a package object `ballast.a` in a folder `pkg/darwin_amd64/github.com/rebeccabilbro`. _Note: the `darwin_amd64` part is an automated way of capturing semantically which operating system and processor architecture were used in the local build/install process._
 - **`go fmt`**: `go fmt src/github.com/rebeccabilbro/ballast` automatically reformats code (e.g. spacing, line breaks, etc) in all the files in the hypothetical `ballast` package to conform with current idiomatic practice.
 - **`go help`**: `go help` will list out all the go tool commands, while `go help <command>` will provide more information about that command, as well as any optional flags.

## Code Organization in Go

The next step is to establish your Go "workspace". But... what's a workspace? The idea of a workspace is one of the things that makes the practice of writing Go code a bit different than with other languages. When I'm writing Python code, it can go anywhere.

So maybe I'll have something like:

```bash
~
└─ random_python_script.py
└── Desktop
|    └── another_random_script.py
└── stuff                            
|    └── yellowbrick
|    |    └── yellowbrick
|    |    |    └── __init__.py
|    |    |    └── anscombe.py
|    |    |    └── base.py
|    |    |    └── bestfit.py
|    |    |    └── classifier
|    |    |    |    └── __init__.py
|    |    |    |    └── base.py
|    |    |    |    └── boundaries.py
|    |    |    └── ...
|    |    └── ...
|    └── ...
| ...
```

My `.py` files are all over the place - some in standalone scripts and others in packages with `__init__.py` files, and everything still runs fine!

Go imagines a different approach to code organization, the workspace.

### Your Go Workspace (GOPATH)

A Go workspace is a directory hierarchy to house the Go source code for a project. It will also end up containing the package objects and command binaries that the compiler produces from your source code. Technically, workspaces can live anywhere, and you *could* even have multiple ones, but that's not considered a [best practice](https://golang.org/doc/code.html#Workspaces) in the Go community.

Let's create a workspace called `goplaces` inside my `Projects` directory:

```bash
~$ cd ~
~$ cd Projects
~$ mkdir goplaces                                           # create workspace dir
~$ export GOPATH=/Users/rebeccabilbro/Projects/goplaces     # make Go tool aware of workspace
```

### Where to Put Your Source Code

Now let's create a folder to store the source code (`src`) for my Go projects. By convention, we create a subfolder for the remote version control system we will be using to host the code, which theoretically for me might include both personal projects hosted on GitHub and work projects hosted on Gitlab, e.g.:

```bash
~$ cd goplaces
~$ mkdir src/github.com/rebeccabilbro     
~$ mkdir src/gitlab.com/rbilbro     
```

We create folders with the same names as my Github and Gitlab usernames because when I `go get` packages from other developers that are publicly hosted, the go tool will create subfolders named after _their_ usernames to store those packages in.

### Where Go Puts Things

Remember in the part above where we were talking about `go install`? Assuming the package we're installing is package `main`, `go install` compiles it and produces an executable that it will put in  $GOPATH/bin. So let's create a directory to store those executable commands:

```bash
~$ mkdir bin
```

And also add the GOBIN to our path, which will tell Go explicitly where to put the results of `go install`:

```bash
~$ export GOBIN=/Users/rebeccabilbro/Projects/goplaces/bin      
```

Lastly, we'll create a directory to store package objects

```bash
~$ mkdir pkg   
```

_Note: the workplace subdirectories `pkg` and `bin` will be created automatically by the go tool when they are needed, but it's useful to create them explicitly so that we understand their purposes and have all our paths set correctly._

### An Example Workspace

So here's an example of what a workspace might look like:

```bash
goplaces
└── bin
|   └── ballast              # example executable, result of installing ballast from src
└── pkg                            
|   └── darwin_amd64
|    |   └── github.com
|    |    |   └── bbengfort  # package objects from `go get`-ing bbengfort's source code
|    |    |        └── capillary.a
└── src                              
|    └── github.com
|    |    └── rebeccabilbro
|    |    |    └── axiomatic  # in dev mode (`go run` only, so no `/bin` executables)
|    |    |    |    └── raise.go
|    |    |    |    └── resolve.go
|    |    |   └── ballast    # a finished project, installed via `go install`
|    |    |    |    └── add.go
|    |    |    |    └── add_test.go
|    |    └── bbengfort       # another user's source code retrieved via `go get`
|    |    |    └── capillary
|    |    |    |    └── pump.go
|    |    |    |    └── ...
|    └── gitlab.com
|    |    └── rbilbro
|    |    |    └── dumbledore # project made for work
| ...
```

### What About GOROOT?

It used to be necessary to set a lot of other paths manually in addition to GOPATH. Following changes made to the Go distribution & installation package, we no longer need to set GOROOT.  The correct value is already embedded in the Go tool. More about that [here](https://dave.cheney.net/2013/06/14/you-dont-need-to-set-goroot-really).

Ok, that's all for now!

## Further Reading

 - [Getting Started](https://golang.org/doc/install) (from the official docs)
 - [How to Write Go Code](https://golang.org/doc/code.html) (from the official docs)
 - [Go Start](https://github.com/alco/gostart)
 - Writing, building, installing, and testing Go Code [screencast](https://youtu.be/XCsL89YtqCs)
 - [Organizing Go Code](https://talks.golang.org/2014/organizeio.slide#1)
 - [Organizing Go Code to Support Go Get](https://www.ardanlabs.com/blog/2013/08/organizing-code-to-support-go-get.html)
 - [Setting up a Go Development Environment](https://skife.org/golang/2013/03/24/go_dev_env.html)
 - [Filesystem Structure of a Go Project](https://flaviocopes.com/go-filesystem-structure/)
 - [Go Project Layout](https://medium.com/golang-learn/go-project-layout-e5213cdcfaa2)
 - [go install vs go build](https://pocketgophers.com/go-install-vs-go-build/)
 - [Go Programming](https://youtu.be/CF9S4QZuV30)

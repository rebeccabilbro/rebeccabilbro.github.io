# Getting Started with Go

Over the last year, I've been slowly teaching myself Go. As a Python programmer who previously studied Java and Perl only very briefly, I was mostly interested to know what learning Go would teach me about programming and problem solving in general (à la the [Blub Paradox](http://www.paulgraham.com/avg.html)). However, as I've continued learning Go, I've become increasingly curious about some of the unique features of the language (e.g. automatic memory management and Goroutines), and how they might help me to solve certain kinds of problems I haven't yet encountered. BUT, before we get to that, this is a quick post that goes over some of the basics of getting started with Go, including notes on installation, the go tool, and workspaces.

## Notes on Installing Go (Assuming OSX)

When you download and open the [Go distribution](https://golang.org/dl/), and follow the installation prompts, the package installs the Go distribution to `/usr/local/go` and puts the `/usr/local/go/bin` directory in your PATH environment variable. 

Open up your bash profile:

```bash
cd ~
open .bash_profile
```

You should now see a new line:

```md
# Golang
export PATH=$PATH:/usr/local/go/bin
```

## The Go Tool

The current distribution of Go come packaged with the go tool, a command line interface for performing common tasks like running, building, and installing code, and also retrieving public packages and necessary dependencies from distributed version control systems like GitHub.

Some commands include:

 - `go run add.go`: `go run` runs the code from a hypothetical `add.go` file. It uses a temporary directory to build, execute, and clean up, but does not produce an executable artifact. Useful for development.
 - `go build add.go`: assuming our `add.go` file is package `main`, `go build` explicitly compiles the file to produce an executable that can be deployed and run without the go tool. `go build` puts the executable in the current directory.
 - `go install add.go`: `go install` also compiles `add.go` and produces an executable, but puts it in  $GOPATH/bin.
 - `go get github.com/rebeccabilbro/ballast`: here `go get` will clone the `ballast` repo from GitHub user `rebeccabilbro` onto our local machine, placing it inside $GOPATH/src, in a local folder `src/github.com/rebeccabilbro/ballast`. It will also automatically build and install `ballast` into $GOPATH/pkg, storing a package object `ballast.a` in a folder `pkg/darwin_amd64/github.com/rebeccabilbro`. _Note: the `darwin_amd64` part is an automated way of capturing semantically which operating system and processor architecture were used in the local build/install process._
 - `go fmt src/github.com/rebeccabilbro/ballast`: `go fmt` automatically reformats code (e.g. spacing, line breaks, etc) in all the files in the hypothetical `ballast` package to conform with current idiomatic practice.
 - `go help`: `go help` will list out all the go tool commands, while `go help <command>` will provide more information about that command, as well as any optional flags.

### But What About GOROOT?

Following changes made to the Go distribution & installation package, we no longer need to set $GOROOT.  The correct value is already embedded in the Go tool. More about that [here](https://dave.cheney.net/2013/06/14/you-dont-need-to-set-goroot-really).

## Your Go Workspace (GOPATH)

You *do* however have to set your GOPATH, aka your Go "workspace". A workspace is a directory hierarchy to house the Go source code for a project. It will also end up containing the package objects and command binaries that the compiler produces from your source code. Workspaces can live anywhere.

Here's an example, where we create a workspace called `goplaces` inside our `Projects` directory:

```bash
~$ cd ~
~$ cd Projects
~$ mkdir goplaces                                                                      # create workspace dir
~$ export GOPATH=/Users/rebeccabilbro/Projects/goplaces       # make Go tool aware of workspace
```
 
Now let's create a folder to store the source code (`src`) for my Go projects. By convention, we place this 

```bash
~$ mkdir src/github.com/rebeccabilbro     
```



Create a directory to store executable commands: 

```bash
~$ mkdir bin 
```

Tell Go where to put the results of `go install`

```bash
~$ export GOBIN=/Users/rebeccabilbro/Projects/goplaces/bin      
```


Create a directory to store public packages to be used internally by your projects
```bash
~$ mkdir pkg   
```


text

----
goplaces
└── bin
 |   └── ballast                    # example executable, resulting from having installed the local ballast package
└── pkg                            
 |   └── 
└── src                              
 |   └── github.com
 |    |   └── rebeccabilbro
 |    |    |   └── axiomatic     # a sample project, still in development, thus no corresponding `/bin` executables
 |    |    |    |   └── raise.go
 |    |    |    |   └── resolve.go
 |    |    |   └── ballast          # a finished project, which has been installed via `go install`
 |    |    |    |   └── add.go
 |    |    |    |   └── add_test.go
 |    |    |    |   └── remove.go
 |    |    |    |   └── remove_test.go
 |    |    |   └── capillary
 |     |    |    |   └── ...
----

text
----
gocode
└── rebeccabilbro
|   └── bin
|    |   └──hello
|    |   └── rocketlauncher
|   └── pkg
|   └── src
|        └── hello
|            └── hello.go
└── primetime
    └── bin
    |   └── rocketlauncher
    └── pkg
    └── src
        └── rocketlauncher
            └── rocketlauncher.go
----

## Package Layout


## Further Reading

 - [Go Start](https://github.com/alco/gostart)
 - Writing, building, installing, and testing Go Code [screencast](https://youtu.be/XCsL89YtqCs)
 - [Organizing Go Code to Support Go Get](https://www.ardanlabs.com/blog/2013/08/organizing-code-to-support-go-get.html)
 - [go install vs go build](https://pocketgophers.com/go-install-vs-go-build/)
 - [Go Programming](https://youtu.be/CF9S4QZuV30)

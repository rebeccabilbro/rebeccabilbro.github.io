# Getting Started with Go

## Notes on Installing Go (Assuming OSX)

When you download and open the [Go package file](https://golang.org/dl/), and follow the installation prompts, the package installs the Go distribution to `/usr/local/go` and puts the `/usr/local/go/bin` directory in your PATH environment variable. So if you:

```bash
cd ~
open .bash_profile
```

You should now see a new line:

```md
# Golang
export PATH=$PATH:/usr/local/go/bin
```

## But What About GOROOT?

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
 
Now let's create a folder to store the source code (`src`) for my Go projects:

```bash
~$ mkdir src/github.com/rebeccabilbro     
```

By convention, 

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

 - Writing, building, installing, and testing Go Code [screencast](https://youtu.be/XCsL89YtqCs)
 - [Organizing Go Code to Support Go Get](https://www.ardanlabs.com/blog/2013/08/organizing-code-to-support-go-get.html)
 - [Go Programming](https://youtu.be/CF9S4QZuV30)

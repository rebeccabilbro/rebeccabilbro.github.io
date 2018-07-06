# Getting Started with Go

## GOROOT

## Go Workspace (GOPATH)

A workspace is a directory hierarchy to house the Go source code for a project. It will also end up containing the package objects and command binaries that the compiler produces from your source code. Workspaces can live anywhere.

```bash
~$ mkdir gocode                     # create workspace dir
~$ export GOPATH=$HOME/gocode       # make Go tool aware of workspace
```

Here's how I have my workspace set up to distinguish local projects (where I'm just messing around) from public-facing projects that might get associated with my GitHub profile.

----
gocode
└── goofing
|   └── bin
|   |   └──hello
|   └── pkg
|   └── src
|       └──hello
|           └──hello.go
└── primetime
    └── bin
    |   └──rocketlauncher
    └── pkg
    └── src
        └──rocketlauncher
            └──rocketlauncher.go
----

## Package Layout


## Further Reading

 - Writing, building, installing, and testing Go Code [screencast](https://youtu.be/XCsL89YtqCs)
 - [Organizing Go Code to Support Go Get](https://www.ardanlabs.com/blog/2013/08/organizing-code-to-support-go-get.html)
 - [Go Programming](https://youtu.be/CF9S4QZuV30)

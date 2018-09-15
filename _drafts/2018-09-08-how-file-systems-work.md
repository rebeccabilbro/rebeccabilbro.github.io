---
layout: post
title:  File System Methods
date:   2018-09-08 09:21
---


When we run our program, we'll use bazil's [`Serve()` method](https://github.com/bazil/fuse/blob/master/fs/serve.go#L390) to instantiate our in-memory filesystem. `Serve()` takes as arguments a connection and a filesystem struct:

```
err = fs.Serve(conn, Dfs{})
```

To successfully implement the filesystem interface, `Dfs` needs a `Root` method. On instantiation, `Dfs` will use `Root()` to obtain the inode for the file system's root:

```
type Dfs struct {
  Root() (Node, error)
}
```

## Root

The root of the file system is the top-most directory in the hierarchy. It is the starting point from which all other directories and files originate.


```
// Root, for a given filesystem `f` retrieves and returns the `root`
// attribute of `f` which is an inode. If `f` has no `root` attribute,
// the function returns an error
func (f *Dfs) Root() (n fs.Node, err error){
    ...
}
```

## Inodes  

What attributes can an inode have? As conceived in our in-memory filesystem, an inode is a generic struct, `DNode`, which can be either a file or a directory. It has the following properties:

```
type DNode struct {
	nid   uint64  // unique identifier of the inode
	name  string  // name of the inode
	attr  fuse.Attr  // attributes from fuse.Attr struct
	dirty bool  // whether or not the inode has been changed
	kids  map[string]*DNode  // map to any children
	data  []uint8 // other data associated with the inode
}
```

But what gives an inode its attributes?

## Attr

We need a way to prepopulate inodes with some basic information, such as a unique identifier, a size, and [permissions code](https://en.wikipedia.org/wiki/File_system_permissions#Numeric_notation) (e.g. read-only, read/write, etc). We do this with the `Attr` method. For instance, in the ["hello word" filesystem example](https://github.com/bazil/fuse/blob/master/examples/hellofs/hello.go#L66-L70), `Attr` (defined as a function that can be performed on a directory), takes as arguments a [context](https://godoc.org/golang.org/x/net/context) and a pointer to a [`fuse.Attr` struct](https://github.com/bazil/fuse/blob/master/fuse.go#L1316-L1333), sets the directory's unique identifier to 1 and it's permissions mode to read/execute, and simply returns.

```
func (Dir) Attr(ctx context.Context, a *fuse.Attr) error {
	a.Inode = 1
	a.Mode = os.ModeDir | 0555
	return nil
}
```

In the context of our in-memory filesystem though, we want `Attr` to be able to set the attributes for any type of inode, whether it's a file or a directory, so we'll define it as a method on a pointer to a `DNode`:


```
// Attr, for a pointer to a inode `n`, fills out the standard
// metadata for `n`.
func (n *DNode) Attr(ctx context.Context, attr *fuse.Attr) error {
    ...
}
```

## Lookup

How are we going to find files and directories in our file system? We'd like a method that would take as input a name (string) and see if it matches any of the files or directories in our filesystem. We can define `Lookup` as a method that can be performed on a pointer to a `DNode` `n`, and takes as arguments a context and a string to search for. We could check first to see if `n` has a `name` attribute that matches the string, and if so return `n`. Otherwise, we can check if `n` has any `kids`, and if so, we can iterate through the children of `n` to see if the `name` attribute of any kid `k` matches the string, and if so return `k`. If we don't find any matches, we should return an `ENOENT` error, which stands for "error-no-entry":


```
// Lookup looks up a specific entry (a DNode), and should return an inode
// corresponding to the entry. If name does not exist, Lookup should return
// ENOENT (error-no-entry) error.
func (n *DNode) Lookup(ctx context.Context, name string) (fs.Node, error) {
    ...
}
```

## ReadDirAll

What if I'm not sure what I'm looking for, and just want to see everything contained within a particular directory? If that node has children (`n.kids` according to the convention in our in-memory file system), we should traverse through all the children, retrieving their ids, filetypes, and names, and returning them as a slice:


```
// ReadDirAll returns a slice of directory entries, including all files
// and directories that are children of a given DNode.
func (n *DNode) ReadDirAll(ctx context.Context) ([]fuse.Dirent, error)
```

## Getattr

Suppose we've identified the file or directory of interest, and now we want to retrieve its metadata. `Getattr` is a function defined for a `DNode` that takes as arguments a context, a pointer to a [`fuse.GetattrRequest`](https://github.com/bazil/fuse/blob/master/fuse.go#L1392-L1396) and a pointer to a [`fuse.GetattrResponse`](https://github.com/bazil/fuse/blob/master/fuse.go#L1416-L1418). It won't actually return anything (except an error, should anything go wrong), but it will take the pointer to the FUSE response and populate it with all of the attributes of the specified DNode:

```
// Getattr populates the fuse response with the attributes of the DNode
func (n *DNode) Getattr(ctx context.Context, req *fuse.GetattrRequest, resp *fuse.GetattrResponse) error

```

## Setattr

Several Unix commands actually change the attributes of a node, meaning that under they hood they make calls to `Setattr`

```
func (n *DNode) Setattr(ctx context.Context, req *fuse.SetattrRequest, resp *fuse.SetattrResponse) error
```

## Fsync

```
func (n *DNode) Fsync(ctx context.Context, req *fuse.FsyncRequest) error
```

## Mkdir

```
func (p *DNode) Mkdir(ctx context.Context, req *fuse.MkdirRequest) (fs.Node, error)
```

## Create

```
func (p *DNode) Create(ctx context.Context, req *fuse.CreateRequest, resp *fuse.CreateResponse)
     (fs.Node, fs.Handle, error)
```

## ReadAll

```
func (n *DNode) ReadAll(ctx context.Context) ([]byte, error)
```

## Write

```
func (n *DNode) Write(ctx context.Context, req *fuse.WriteRequest, resp *fuse.WriteResponse) error
```

## Flush

```
func (n *DNode) Flush(ctx context.Context, req *fuse.FlushRequest) error
```

## Remove

```
func (n *DNode) Remove(ctx context.Context, req *fuse.RemoveRequest) error
```

## Rename

```
func (n *DNode) Rename(ctx context.Context, req *fuse.RenameRequest, newDir fs.Node) error
```

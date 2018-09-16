---
layout: post
title:  What is a Filesystem?
image:
  feature: pepper_crop.png
tags:   programming
date:   2018-09-03 17:45
---

What is a filesystem? In this post we'll explore userspace filesystems, discuss their components, get to know the FUSE kernel module, and learn about `bazil`, a Go library that implements a userspace server for the Linux and OS X kernel protocols.


## What is a Filesystem?

A [filesystem](https://en.wikipedia.org/wiki/File_system) is a set of abstract data types implemented for storing and interacting with data. As it relates to this post, a filesystem is a kernel module used to access files and directories.

A filesystem provides access to data for applications and system programs via consistent, standard interfaces exported by the virtual file system (VFS), and enables access to data that may be stored persistently on local media or on remote network servers/devices, or even transient data (such as debug data or kernel status) stored temporarily in RAM or special devices.


### Definitions (expanded from [here](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/filesystems/fuse.txt) and [here](https://download.samba.org/pub/samba/cifs-cvs/ols2006-fs-tutorial-smf.pdf))

 - *Kernel:* The core program of a computer's operating system, which handles its memory.
 - *Userspace filesystem:* A filesystem in which data and metadata are provided by an ordinary userspace process. The filesystem can be accessed normally through the kernel interface.
 - *Filesystem daemon:* The process(es) that provide the data and metadata of the filesystem.
 - *Mounting:* The process by which the operating system makes files and directories on a storage device accessible to users via a file system.
 - A *mount point* is the location of a registered virtual file system on a storage device.
 - *User mount:* A userspace filesystem mounted by a non-privileged (non-root) user. The filesystem daemon is running with the privileges of the mounting.
 - *Filesystem connection:* A connection between the filesystem daemon and the kernel. The connection exists until either the daemon dies, or the filesystem is unmounted.
 - *Detaching* (or *lazy unmounting*) the filesystem does _not_ break the connection; it will exist until the last reference to the filesystem is released.
 - *Mount owner:* The user who does the mounting.
 - *User:* The user who is performing filesystem operations.

## What is FUSE?

A single computer's kernel can (and often does) have many different local filesystems. Common ones include Ramfs, Sysfs,Proc, Ext3, NTFS, JFS, XFS, and FUSE.

FUSE is a special purpose userspace filesystem framework. It consists of a kernel module, a userspace library, and a mount utility. We can think of FUSE as an API for the Linux kernel.

FUSE allows secure, non-privileged mounts, which means that as a user, I can create and access files without having to be a root-user.

If you have a Mac like me, you can install FUSE for OSX via `brew cask install osxfuse`.


## What is `bazil`?
`bazil.org/fuse` is a Go library for writing filesystems. It is a from-scratch implementation of the FUSE kernel-userspace communication protocol. Bazil mirrors kernel data structures (trees), with `uint64` handles to `inode` objects.


### What is an inode?

An `inode` is a representation of a file and its metadata
(timestamps, type, size, attributes) but not its name. Inodes can represent files, directories (containers of files),
symlinks and special files. Sample operations that we want to perform on inodes include `create`, `mkdir`, `unlink` (delete), `rmdir`, and `mknod`.

In the below snippet, `File` is a struct and has associated with it an `Attr` method, which returns a `fuse.Attr` set to `read` mode (which is `0444` in [numeric notation](https://en.wikipedia.org/wiki/File_system_permissions#Numeric_notation)):

```
type File struct{}

func (File) Attr() fuse.Attr {
    return fuse.Attr{Mode: 0444}
}
```

A `Node` must implement `Attr()` (e.g. must implement methods like `Remove()` and `unlink(2) on`). Other methods are optional.

The following `ReadAll` method takes as an argument an interrupt request (`fuse.Intr`) and returns a string of bytes (containing "hello, world") and a nil error:

```
func (File) ReadAll(intr fuse.Intr) ([]byte, fuse.Error) {
    return []byte("hello, world\n"), nil
}
```

`ReadAll()` caches the whole content in memory and serves smaller reads from that. There's also `Read() `for more realistic use.

Here we create a directory `struct`, `Dir`, and an associated function that returns a `fuse.Attr` containing an inode id and a mode specifying that the inode is a directory, and that it has read/execute permissions:

```
type Dir struct{}

func (Dir) Attr() fuse.Attr {
    return fuse.Attr{Inode: 1, Mode: os.ModeDir | 0555}
}
```

Now we'll add a `Lookup` function that takes as arguments a string that represents the name associated with an inode and an interrupt request, and returns either the matching inode and a nil error, or if the inode is not found, a nil in place of an inode, and a error-no-entry message.

```
func (Dir) Lookup(name string, intr fuse.Intr) (fuse.Node, fuse.Error) {
    if name == "hello" {
        return File{}, nil
    }
    return nil, fuse.ENOENT
}
```

We now create our entry point into the filesystem with an `FS` `struct` and an associated function that returns a directory inode and nil error:

```
type FS struct{}

func (FS) Root() (fuse.Node, fuse.Error) {
    return Dir{}, nil
}
```

How will we list out the files contained in the filesystem? Let's create a single directory entry (`fuse.Dirent`) variable called `dirDirs`, with an inode id, a name, and a type corresponding to a file entry in a directory listing (`fuse.DT_File`). We then write a function, `ReadDir`, that accepts an interrupt request and returns this single directory entry:

```
var dirDirs = []fuse.Dirent{
    {Inode: 2, Name: "hello", Type: fuse.DT_File},
}

func (Dir) ReadDir(intr fuse.Intr) ([]fuse.Dirent, fuse.Error) {
    return dirDirs, nil
}
```

*Note: If you don't fill in inode numbers in your Attr() etc calls, Bazil will hash the full path to create a pseudorandom inode number. If you care, manage inode numbers explicitly.*


#### Directory Lookup in `bazil`
Kernel `struct dentry` maps to `fuse.Node`, identified on wire with `fuse.NodeID`. `Lookup()` returns a `Node`, and a reference is kept in a `map[NodeID]Node` until a `Forget()` call is made.

#### Opening and Closing Files
Kernel `struct file` maps to `fuse.Handle`, identified on wire with `fuse.HandleID`. `Open()` returns a `Handle` (maybe `self`), which is kept in a `map[HandleID]Handle` until a `Destroy()` call is made.

`close(2)` has two parts:` Release()` which returns an error (for delayed writes and such), and a final `Destroy()` that always succeeds.

### FUSE Kernel Protocol
With `bazil`, requests are served by methods on the inode itself, not a global dispatch function.

 - *RequestID:* to match response to request; lifetime ends with response.
 - *NodeID:* directory entry kernels; knows about kernel; tells when to forget.
 - *HandleID:* open file kernel; tells when to destroy.


## More FUSE Details

### FUSE Mount Options

`fd=N`
 The file descriptor to use for communication between the userspace filesystem and the kernel. The file descriptor must have been obtained by opening the FUSE device (`/dev/fuse`).

`rootmode=M`
 The file mode of the filesystem's root in octal representation.

`user_id=N`
 The numeric user id of the mount owner.

`group_id=N`
 The numeric group id of the mount owner.

`default_permissions`
 By default FUSE doesn't check file access permissions, the filesystem is free to implement its access policy or leave it to the underlying file access mechanism (e.g. in case of network filesystems). This option enables permission checking, restricting access based on file mode.  It is usually useful together with the `allow_other` mount option.

`allow_other`
 This option overrides the security measure restricting file access to the user mounting the filesystem.  This option is by default only allowed to root, but this restriction can be removed with a (userspace) configuration option.

`max_read=N`
 With this option the maximum size of read operations can be set. The default is infinite. Note that the size of read requests is limited to 32 pages (which is 128kbyte on i386).

`blksize=N`
Set the block size for the filesystem.  The default is 512.  This option is only valid for `fuseblk` type mounts.


### Control Filesystem

Under the FUSE control filesystem, each connection has a directory named by a unique number. For each connection the following files exist within this directory:

`waiting`
 The number of requests which are waiting to be transferred to userspace or being processed by the filesystem daemon. If there is no filesystem activity and 'waiting' is non-zero, then the filesystem is hung or deadlocked.

`abort`
 Writing anything into this file will abort the filesystem connection. This means that all waiting requests will be aborted and an error returned for all aborted and new requests.


### Interrupting filesystem operations

If a process issuing a FUSE filesystem request is interrupted, the following will happen:

 1) If the request is not yet sent to userspace AND the signal is fatal (SIGKILL or unhandled fatal signal), then the request is dequeued and returns immediately.

 2) If the request is not yet sent to userspace AND the signal is not fatal, then an 'interrupted' flag is set for the request. When the request has been successfully transferred to userspace and this flag is set, an INTERRUPT request is queued.

 3) If the request is already sent to userspace, then an INTERRUPT request is queued. INTERRUPT requests take precedence over other requests, so the userspace filesystem will receive queued INTERRUPTs before any others.


### Aborting a filesystem connection

It is possible to get into certain situations where the filesystem is not responding.  Reasons for this may be:

 1) Broken userspace filesystem implementation
 2) Network connection down
 3) Accidental deadlock
 4) Malicious deadlock

In these cases it may be useful to abort the connection to
the filesystem. There are several ways to do this:
 - Kill the filesystem daemon.  Works in case of a) and b)
 - Kill the filesystem daemon and all users of the filesystem. Works in all cases except some malicious deadlocks
 - Use forced umount (umount -f).  Works in all cases but only if filesystem is still attached (it hasn't been lazy unmounted)
 - Abort filesystem through the FUSE control filesystem.  Most powerful method, always works.


## Resources

 - [Bazil](https://bazil.org/fuse/)
 - [FUSE documentation](https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/tree/Documentation/filesystems/fuse.txt)
 - [How to build a filesystem](https://bazil.org/talks/2013-06-10-la-gophers)
 - [Linux Filesystems in 45 minutes](https://download.samba.org/pub/samba/cifs-cvs/ols2006-fs-tutorial-smf.pdf)
 - [Go implementation of an in-memory file system](https://github.com/bazil/fuse/blob/master/examples/hellofs/hello.go)
 - [Python implementation of an in-memory file system](https://github.com/libfuse/python-fuse/blob/master/example/hello.py)

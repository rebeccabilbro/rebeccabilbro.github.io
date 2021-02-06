---
layout: post
title:  Embedded Binaries for Go
image:
  feature: pepper_crop.png
tags:   programming
date:   2021-2-06 14:09
---

Recently a friend asked about Go packages for embedding binary data into code...
As it turns out, there are a lot of options!

## go-bindata

### [go-bindata/go-bindata](https://github.com/go-bindata/go-bindata)
This package converts any file into Go source code, including for embedding binary data into a Go program. The file data is optionally gzip compressed before being converted to a raw byte slice. It comes with a command line tool in the `go-bindata` sub directory. The converted file(s) is/are embedded in a new Go source file, along with a table of contents and an `Asset` function, which allows quick access to the asset, based on its name.

### [kevinburke/go-bindata](https://github.com/kevinburke/go-bindata)
As of the time of this writing, the most recently updated fork of the original `go-bindata/go-bindata`. This fork is also apparently the version trusted by Homebrew. Changes from the original package include:
- Atomic writes; generated file cannot be read while partially complete.
- Better encoding of files that contain characters in the Unicode format range.
- Generated file reports file sizes.
- Generated code is run through go fmt.
- SHA256 hashes are computed for all files and stored in the binary. You can use this to detect in-memory corruption and to provide easy cache-busting mechanisms.
- Added `AssetString` and `MustAssetString` functions.
- `ByName` is not public.
- Some errors in file writes were unchecked, but are now checked.
- File modes are stored in octal (0644) instead of nonsensical decimal (420)

## [pkger](https://github.com/markbates/pkger)
`pkger` is a tool for embedding static files into Go binaries and was intended as a replacement for [gobuffalo/packr](https://github.com/gobuffalo/packr). Use the `pkger` command to package files and the `parser` tool to access them after packaging. The API is modeled on the `os` package in the Go standard lib.

## [esc](https://github.com/mjibson/esc/)
`esc` embeds files into Go programs and provides `http.FileSystem` interfaces to them. It adds all named files or files recursively under named directories at the path specified. The output file provides an `http.FileSystem` interface with zero dependencies on packages outside the Go standard lib. After producing an output file, the assets may be accessed with the `FS()` function. `esc` appears to have had a very loyal following but has not been updated for over a year.


## Conclusion (for now)
At the time of this writing the original `go-bindata` and `pckgr` libraries have the most stars on Github, though given that it is the trust choice of Homebrew, I'd recommend using the [kevinburke/go-bindata](https://github.com/kevinburke/go-bindata) package.


## References

- [Embedding files in binaries](http://blog.itaysk.com/2020/04/30/embedding-files-in-binaries), Itay Shakury
- [How to embed files into Go binaries](https://stackoverflow.com/questions/17796043/how-to-embed-files-into-go-binaries), Stackoverflow
- [The easiest way to embed static files into a binary file in your Golang app (no external dependencies)](https://dev.to/koddr/the-easiest-way-to-embed-static-files-into-a-binary-file-in-your-golang-app-no-external-dependencies-43pc), Vic Shostak

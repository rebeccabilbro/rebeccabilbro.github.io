---
layout: post
title:  The Elephant file system
image:
  feature: pepper_crop.png
tags:   class_readings
date:   2018-09-09 15:02
---


I was recently reading [Creativity, Inc](https://www.amazon.com/Creativity-Inc-Overcoming-Unseen-Inspiration/dp/0812993012) by Ed Catmull and Amy Wallace, which is about the genesis of Pixar, a company that was made by a single movie (Toy Story). What most people don't know is that the company was very nearly unmade when, a year into the production of Toy Story 2, the entire movie was accidentally deleted from the file system where it was stored. Tldr; everything turns out ok, but it got me thinking -- how do our file systems protect us from ourselves? In "Deciding when to forget in the Elephant file system," Douglas Santry, et al described their development and experimentation with a new kind of filesystem that, by default, refuses to forget.

## Considering User Behavior

The primary thing that struck me about Santry et al's filesystem implementation is that it is entirely designed around how file systems get used in practice -- people manually save multiple versions of files; and as time passes, they struggle to differentiate between those multiple versions; they rarely perform manual clean-up maintenance of old data; they delete things by accident; they edit in short bursts and then stop; and for better or worse, they use exactly as much control as they are allowed by their file system and operating system.

## Complexity

Santry's solution for how to protect users from themselves in the Elephant file system is to "separate storage management from the common file system operations available to users." The actual implementation of this ends up being rather complex, requiring not only `inodes` (used for new files with no history, or old files that have ceased to change), but also `inode logs` (maintain pointers to multiple versions of a file), and `imaps` (store extended metadata for a file, including an `inode` or `inode log`, details about how the file should be versioned over time, and it's change velocity, or `temperature`).

## Performance

In addition to being conceptually rather complex, the storing of multiple versions results in performance slow-downs for opening old versions and writing new versions files (though not as much as one might expect); moreover, as the authors admit, "it reduces the effectiveness of buffer-cache write absorption and thus increases the number of disk writes." This made me wonder about potential optimizations inspired by the [log-structured file system paper](https://rebeccabilbro.github.io/log-structured-filesystem/), i.e. using an in-memory log segment to capture multiple changes that could be later written in a single sequential write. Alternatively, I wondered if it might be possible to use some version of the block-comparison strategy discussed in the [low-bandwidth networked file system paper](https://rebeccabilbro.github.io/network-filesystem/), which compared versions of files in terms of variable length chunks, writing only chunks that had changed between versions. This is something the authors later seem to suggest when they discuss the potential for implementing a branch-merge strategy for Elephant.

## Takeaways

It seems the main downside of the Elephant system is that its naming convention for versions combines the file's name with a timestamp, which makes a fundamental "assumption [that] the multiple versions of a file never co-exist"; however, in a networked context where many people are interacting with a filesystem simultaneously, it becomes increasingly likely that their interactions will be disconnected, and that the resulting history, when merged, "may have intervals in which multiple versions co-existed."

One strength of this paper worth noting is the extent to which the authors go to document the Elephant interface, including an extensive list of system calls, methods, and parameters, which future researchers could use as references for future work. Looking at you Bazil...

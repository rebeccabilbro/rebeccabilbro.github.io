---
layout: post
title:  The Old Block and Chain
image:
  feature: pepper_crop.png
date:   2018-11-27 17:40
tags:   class_readings
---


I have to admit that as an applications developer who is living through the age of the blockchain mania, having to explain on a routine basis [why blockchain is not relevant
to a problem](https://twitter.com/arnabdotorg/status/1049116699927171077?lang=en), I was not properly enthused about reading the [Ethereum paper](https://github.com/ethereum/wiki/wiki/White-Paper) for class this week. Having now read through it, I remain unconvinced about the current frenzy to eschew RDBMS and nice, simple NoSQL solutions for trendy blockchain implementations. However, I can certainly see the appeal, both from a decentralized consensus perspective, and from a (probably FinTech) applications developer perspective.

## Ethereum

One thing we have observed over and over in the distributed systems papers we've read for [class](http://triffid.cs.umd.edu/818/) is that transactions are usually an afterthought. "Should we implement transactions?" ask many of the authors, meaning I assume, "will they be worth the effort it will take us to implement them?" From an academic novelty perspective, transactions apparently don't seem very compelling, and they take a lot of work. For this reason, one thing that stands out about the Ethereum paper (aside from it's stated goal of exposing an API for doing distributed consensus with blockchain) is the support for robust transactions as a first-class feature, inside an API that allows developers to write their own "contracts" to decide how objects should react to messages about those transactions.

Bitcoin (which is what inspired Ethereum) is reminiscent of several of the distributed consensus papers, including [SUNDR and SPORC](https://rebeccabilbro.github.io/trust-and-consistency/); as Ray explains, "if we had access to a trustworthy centralized service, this system would be trivial to implement." But we don't, so as with SUNDR and SPORC, Bitcoin leverages public and private keys to index coins by their owners, and to sign transactions. How do we reach consensus about the ledger? We weight the votes of a given participant with respect to the compute power they contribute to the system. Miners process transactions by taking part in the consensus protocol and trying to form blocks of transactions, and in exchange they profit off the transaction fees. Blocks are essentially Merkle trees, which allow piecemeal access to transactions.

One of the unique parts of Bitcoin is the need to artificially handicap the rate of growth of the ledger by making it computationally slow to form blocks. This handicap (aka 'proof of work') keeps gaming of the system in check.

Speaking of gaming the system, Bitcoin is subject to forking attacks just as in SUNDR/SPORC. The solution is to tell miners to work on the longest chains, with the assumption that length is a proxy for validity. This ends up being a pretty safe proxy, since "in order for the attacker to make his blockchain the longest, he would need to have more computational power than the rest of the network combined in order to catch up".

So, what if I'm an applications developer looking to build my transactions on top of this kind of technology, what are my options? Well, I can (1) make my own blockchain, but this will be hard, and might not be worth it given the economy of scale. Or I can (2) build on vanilla bitcoin, but then I have to rely on length of chains as a proxy for validity, which might not work for my use case. Finally, I can (3) try to write a bunch of complicated heuristics on top of the unspent transaction output (`UTXO`) primitive to get the kinds of validations I need, but this is pretty limited and also kind of risky.

What if instead there was a nice generic open source blockchain API? There is; it's Ethereum! Ethereum give us access to the transactional interface of Bitcoin, but in a more flexible way, exposing an "account" object with attributes like balance, "nonce" (Lamport clock), and "contract codes" (database interaction layer methods). Ethereum is definitely more flexible that Bitcoin, and more accessible that Blockchain, but whether it has the kind of broad application outside of FinTech-type applications is, I think, still debatable.

## Stellar

The Stellar consensus protocol is a fascinating amalgamation of prior ideas from the distributed consensus and peer-to-peer network literature. Most of the consensus algorithms we've read about assume a closed, trusted membership system. Practical Byzantine Fault Tolerance has closed membership, but doesn't assume that all participants are trustworthy. Bitcoin's membership system is more flexible, awarding membership based on compute power (or sometimes an ante), which uses incentives (transaction fees) and limits (proof of work) to try to keep bad behavior in check. By contrast, Stellar offers an open membership system that can scale flexibly and offer trust as a configurable feature. Moreover, while most of the previous systems have to grapple with the tradeoff between performance (e.g. latency) and decentralization, Stellar manages to wrangle both.

I find the idea of per-application quorum selection to be exciting and a little scary! On the one hand, I can decide which servers to trust, and they will be my quorum. You can decide to trust a different slice of the quorum. On the other hand, putting that much power into the hands of the apps developers, who may have little insight into the system as a whole, and thus little context for deciding which slices are generally agreed to be trustworthy, seems a bit dangerous to me!
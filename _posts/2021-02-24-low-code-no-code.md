---
layout: post
title:  Why don't developers give much cred to low-code/no-code tools?
image:
  feature: pepper_crop.png
date:   2021-2-24 08:18:36
tags:   development
---

Recently a good friend asked me why it is that developers don't give much credence to low-code and no-code tools. It's an interesting question! One problem is that "low code" is a relative term &mdash; technically something like D3 is a low-code solution for building interactive data viz. Bootstrap is a low-code tool for making webpages. Keras is a low-code way for me to template out my Tensorflow models. And, if Kubernetes is mostly just yaml, does that mean it's "no code"? Nevertheless, the words "low code" and "no code" *do* make me cringe. In this post, I try to tease out exactly why.


## Make it, but with your hands tied behind your back

One of the reasons that developers don't like low-code/no-code (I'm going to abbreviate as LCNC from here on out) is because they make us feel like we are building with our hands tied behind our backs. As a coder, I have my own highly personalized ways of breaking problems down into pieces, building components against each of those problems, and then orchestrating those components together into a solution. It might not be for everyone, but it's my process. With LCNC, I have to use someone else's process, and it makes me feel awkward and constrained. I can't use the shortcuts and mental gynastics I'm used to and instead have to belly flop through someone else's jungle gym.

In [The No Code Delusion](https://www.alexhudson.com/2020/01/13/the-no-code-delusion/), Alex Hudson writes:

> At the heart of the issue is the concept that “computer programming” - which is to say, writing code - is a constraint on the development of software. That there is some “higher level” on which people can operate, where development is much simpler but the end results in some way the same.

Hudson's post speaks to me because while I do feel like I have my own "higher level" &mdash; my own cerebral operating system *per se* &mdash; I don't imagine that `rebeccaOS` would make sense or in any way accelerate the problem-solving processes of another developer.

## You're so basic

It's ironic that the word "basic" has become a dig meaning that someone is kind of dull. When asked about LCNC, many programmers may instinctively think about Visual Basic, one of the first tools that aimed to directly expose this "higher level" in order to facilitate the process of building software.

In [The Rise and Fall of Visual Basic](https://developers.slashdot.org/story/19/06/22/2138248/the-rise-and-fall-of-visual-basic), Matthew MacDonald writes of how VB changed how people thought about programming when it was released in the early 1990's:
> Here was something entirely new. You could create buttons for your programs by drawing them on the surface of a window, like it was some kind of art canvas. To make a button do something, all you had to do was double-click it in the design environment and write some code.

VB made a lot of things easier, but it wasn't perfect. Bruce McKinney, author of [Hardcore Visual Basic](https://www.worldcat.org/title/hardcore-visual-basic/oclc/36841494) is famously credited with saying "Visual Basic makes 95% of your task easy and the other 5% impossible".

The issue isn't specific to Visual Basic. With LCNC, progress becomes untenable as soon as you need to do something the framework hasn't anticipated that you'll want to do:

Alexander Ilg [writes](https://medium.com/alexander-ilg/):
> With low-code, you are a prisoner of the framework or tool you use.

Devetry [writes](https://devetry.com/blog/why-hasnt-low-code-revolutionized-app-development-yet/):
> [The easy...] functionality comes at a price, which is namely an absence of customization.

Whether that absence of customization means that you have to miss out on certain features you wanted, or it just means that your app looks just as basic as everyone else's &mdash; there's a clear opportunity cost involved in choosing LCNC.

## Black boxes with bad things inside

I've seen a lot of developers describe LCNC with metaphors like the "roadbike vs mountain bike" or "frozen dinner vs homemade meal" or "manual vs automatic transmission". These metaphors get at some of the issues the community has with LCNC &mdash; over-optimization, over-genericization, over-commoditization.

But these metaphors don't capture the full picture. Sometimes LCNC actually produces *worse* results. In [Why Low Code Development Is Not As Great As We Think](https://opensenselabs.com/blog/tech/low-code-development-not-great), Tuba Ayyubi writes:
> [Low code] puts user experience at stake. A design-led approach or a progressive approach becomes harder to achieve with low code. Functionality over the need of the user never ends well.

Moreover, she says:
> Using low code to produce code that does not adhere to established best practices could violate an organization’s compliance measures.

One of the areas that is quite close to my own work, and where LCNC can be really dangerous is in AI/ML. When I started out building ML models at work, there was a definite the-robots-are-coming-to-steal-our-jobs backlash. My assurance to my colleagues and clients was that very few ML use cases are improved by completely removing thoughtful humans from the loop. Unfortunately, LCNC ML seems increasingly enthusiastic to try anyway.

There are already a shocking number of data scientists who are not incentivized to unpack the choices implicit in their ML pipelines. Does our imputation or normalization strategy make sense for this data? Have we applied cross validation in a way that protects us from data leakage? Might multicollinearity or heteroskedasticity be unexpectedly influencing our model's performance metrics?

Now imagine that some non-trivial percentage of those data scientists do not even have the *option* to unpack those choices, because they have been made at the platform level and fully abstracted away from the user.

## CloudLock

Another thing that keeps me up at night about LCNC is the cost. On the surface, LCNC seems like a clear cost-saving homerun. Maybe you don't need to worry about hiring any engineers to build your website, or you can get away with not hiring a devOps team to deploy your app. Cloud offerings, including things like CloudFormation, Serverless, and Kubernetes do seem to offer a LCNC method to scale on a budget (this has even become a [joke](https://github.com/kelseyhightower/nocode)). But is that really the case?

Think about something like Ikea. Ikea furniture seems cost effective; it's easy to find, easy to get through your front door, and you can (theoretically) put it together yourself once you're home. But it ages quickly, and then you have to get a new bookcase. Fortunately with Ikea, you probably haven't made a 3-year commitment to buy all your furniture there.

Cloud providers like AWS, Azure, and Google Cloud make a lot of money selling cloud and "serverless" services like pieces of modular furniture that are easily combined, and easily augmented with new components. But at some point, you've built an entire home composed of individually-priced pieces of furniture, each of which cost significantly more than the particle board they were made from.

# Conclusion

As a technical person, there is very little attraction for me in most LCNC software. We want the things we make to have our unique stamp, whether that is the look and feel of a frontend, the model selection or hyperparameter tuning processes in the machine learning innards, and maybe even the data replication strategy on the backend.

What if you don't see yourself as a developer? Here's my advice. If there's a one-size-fits-all LCNC tool for it, there's likely a faster path to something more differentiated, more efficient, and more relevant to your use case. And if you start to feel indentured to your cloud provider for their LCNC services, there could very well be a better and more cost-effective path forward for you and your organization.


## References

- Alex Hudson, [The No Code Delusion](https://www.alexhudson.com/2020/01/13/the-no-code-delusion/)
- Alexander Ilg [Low Code / No-Code Solutions for SAP — or: Why Low Code sucks](https://medium.com/alexander-ilg/low-code-no-code-solutions-for-sap-or-why-low-code-sucks-70e0610c79e2)
- Andrey Glaschenko [Low Code Platforms — a Dangerous Bet](https://dzone.com/articles/low-code-platforms-a-dangerous-bet)
- Bruce McKinney [Hardcore Visual Basic](https://www.worldcat.org/title/hardcore-visual-basic/oclc/36841494)
- Devetry [Why Hasn’t Low-Code Revolutionized App Development Yet?](https://devetry.com/blog/why-hasnt-low-code-revolutionized-app-development-yet/)
- Drew Conry-Murray [Datanauts 128: Kubernetes, Serverless And No Code With Kelsey Hightower](https://packetpushers.net/podcast/datanauts-128-kubernetes-serverless-no-code-kelsey-hightower/)
- Kelsey Hightower [NoCode](https://github.com/kelseyhightower/nocode)
- Mark Troester [When developers shouldn’t trust low-code platforms](https://www.infoworld.com/article/3389682/when-developers-shouldnt-trust-low-code-platforms.html)
- Matthew MacDonald [The Rise and Fall of Visual Basic](https://developers.slashdot.org/story/19/06/22/2138248/the-rise-and-fall-of-visual-basic)
- Peter Wayner [Why developers hate low-code](https://www.infoworld.com/article/3438819/why-developers-hate-low-code.html)
- TFIR [Kelsey Hightower Explains No Code](https://www.youtube.com/watch?v=0yFIJ5izA48&ab_channel=TFiR)
- Tuba Ayyubi [Why Low Code Development Is Not As Great As We Think](https://opensenselabs.com/blog/tech/low-code-development-not-great)
- TJ VanToll [Why Low-Code Doesn’t Have to Be Awful](https://www.progress.com/blogs/why-low-code-doesnt-have-to-be-awful)

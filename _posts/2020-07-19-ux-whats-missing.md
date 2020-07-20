---
layout: post
title:  Why UX will Get Worse Before it Gets Better
image:
  feature: pepper_crop.png
tags:   dist_sys
date:   2020-07-19 15:46
---

The things we make are not user-friendly by accident; we have to *make* them that way. And that's hard. For most of the time people have been making things, we've been mainly concerned with making them user-friendly for just *us*. And, even if the last few decades of app development have brought more focus to the importance of empathy (especially if it helps you capture market share), the last few years have forced app developers to acknowledge the continued pervasiveness of white privilege, gender privilege, and class privilege in UI/UX. Unfortunately, as our efforts to become more intentional and empathetic as technologists continue in the coming years, there is another problem we have barely considered that will become a major threat to compassionate, egalitarian, and even subversive app development. Spoiler: it's our cloud infrastructure.


# The Voice of the User

While [it's originator is by no means a shining example of empathy](https://www.newyorker.com/science/elements/after-years-of-abusive-e-mails-the-creator-of-linux-steps-aside), Linux was the first major success in community-built software primarily because its development model embraced the voice of the user. Innovation, [wrote Eric Raymond in 1997](http://www.catb.org/~esr/writings/cathedral-bazaar/cathedral-bazaar/ar01s03.html), "mostly takes place in the open part of the tool where a large and varied community can tinker with it." Until that point, in tech, the only real model of development expected direction to be determined in a top-down fashion. The problem is that the people at the top were often not tuned into what users actually needed, or the problems they were encountering when they tried to use an OS or other software tool. This, perhaps more than anything else, is what started the open source movement. And while many of us have been [discouraged from OSS development platforms because we don't conform to others expectations of what a developer looks like](https://people.engr.ncsu.edu/ermurph3/papers/icse19gender.pdf), there are nonetheless a growing number of black, brown, women and non-binary contributors to OSS, simply because it is often a faster, if still imperfect, path to self-expression.

Obvious as this observeration may seem, the voices of minorities are not automatically included in the design of technology. In 1998, one year after Raymond wrote those words about the importance of users, Congress amended the Rehabilitation Act (originally published in 1973) to [require Federal agencies to make all electronic and information technology accessible to people with disabilities](https://en.wikipedia.org/wiki/Section_508_Amendment_to_the_Rehabilitation_Act_of_1973). By the time I started working in the Federal government in 2011, making sure web content was "508 compliant" was a common refrain, though usually a painfully uncomfortable afterthought.

Now, roughly 10 years later, it finally feels like user-centered design is accelerating. I've long since moved away from the public sector, turning instead towards the tech startup world to follow my passion for data science, machine learning, and artificial intelligence.  [UI and UX](https://en.m.wikipedia.org/wiki/User_experience_design) have become a huge part of the conversation. We've come a long way from considering only the legally-mandated accessibility issues ([supposing incorrectly that these are largely a solved problem](https://www.theatlantic.com/technology/archive/2018/11/city-apps-help-and-hinder-disability/574963/)) toward [gender inclusivity in app development](https://careerfoundry.com/en/blog/ux-design/design-for-every-gender/), and, only *very* recently, towards [acknowledging white privilege in product/app design](https://uxplanet.org/an-overdue-conversation-the-ux-research-industrys-achilles-heel-3524b1c6f908). Even so, this shift in focus to *all users*, instead of just *users who look like us*, has been slow and stilted. As UX Researcher [Vivianne Castillo](https://twitter.com/vcastillo630) [explains](https://uxplanet.org/an-overdue-conversation-the-ux-research-industrys-achilles-heel-3524b1c6f908):

> The UX Research Industry’s Achilles Heel rests in our inability to discuss, acknowledge and absolve the effects of unchecked white privilege and male privilege within our leadership, organizations, conferences, and research.

Of the UI/UX field's reluctance to engage in discussions of white privilege, Castillo [writes](https://uxplanet.org/an-overdue-conversation-the-ux-research-industrys-achilles-heel-3524b1c6f908):

> What we have instead is the constant repackaging and selling of best practices and ideas about how to “do” research faster and better without the call to carefully think about the biases and values we are unknowingly weaving into our research and the direct impact it has on the individuals and families exposed to the experiences and products we help create.

As a machine learning practitioner and data product developer, I strongly agree with Castillo's view; my field is similarly confronting many issues with white privilege, bias and ethics. And yet, I worry that even with the gains we are making with [developing more inclusive UIs](https://blog.prototypr.io/inclusive-design-and-accessibility-50718a3ac768) and [reflecting on the ethics of our ML](https://weaponsofmathdestructionbook.com/), we are missing out on an opportunity to address another systemic problem that, as Castillo says, we are unknowingly weaving into our applications, in their very infrastructures.

# Distributed UX Fails

If you're a techie working in app development, you probably identify as one of the following: "backend", "frontend" or "data science". Possibly this is one of our failings, that we have created these artificial silos for the problems that concern our data systems, the user-facing components of our applications, and the non-deterministic algorithms that stitch them together. This view isn't doing us any favors, and it certainly doesn't help our users. In fact, apps suffer greatly from the dissociation of these components. You can't build a backend if you don't understand how the data is going to be queried, just as you can't build machine learning models without considering how the users are going interact with them. The backend is everyone's problem.

The recent failures of companies like [Trivia HQ](https://slidebean.com/blog/what-happened-to-hq-trivia) and of apps like [Niantic's Pokémon Go](https://medium.theuxblog.com/an-honest-ux-critique-of-pok%C3%A9mon-go-from-a-longtime-fan-and-mobile-designer-76156c9cdc0c) belie the strong interconnectedness of the backend and the user's experience. As Slidebean writes of Trivia HQ's spectacular crash-and-burn:
> Livestreaming an interactive game through a mobile phone is hard. Very hard.Interactivity needed to be instant, especially if the questions are timed. But sometimes, as many users complained, clicking on an answer did nothing and time ran out. Which meant that users were kicked out. Other times, the quiz just didn’t work at all. So, when it crashed, which it did often, the hosts worked hard to keep the frustrated players from leaving before the problems were solved.

Pokémon Go was plagued with similar UX challenges that were also caused by underlying problems with the app's distributed data storage. Akhil Dakinedi [wrote](https://medium.theuxblog.com/an-honest-ux-critique-of-pok%C3%A9mon-go-from-a-longtime-fan-and-mobile-designer-76156c9cdc0c):
> It seems fine on paper, but once you see the extremely fast pace at which these battles take place, you start to notice the problems. The app, in its launch state, isn’t very responsive or fluid. It’s being plagued by constant server issues and unstable location tracking.

People wanted to like the game, but it's not fun to play a game that's laggy and slow, especially one that relies on interactivity and AR. Wrote [Amber Stechyshyn](https://usabilitygeek.com/pokemon-go-user-experience/):
> Pokémon Go is exciting and fun and the biggest new thing, but you will find people describing it just as often as slow, frustrating, and buggy. It was released quickly, hacked even quicker to allow for those outside the US to play it ahead of time, and has had server issues ever since.

Ultimately while the failures of apps like Trivia HQ and Pokémon Go may *manifest* in the UI, they come down to problems with commerical cloud storage offerings. As Dr. Benjamin Bengfort [writes](https://drum.lib.umd.edu/bitstream/handle/1903/21968/Bengfort_umd_0117E_19718.pdf?sequence=2&isAllowed=y),
> The launch of the augmented reality game Pokémon Go in the United States was an unmitigated disaster. Due to extremely overloaded servers from the release’s extreme popularity, users could not download the game, login, create avatars, or find augmented reality artifacts in their locales. The company behind the platform, Niantic, scrambled quickly, diverting engineering resources away from their feature roadmap toward improving infrastructure reliability. The game world was hosted by a suite of Google Cloud services, primarily backed by the Cloud Datastore, a geographically distributed NoSQL database. Scaling the application to millions of users therefore involved provisioning extra capacity to the database by increasing the number of shards as well as improving load balancing and autoscaling of application logic run in Kubernetes containers.

This isn't to say that the problem is inherent in GCC in particular; says Dr. Bengfort:
> Niantic’s quick recovery is often hailed as a success story for cloud services and has provided a model for elastic, on demand expansion of computational resources. A deeper examination, however, shows that Google’s global high speed network was at the heart of ensuring that service stayed stable as it expanded, and that the same network made it possible for the game to immediately become, available to audiences around the world.

The problem is that commercial cloud offerings, while technically available around the world, do not offer a consistent experiences to all of those users. In fact, your UX is *always* strongly coupled to geographic boundaries, whether it's hosted on Google, AWS, Azure, Alibaba, or any of the other cloud platforms. And that's the problem &mdash; what happens when we want our app to be truly international?

> The original launch of the game was in 5 countries – Australia, New Zealand, the United States, the United Kingdom, and Germany. The success of the game meant worldwide demand, and it was subsequently expanded to over 200 countries starting with Japan. Unlike previous games that were restricted with region locks, Pokemon GO was a truly international phenomenon and Niantic was determined to allow international interactions in the game’s feature set, interaction which relies on Google’s unified international architecture and globally distributed databases. Stories such Niantic’s deployment are increasingly becoming common and medium to large applications now require developers to quickly reason about how data is distributed in the wide area, different political regions, and replicated for use around the world.

What if, indeed, we consider not only global games, but things like global communications and policy?


# Why UX will Get Worse Before it Gets Better

In February 2020, something went wrong in Iowa. The Democratic caucuses leveraged a new voting app that was designed to enable voters to choose a presidential nominee. But the results were [delayed](https://www.vox.com/2020/2/3/21121883/iowa-caucus-results-delay-app-2020), and when they came in, they were inconsistent. Offically blamed on an unspecified ["coding error"](https://www.zdnet.com/article/how-the-iowa-caucus-app-went-wrong-and-how-open-source-could-have-helped/), the app developed by Shadow, Inc ([now BlueLink](https://www.vox.com/recode/2020/5/8/21251438/shadow-bluelink-iowa-caucus-app-rebranding)) almost certainly suffered from both eventual consistency and latency issues, classical distributed systems problems that were not afforded near sufficient attention in this case.

In Iowa the result was mistrust, conspiracy theories, and a general lack of confidence in a voting system that is already [struggling to improve UX](https://medium.com/@TarenSK/progressives-need-a-ux-design-revolution-195aa2c12894). Imagine what the result of a voting failure like this would have been had it occurred on the global political stage, such as the UN or WHO, where trust is already beginning to dissolve. Indeed, international technology is only becoming more controversial, with [the Huawei ban in the UK](https://www.cnn.com/2020/07/14/tech/huawei-uk-ban/index.html) and the US's [love](https://www.datacenterdynamics.com/en/news/report-google-cloud-sold-800m-cloud-services-tiktok-2019/)/[hate](https://www.wired.com/story/could-trump-win-the-war-on-huawei-and-is-tiktok-next/) relationship with TikTok only the latest examples.


# Linux, but Make It Distributed

We've begun to confront the systemic racism, sexism, classism, ableism, and heteronormativity baked into our favorite applications, our approaches to tech hiring, and our industry best practices.

We also need to agree that [user experience is inextricably linked to the backend](https://css-tricks.com/consistent-backends-and-ux:-why-should-you-care/), or as Tyler Treat [puts it](https://bravenewgeek.com/distributed-systems-are-a-ux-problem/), "Distributed systems are a UX problem". People who are geographically further away from where we make our apps are going to have a worse UX.

And then perhaps we need to go a step further. In the same way that programmers started coming together to build a better, open, operating system, perhaps we need to think about what it means to [break up with your corporate cloud provider](https://www.instagram.com/p/CB1dabtltyD/) on an even bigger scale.

# References

- Graff, Garrett. ["Could Trump Win the War on Huawei—and Is TikTok Next?"](https://www.wired.com/story/could-trump-win-the-war-on-huawei-and-is-tiktok-next/) (July 2020)

- Alley, Alex. ["Report: Google Cloud solds $800m in cloud services to TikTok in 2019"](https://www.datacenterdynamics.com/en/news/report-google-cloud-sold-800m-cloud-services-tiktok-2019/) (July 2020)

- Beauchamp, Zack, Peters, Cameron, and Collins, Sean. ["Why the Iowa results are taking so long"](https://www.vox.com/2020/2/3/21121883/iowa-caucus-results-delay-app-2020) (February 2020)

- Bengfort, Benjamin. ["Planetary Scale Data Storage"](https://drum.lib.umd.edu/handle/1903/21968) (November 2019)

- Castillo, Vivianne. ["An Overdue Conversation: The UX Research Industry’s Achilles Heel"](https://uxplanet.org/an-overdue-conversation-the-ux-research-industrys-achilles-heel-3524b1c6f908) (June 2018)

- Cohen, Noam. ["After Years of Abusive E-mails, the Creator of Linux Steps Aside"](https://www.newyorker.com/science/elements/after-years-of-abusive-e-mails-the-creator-of-linux-steps-aside) (September 2018)

- Dakinedi, Akhil [An Honest UX critique of Pokémon Go, from a longtime fan and mobile designer](https://medium.theuxblog.com/an-honest-ux-critique-of-pok%C3%A9mon-go-from-a-longtime-fan-and-mobile-designer-76156c9cdc0c) (July 2016)

- De Rooms, Brecht. ["Consistent Backends and UX: Why Should You Care?"](https://css-tricks.com/consistent-backends-and-ux:-why-should-you-care/) (March 2020)

- Gold, Hadas. ["UK bans Huawei from its 5G network in rapid about-face"](https://www.cnn.com/2020/07/14/tech/huawei-uk-ban/index.html) (July 2020)

- Hamraie, Aimi. ["A Smart City Is an Accessible City"](https://www.theatlantic.com/technology/archive/2018/11/city-apps-help-and-hinder-disability/574963/) (November 2018)

- Miller, Josephine. ["Inclusive Design and Accessibility."](https://blog.prototypr.io/inclusive-design-and-accessibility-50718a3ac768) (October 2018)

- O’Neil, Cathy. ["Weapons of Math Destruction: How Big Data Increases Inequality and Threatens Democracy"](https://weaponsofmathdestructionbook.com/) (June 2016)

- Querini, Vale. ["Design for Every Gender"](https://careerfoundry.com/en/blog/ux-design/design-for-every-gender/) (March 2020)

- Raymond, Eric. ["The Cathedral and the Bazaar"](http://www.catb.org/~esr/writings/cathedral-bazaar/cathedral-bazaar/) (May 1997).

- Shop.Thoughtful. ["How to (Mostly) Stop Using Amazon"](https://www.instagram.com/p/CB1dabtltyD/) (June 2020)

- Slidebean. ["HQ Trivia's failed mutiny against their CEO"](https://youtu.be/eGClgNa3SxA) (February 2020)

- Stechyshyn, Amber. ["Pokémon Go And Its Impact On User Experience"](https://usabilitygeek.com/pokemon-go-user-experience/) (August 2016)

- Stinebrickner-Kauffman, Taren. ["Progressives Need a UX Design Revolution"](https://medium.com/@TarenSK/progressives-need-a-ux-design-revolution-195aa2c12894) (November 2018)

- Treat, Tyler. ["Distributed Systems are a UX Problem"](https://bravenewgeek.com/distributed-systems-are-a-ux-problem/) [slides](https://www.slideshare.net/mobile/TylerTreat/distributed-systems-are-a-ux-problem) [video](https://m.youtube.com/watch?v=5aOZ2bIKy-w) (June 2015)

- Vaughan-Nichols, Steven. ["How the Iowa caucus app went wrong and how open source could have helped"](https://www.zdnet.com/article/how-the-iowa-caucus-app-went-wrong-and-how-open-source-could-have-helped/) (February 2020)

- Wikipedia. ["Section 508 Amendment to the Rehabilitation Act of 1973](https://en.wikipedia.org/wiki/Section_508_Amendment_to_the_Rehabilitation_Act_of_1973) (July 2020)

- Wikipedia. ["User Experience Design"](https://en.m.wikipedia.org/wiki/User_experience_design) (July 2020)



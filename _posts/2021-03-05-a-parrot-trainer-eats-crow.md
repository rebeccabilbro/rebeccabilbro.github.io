---
layout: post
title:  A Parrot Trainer Eats Crow
image:
  feature: pepper_crop.png
date:   2021-3-10 18:42:34
tags:   machine_learning
---

In this post, we'll consider how it is that models trained on massive datasets using millions of parameters can be both "low bias" and also *very biased*, and begin to think through what we in the ML community might be able to do about it.

## Birds on a Wire

In the machine learning community, we are trained to think of size as inversely proportional to bias. We associate small datasets with the problem of underfit, which is to say high bias. We learn that in the face of unfamiliar data, underfit models make poor assumptions that lead to inaccuracies. Likewise, we call models with smaller sets of hyperparameters "weak learners" because their limited complexity limits our ability to reduce bias even as our dataset size grows.

This intuition has driven the ML community towards ever larger datasets and increasingly complex model architectures, and to be sure, towards ever better accuracy scores. Unfortunately (and not unironically), this progression has driven a wedge between the ML definition of "bias" and the more colloquial sense of the word.


## Migration Patterns

To understand our situation, it may help to trace back through the pattern of our collective migration towards these more complex models.

> "Is deep learning really necessary to solve most machine learning problems?"

This question has come to me more times than I can count over the years, both at work and with my students. It often comes laced with some underlying anxiety. Sometimes it means "These deep learning hyperparameters are really tedious to tune, are you sure it's worth my time to learn them?". Sometimes it means "does your solution actually use neural models, or is this just a marketing layer on top of a Logistic Regression?".

To be fair, I find this kind of skepticism totally healthy. We even gave the skeptics a little shout-out in [our book's](https://learning.oreilly.com/library/view/applied-text-analysis/9781491963036/) chapter on deep learning, writing,
> As application developers, we tend to be cautiously optimistic about the kinds of bleeding-edge technologies that sound good on paper but can lead to headaches when it comes to operationalization.

My own views about the value and practicality of deep learning are always changing, and my answers to askers of this question have shifted over time. While I almost always bring up what I see as the two main tradeoffs between traditional models and deep learning, namely model complexity (neural models are more complicated, harder to tune, easier to mess up) and speed (neural models tend to take longer to train and can impede rapid prototyping and iteration), I am much more encouraging about the use cases for deep learning these days than I used to be.

The reality is that neural models are getting more practical to use all the time, and even if they require us to grapple with more complexity, the rewards of being able to scale complexity are hard to ignore. Given enough data, neural models are likely to always outperform more traditional machine learning algorithms, simply because they don't ever have to stop learning.

## Training Parrots

Industry's shift towards deep learning in earnest has become particularly evident to me in the last 5 or 6 years of building commercial NLP applications. Five years ago, we were all using software designed out of the computational linguistics tradition &mdash; models that took into account things like part-of-speech tags, n-grams, and syntactic parsers (e.g. [NLTK](https://www.nltk.org/)). Three years ago, the community had begun to shift towards software that leveraged a hybrid of computational linguistics and neural network-trained distributed representations (e.g. [SpaCy](https://spacy.io/), [Gensim](https://radimrehurek.com/gensim/)). These new hybrid libraries abstracted away much of the grammar-based feature extraction work that we previously had to do ourselves. Now, in the first half of 2021, many folks go directly to projects like [HuggingFace's Transformers library](https://huggingface.co/transformers/), leveraging pre-trained language models that require no feature extraction at all beyond transformation from arrays into tensors.

The progression over the last few years has been amazing to watch. There have never been more excellent open source resources for people who do what I do. It has never been easier to [bootstrap a domain-specific language model](https://rebeccabilbro.github.io/tailored-learning/), even if [you don't have much data to start with](https://rebeccabilbro.github.io/small-data-delegated-literacy/). But it's also true that we have never been more removed from our data than we are today, or less in touch with its underlying patterns, themes, and biases.

This problem is at the heart of the recent paper [On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?](https://dl.acm.org/doi/pdf/10.1145/3442188.3445922) The paper itself is at the heart of a controversy about Google's [abrupt dismissal](https://www.bbc.com/news/technology-56135817) of two of the authors, Dr. Timnit Gibru and Dr. Margaret Mitchell, who helped found and lead Google's AI Ethics team.

The Parrots paper discusses a range of concerns with large language models (like the ones Google makes), including the dangers of "ersatz fluency" and the environmental costs of training such models. Indeed, we seem to be entering a new phase in which machine models are only distinguishable from humans by their absence of legal and ethical responsibilities for the ramifications of their words and actions. Moreover, as with cryptocurrencies and [cryptoart like NFTs](https://everestpipkin.medium.com/but-the-environmental-issues-with-cryptoart-1128ef72e6a3), it is becoming clear that the costs are disproportionately paid by people unlikely to realize much of their benefits.

The paper is, however, primarily a warning about the challenge of responsibly building deep learning models that require a volume of data that exceeds human capacity to effectively curate. And as an NLP developer, this was the part of the paper that triggered that uneasy feeling in the pit of my stomach. This is something that ~~we~~ I need to take responsibility for and help fix. But how?

## Eating Crow

Presumably the first step is admitting you have a problem. OpenAI [has acknowledged](https://github.com/openai/gpt-3/blob/master/model-card.md#limitations) that GPT-3 exhibits concerning NLG properties, which they attribute to the training data:

> GPT-3, like all large language models trained on internet corpora, will generate stereotyped or prejudiced content. The model has the propensity to retain and magnify biases it inherited from any part of its training, from the datasets we selected to the training techniques we chose. This is concerning, since model bias could harm people in the relevant groups in different ways by entrenching existing stereotypes and producing demeaning portrayals amongst other potential harms.


In his article, "For Some Reason I’m Covered in Blood", [Dave Gershgorn](https://onezero.medium.com/for-some-reason-im-covered-in-blood-gpt-3-contains-disturbing-bias-against-muslims-693d275552bf) writes about GPT-3's problem with Islam:
> This bias is most evident when GPT-3 is given a phrase containing the word “Muslim” and asked to complete a sentence with the words that it thinks should come next. In more than 60% of cases documented by researchers, GPT-3 created sentences associating Muslims with shooting, bombs, murder, and violence.

So, yes, as an NLP developer, I *am* concerned that leveraging pretrained LMs in my consumer-facing products could manifest in bias that might alienate my Muslim, my women, my LGBTQ+ users. However, I am *also* concerned about how my commercialization of such LMs could serve to further normalize and entrench racist, sexist, anti-Islamic, homophobic, transphobic, and white supremist beliefs for everyone else.

As developers, when we build data products, we help produce the training data that will be used for the next generations of machine learning models. When we build atop models like GPT-3, that has the effect of ensuring that bias and hate speech remain in the collective conversation online, indefinitely.

How can we do a better job of dataset curation for large language models to avoid the problem of poisonous training data? In the Parrots paper, Dr. Gibru et al. discuss some of the approaches that were used to filter the training data for models like GPT-3 and BERT:
> The Colossal Clean Crawled Corpus...is cleaned, *inter alia*, by discarding any page containing one of a list of about 400 “Dirty, Naughty, Obscene or Otherwise Bad Words". This list is overwhelmingly words related to sex, with a handful of racial slurs and words related to white supremacy (e.g. swastika, white power) included. While possibly effective at removing documents containing pornography (and the associated problematic stereotypes encoded in the language of such sites) and certain kinds of hate speech, this approach will also undoubtedly attenuate, by suppressing such words as *twink*, the influence of online spaces built by and for LGBTQ people. If we filter out the discourse of marginalized populations, we fail to provide training data that reclaims slurs and otherwise describes marginalized identities in a positive light.

In other words, the data cleaning mechanisms in place are crude at best, and perhaps overly aggressive in filtering out marginalized conversations that may be punctuated by reclaimed "bad" words. And yet...any solution I can think of that would manage to include marginalized conversations might also produce language models prone to using those reclaimed words.

This leads us to the question of whether it would *ever* be ok for a LM to use a word like "twink". Knowing who can use and who should refrain from using such reclaimed words is something that humans &mdash; despite our access to education, historical context about oppression, and discussions about systemic racism, sexism, and homophobia &mdash; [still routinely screw up](https://www.yahoo.com/lifestyle/papa-johns-founder-says-hes-211500691.html?guccounter=1&guce_referrer=aHR0cHM6Ly93d3cuZ29vZ2xlLmNvbS8&guce_referrer_sig=AQAAAJKwRjOsKJ2Ob0xoccP5Ck2jNFa2Oss-dVj11oSHLODckm7Yi_S-TCkt-8eKFrB8ghQzscpnl9bqLe4wUCgu2cn75e6AqZ0zpSVWH0GYYKfTWHICUk-jCSu6cnixkdFF5tX1K0U6aNmJWyom-2WDt3HMvT5_DI5PGb_F-gytgYkQ).


## Beyond the Gilded Cage

My sense is that an awareness of appropriate use for things like reclaimed words, code switching, and patois involve a degree of complexity that we cannot reasonably expect of any global model. Instead, perhaps the answer is to decolonize our language models.

[Mohamed, et al.](https://arxiv.org/pdf/2007.04068.pdf) summarize three strategies for the decolonisation of artificial intelligence: the decentering view, the additive-inclusive view, and the engagement view. It is interesting to think about how these methods might be used to inform the model development, training, and evaluation processes. For instance, for the decentering view, this could mean training models on non-white, non-male, non-Western, non-Judeo Christian conversations, rather than applying zero-shot learning techniques to tack additional training onto pretrained LMs that have already encoded the white, male, Western, Judeo Christian viewpoint.

Reading the Parrots paper also got me thinking and reading up on indigenous language models (e.g. [this workshop](https://aiforgood.itu.int/events/indigenous-knowledge-and-ai/), [this article](https://medium.com/codingrights/decolonising-ai-a-transfeminist-approach-to-data-and-social-justice-a5e52ac72a96), and [this blog](http://blog.shakirm.com/2018/10/decolonising-artificial-intelligence/)). My research led me to find a very interesting piece called the [Indigenous Protocol and Artificial Intelligence Position Paper](https://spectrum.library.concordia.ca/986506/) that was recently published by a consortium of indigenous researchers, with the following passage:

> Indigenous ways of knowing are rooted in distinct, sovereign territories across the planet. These extremely diverse landscapes and histories have influenced different communities and their discrete cultural protocols over time. A single ‘Indigenous perspective’ does not exist, as epistemologies are motivated and shaped by the grounding of specific communities in particular territories. Historically, scholarly traditions that homogenize diverse Indigenous cultural practices have resulted in ontological and epistemological violence, and a flattening of the rich texture and variability of Indigenous thought. Our aim is to articulate a multiplicity of Indigenous knowledge systems and technological practices that can and should be brought to bear on the ‘question of AI.’

Perhaps the time has come to move away from monolith language models that reduce the rich variations and complexities of our conversations to a simple argmax on the output layer, and instead embrace a new generation of language model architectures that are just as organic and diverse as the data they seek to encode.


## References

- Emily M. Bender, Timnit Gebru, Angelina McMillan-Major, and Shmargaret Shmitchell. 2021. [On the Dangers of Stochastic Parrots: Can Language Models Be Too Big?](https://dl.acm.org/doi/pdf/10.1145/3442188.3445922)
- Shakir Mohamed. 2018. [Decolonising Artificial Intelligence](http://blog.shakirm.com/2018/10/decolonising-artificial-intelligence/)
- Shakir Mohamed, Marie-Therese Png, William Isaac. 2020. [Decolonial AI: Decolonial Theory as Sociotechnical Foresight in Artificial Intelligence](https://arxiv.org/pdf/2007.04068.pdf)
- Paz Peña and Joana Varon. 2020. [Decolonising AI: A transfeminist approach to data and social justice](https://medium.com/codingrights/decolonising-ai-a-transfeminist-approach-to-data-and-social-justice-a5e52ac72a96)
- Davar Ardalan, Burr Settles, Chamisa Edmo, Tracy Monteith, Wolfgang Victor Yarlott, and Alva Lim. 2020. [Indigenous Knowledge and AI](https://aiforgood.itu.int/events/indigenous-knowledge-and-ai/)
- Geoff McMaster. 2020. [Creating ethical AI from Indigenous perspectives](https://www.ualberta.ca/folio/2020/10/creating-ethical-ai-from-indigenous-perspectives.html)
- Jason Edward Lewis, Angie Abdilla, Noelani Arista, Kaipulaumakaniolono Baker, Scott Benesiinaabandan, Michelle Brown, Melanie Cheung, Meredith Coleman, Ashley Cordes, Joel Davison, Kūpono Duncan, Sergio Garzon, D. Fox Harrell, Peter-Lucas Jones, Kekuhi Kealiikanakaoleohaililani, Megan Kelleher, Suzanne Kite, Olin Lagon, Jason Leigh, Maroussia Levesque, Keoni Mahelona, Caleb Moses, Isaac ('Ika'aka) Nahuewai, Kari Noe, Danielle Olson, 'Ōiwi Parker Jones, Caroline Running Wolf, Michael Running Wolf, Marlee Silva, Skawennati Fragnito and Hēmi Whaanga. 2020. [Indigenous Protocol and Artificial Intelligence Position Paper](https://spectrum.library.concordia.ca/986506/)
- Ashwin Rodrigues. 2016. [A History of SmarterChild](https://www.vice.com/en/article/jpgpey/a-history-of-smarterchild)
- Frank Schilder. 2020. [GPT-3: The good, the bad and the ugly](https://towardsdatascience.com/gpt-3-the-good-the-bad-and-the-ugly-5e2e5b7f0f66)
- Liz O'Sullivan and John Dickerson. 2020. [Here are a few ways GPT-2 can go wrong](https://techcrunch.com/2020/08/07/here-are-a-few-ways-gpt-3-can-go-wrong/)
- Tristan Greene. 2020. [GPT-3's bigotry is exactly why devs shouldn't use the internet to train AI](https://thenextweb.com/neural/2020/09/24/gpt-3s-bigotry-is-exactly-why-devs-shouldnt-use-the-internet-to-train-ai/)
- Will Douglas Heaven. 2020. [How to make a chatbot that isn't racist or sexist](https://www.technologyreview.com/2020/10/23/1011116/chatbot-gpt3-openai-facebook-google-safety-fix-racist-sexist-language-ai/)
- Dave Gershgorn. 2020. [‘For Some Reason I’m Covered in Blood’: GPT-3 Contains Disturbing Bias Against Muslims](https://onezero.medium.com/for-some-reason-im-covered-in-blood-gpt-3-contains-disturbing-bias-against-muslims-693d275552bf)
- Jonathan Vanian. 2020. [Your favorite A.I. language tool is toxic](https://fortune.com/2020/09/29/artificial-intelligence-openai-gpt3-toxic/)
- Eliza Strickland. 2021. [OpenAI's GPT-3 Speaks! (Kindly Disregard Toxic Language)](https://spectrum.ieee.org/tech-talk/artificial-intelligence/machine-learning/open-ais-powerful-text-generating-tool-is-ready-for-business)
- Benjamin Bengfort, Rebecca Bilbro, Tony Ojeda. 2018. [Applied Text Analysis with Python: Building Language-Aware Data Products](https://learning.oreilly.com/library/view/applied-text-analysis/9781491963036/)
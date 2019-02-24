---
layout: post
title:  Boxing and Unboxing - Kubernetes for ML
image:
  feature: pepper_crop.png
tags:   devops
date:   2019-02-24 09:28
---

There is, at best, a tenuous relationship between the emerging field of DevOps and the more prevalent but still incipient one of Data Science. Data Science (when it works) works best by contributing exploratory data analysis and munging, hypothesis tests, rapid prototypes, and non-deterministic features. But then who is responsible for transforming *ad hoc* EDA and data cleaning steps into ETL pipelines? Who containerizes the experimental code and models into packages for deployment? Who sets up CI tools to monitor deployed code as new predictive features are integrated? Increasingly, such responsibilities are becoming the domain of the DevOps Specialist. And if the mythical Data Scientist (as the world imagined her 5 years ago during Peak Data Science Mysticism) was a mage capable of squeezing predictive blood from data stones, the lionhearted DevOps Specialist is now the real hero of the story &mdash; Moses holding back the Red Sea while the Data Scientists sit in tidepools digging in the sand for little crabs. 

## Data Scientists Should Understand Deployment and Scaling

My personal opinion is that data scientists should understand how to deploy and scale their own models. I believe overspecialization is generally a mistake; if the research question requires not only experimentation but repeatability, the scientist should build the apparatus in such a way as to support successive experiments &mdash; her own *and* those of future researchers. If the business problem requires not only machine learning model prototyping, but the integration of successful models into the application, we should build the modeling pipeline in such a way as to support deployment. 

> "Machine learning engineer (MLE) is an emerging job title for software engineers specializing in building machine learning systems. MLEs have an understanding of data science and machine learning, though they are perhaps not as strong on the fundamentals as a data scientist. They are much stronger, though, in their understanding of how to build, deploy and support production-quality software." - [Charrington, TWiML](https://twimlai.com/kubernetes/)

In my view, these responsibilies should **not** be delegated to different team members &mdash; the scientist understands how the apparatus needs to work; building it so that it doesn't break after the first experiment is simply a matter of dedicating the necessary time and effort. This is also the case with machine learning models.

## But It's Hard

But here's the thing; it's hard. It's definitely not an insignificant amount of time and effort to figure out how your models can or should fit into a larger ecosystem of microservices, or how they should make use of a data layer that may be growing rapidly distributed. For the last year or so, I've been teaching myself Go, experimenting with Docker, reading about applications development, and learning about distributed systems and consensus, all in an effort to shore up my ability to play more of a role in the deployment of the models I build at work. One of the tools that I've been trying to get motivated to learn is Kubernetes. 

Over the summer I took Sebastien Goasguen's [Intro to Kubernetes](https://learning.oreilly.com/live-training/courses/introduction-to-kubernetes/0636920264002/) class via O'Reilly's online training. I had the sense that I was probably the only machine learning/data science person in the whole class, and I'll admit that it was a little tough to connect what Sebastien was saying to the everyday work that I do; it was about an hour of wrestling with my OS to get `minikube` and `kubectl` properly installed and configured, followed by two hours of staring at and editing YAML files. (Sorry Sebastien, I'm sure it was me and not you.)

In one of my more frustrated moments I might have called Kubernetes "basically Excel for container orchestration." But it's also incredibly important to the work I'm doing, and to some side projects I'll be working on over the next few months, which means its time to suck it up and take another swing... 

## Scaling the Delivery of Machine Learning

This weekend I read ["Kubernetes for Machine Learning, Deep Learning, and AI"](https://twimlai.com/kubernetes/), a short e-book by Sam Charrington of [This Week in Machine Learning](https://twimlai.com/). 

The book seems to be aimed mainly at larger organizations (they mention Booking.com and OpenAI in the case studies). It suggests, for instance, that the engineering team build specialized computing environments and APIs to orchestrate automated provisioning to facilitate the work of the data science team &mdash; potentially a lot more infrastructure than most small teams would be able to pull off, and also imagining a company big enough to have a data science team distinct from the engineering team. 

However, I liked the contextualization of containers and orchestration in terms of the machine learning workflow and the walkthrough of the current 3rd party ML/Kube tools out there. There were useful takeaways that I think would make sense in both the very large and very small organizations where I've worked. A few of my favorite lines:

> "Much of the industry dialogue around machine learning is focused on modeling, but to achieve scale models must be developed within a repeatable process that accounts for the critical activities that precede and follow model development."

> "Model inference is even more computationally expensive than model training, though they use computing resources very differently.* While training might require large bursts of CPU or GPU over the course of several hours, days or weeks, each inference against a deployed model requires a small but significant amount of computing power. Unlike the demands of training, the computational burden of inference scales with the number of inferences made and continues for as long as the model is in production."

> "Files created within a container are ephemeral, meaning they don’t persist beyond the lifetime of the container. This presents critical issues when building real-world applications in general and with machine learning systems in particular... container runtimes like Docker provide mechanisms to attach persistent storage to the containers they manage. However, these mechanisms are tied to the scope of a single container, are limited in capability, and lack flexibility."

> "Putting a model in production is the beginning of the model’s journey, not the end." 
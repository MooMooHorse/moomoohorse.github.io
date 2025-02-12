---
layout: post
title:  "My experience at Microsoft Research"
summary: "Part 1"
author: moomoohorse
date: '2024-08-15 15:01:51 -0500'
category: work_summary
thumbnail: /assets/img/posts/Microsoft_logo.png
keywords: summary
permalink: /blog/microsoft-research-part-1
usemathjax: true
---

# Checkout summary

I finished the journey as an intern at Microsoft Software Technology Center Asia (STCA). My role is Research Software Development Engineer Intern. 

I could not share too much about the specific works I did until the paper is set & ready to publish. (Now it is! Submitted to FSE :) But there is still so much I learned besides these concrete topics.

The summary will be in following parts:

* Thoughts on research
* Thoughts on engineering



## Thoughts on research

One interesting lesson I learnt from research is, a great question is more important than a any answers.

Hence, the following are a set of great questions I think are worth pondering:

1. Define problem space / research space
   * Q: There are tons of problems out there, why are we looking at this aspect of the problem? [what's the people's problem]
   * Q: There are tons of attempts available, why are we using our solution? [what's the technical problem]
   * Q: Does the problem / motivation really exist? [how to balance over-thinking and over-confidence]
   * Q: Does our solution stand? [how do we measure its quality]
2. Facts, data and reasoning generate idea. 
   * Q: How do we get the data? [how to balance reading, experimenting and thinking]
   * Q: When is the data enough? [how to balance over-thinking and over-confidence]
3. Ideas produce facts, data, reasoning. Hence, evaluation matters.
  * Q: How to design a way to let our idea becomes facts, data and reasoning? [how to design evaluation]
  * Q: If our idea is not working / killed, should we diversify or focus? [how to balance over-thinking and over-confidence]
4. Ideas, plans, implementations should be simple
  * Q: It's normal to have a simple problem with a complex idea, how to make it simple? Should we make it simple? [how to simplify the idea]
5. Refined ideas and plans must be written down in various forms
  * Q: Does presentation of our work matter? [how to present our work]
  * Q: Drawing a diagram might be time-consuming, but it also greatly improves communication between researchers. How to balance? [how to present our work]
6. Have a concrete (task, work-item, evaluation, deadline) plan
  * Q: How do we make a plan? [how to plan with concrete objectives and milestones]
  * Q: Should we have a high-level or low-level plan? [how to plan with concrete objectives and milestones]
7. Each step comes with a discussion, covering the bottlenecks, what's changed, and what we have
  * Q: Talking to other people is frightning. Under-preparing wastes your value in other people's mind. Over-preparing wastes your time. How to balance? [when and how to sync up with others]
8. Implementation must be reproducible, followed by careful testing & checking
  * Q: should we scratch and then build the details or should we build it step by step? [how to implement]
10. Always be rational and open so you can rebuild happily
  * Q: How do we face collapse of our work? [how to face failure]


## Thoughts on engineering

I really like [Principles For Success by Ray Dalio](https://www.youtube.com/watch?v=B9XGUpQZY38).

Similar to investment, engineering takes principles.

The following are a set of principles I think are worth pondering:

1. Do basic research (finding motivation, profiling, reading) while writing down your plan, design document.  
  * Example: design a dataset. With an evaluation plan, profile the existing / brute-force solutions to identify the problem space.

2. Discuss it widely and refine and iterate the version before we start.
  * Example: discuss the findings and ideas you have with your managers before you move on.

3. Start from the basic version. By basic we mean a version with the least **implementation** but with the full **capabilities**.
  * Example: Pick one entry from the dataset and build a proof-of-concept system.

4. Iterate the version.
  * Example: add feature / improvement gradually and fully test each version.
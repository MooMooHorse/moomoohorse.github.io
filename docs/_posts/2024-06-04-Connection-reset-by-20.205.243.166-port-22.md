---
layout: post
title:  "Git: Connection reset by 20.205.243.166 port 22"
summary: "A solution to git connection error caused by proxy setting"
author: moomoohorse
date: '2024-06-04 09:40:16 -0500'
category: random
thumbnail: /assets/img/posts/v2raysetting.png
keywords: random
permalink: /blog/gitconnectionv2ray
usemathjax: true
---

Add this to your `~\.ssh\config` if the github.com - port 22 hasn't been set properly with the following proxy setting.
```
Host github.com
  port 22
  User git
  HostName github.com
  PreferredAuthentications publickey
  IdentityFile ~/.ssh/id_rsa
  # 10808 is local socks listening port number, find it in your v2ray / clash setting (through GUI, preferrably)
  ProxyCommand connect -S 127.0.0.1:10808 -a none %h %p
```


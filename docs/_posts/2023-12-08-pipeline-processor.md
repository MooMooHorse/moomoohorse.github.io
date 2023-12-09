---
layout: post
title:  "Pipeline processor built from scratch"
summary: "Use VCS, openRAM, and magic to build a pipeline processor from scratch"
author: moomoohorse
date: '2023-12-09 01:42:56 -0600'
category: ['computer-architecture']
thumbnail: /assets/img/posts/cuda_profiling_sample.png
keywords: computer-architecture
permalink: /blog/pipeline-processor
usemathjax: true22
---



[repos](https://github.com/MooMooHorse/CRC_processor)



## Current Progress

- **[Done]** Pipeline processor w/ static branch prediction
- **[Done]** Multi-level cache
- **[Done]** Fully customizable cache
- **[Done]** Branch predictors, BTB, RAS
- **[Done]** Prefetchers



<br>

## Statistics & Observations

### Prefetchers and Predictors

Context: Default 2-level cache, Conservative prefetcher, Baseline Predictor
- Baseline configuration
```
    stop time is          31500260000
    IPC: 0.236838
    L1 I Cache:    1052928 hits,        656 misses,    2111237 cycles,      8.203 penalty
    L2 I Cache:        556 hits,        100 misses,       3414 cycles,     23.020 penalty
    L1 D Cache:      73868 hits,         68 misses,     148678 cycles,     13.853 penalty
    L2 D Cache:         84 hits,         24 misses,        738 cycles,     23.750 penalty
    Predictor :    149981 misses for     211564 branch instr.
    Prefetcher:      5318 prefetches
    $finish at simulation time          31538320000
```

Context Default 2-level cache, Conservative prefetcher, Global Predictor w/ 1-Way BTB
- Shows that 1-way BTB is better than **both** Baseline and **and** 4-way BTB on Coremark.
- Shows that predictors can be beneficial to Coremark.
```
    stop time is          27107780000
    IPC: 0.275292
    L1 I Cache:     906514 hits,        603 misses,    1818190 cycles,      8.561 penalty
    L2 I Cache:        501 hits,        102 misses,       3354 cycles,     23.059 penalty
    L1 D Cache:      73868 hits,         68 misses,     148678 cycles,     13.853 penalty
    L2 D Cache:         84 hits,         24 misses,        738 cycles,     23.750 penalty
    Predictor :     76781 misses for     211564 branch instr.
    Prefetcher:      5290 prefetches
    $finish at simulation time          27143740000
```

Context: Default 2-level cache, Conservative prefetcher, Local predictor w/ 4-way BTB
- Shows that Local predictor on Coremark is better than Baseline.
```
    stop time is          31109120000
    IPC: 0.239635
    L1 I Cache:    1039890 hits,        656 misses,    2085161 cycles,      8.203 penalty
    L2 I Cache:        556 hits,        100 misses,       3414 cycles,     23.020 penalty
    L1 D Cache:      73868 hits,         68 misses,     148678 cycles,     13.853 penalty
    L2 D Cache:         84 hits,         24 misses,        738 cycles,     23.750 penalty
    Predictor :    143462 misses for     211564 branch instr.
    Prefetcher:      5318 prefetches
    $finish at simulation time          31147180000
```

Context: Default 2-level cache, Conservative prefetcher, Local predictor w/ 1-way BTB
- Shows that conservative prefetcher is ***worse*** than the case without prefetchers
- since we have few cache misses and the prefetcher won't positively affect the performance.
- The degradation is due to additional cache hit latency.
```
    stop time is          27055390000
    IPC: 0.275790
    L1 I Cache:     901272 hits,        596 misses,    1807650 cycles,      8.567 penalty
    L2 I Cache:        495 hits,        101 misses,       3319 cycles,     23.059 penalty
    L1 D Cache:      73868 hits,         68 misses,     148678 cycles,     13.853 penalty
    L2 D Cache:         84 hits,         24 misses,        738 cycles,     23.750 penalty
    Predictor :     76782 misses for     211652 branch instr.
    Prefetcher:         0 prefetches
    $finish at simulation time          27091310000
```

Context: Default 2-level cache, Conservative prefetcher, Global predictor w/ 1-way BTB
- Shows that Local predictor is better than Baseline but is inferior to Global predictor.

```
    stop time is          27831170000
    IPC: 0.268125
    L1 I Cache:     927138 hits,        593 misses,    1859346 cycles,      8.550 penalty
    L2 I Cache:        493 hits,        100 misses,       3292 cycles,     23.060 penalty
    L1 D Cache:      73868 hits,         68 misses,     148678 cycles,     13.853 penalty
    L2 D Cache:         84 hits,         24 misses,        738 cycles,     23.750 penalty
    Predictor :     89694 misses for     211652 branch instr.
    Prefetcher:         0 prefetches
    $finish at simulation time          27867030000
```

### Parameterized Cache

Parameter search space
- **Word size:** `{128, 256, 512, 1024}`
- **L1 cache:** `16` sets, `4` ways (fixed at CP1, CP2 baseline)
- **L2 cache:** `{16, 32, 64, 128, 256}` sets, `{4, 8, 16}` ways

*Important Notes*
- *IPCs are lower because these experiments use a commit **less optimized** in prefetching and branch prediction.*
- *Experiments are extensive, so refer to the [appendix](./mp4cp3_appendix.md) for detailed logs.* <br>
- *Here we only select configurations with a **128KB budget** for **L2 cache**.*

<br>

Baseline: L1 cache only, 256 wordsize, 16 sets, 4 ways
```
    stop time is          32524050000
    IPC: 0.229373
    L1 I Cache:    1173571 hits,       1280 misses,    2361298 cycles,     11.059 penalty
    L1 D Cache:      73801 hits,        135 misses,     149582 cycles,     14.667 penalty
    $finish at simulation time          32566770000
```

128 wordsize, 64 sets, 16 ways
- Miss penalty is low, but L1 cache miss rate is high.
- Therefore, performance degrades compared to the baseline.
```
    stop time is          32776490000
    IPC: 0.227675
    L1 I Cache:    1173862 hits,       8476 misses,    2395276 cycles,      5.610 penalty
    L2 I Cache:       7740 hits,        736 misses,      22125 cycles,      9.029 penalty
    L1 D Cache:      73361 hits,        575 misses,     151694 cycles,      8.647 penalty
    L2 D Cache:        784 hits,        171 misses,       3247 cycles,      9.819 penalty
    $finish at simulation time          32824340000
```

256 wordsize, 128 sets, 4 ways
- L1 I cache miss is dramatically reduced. **This is the optimal configuration given the budget.**
- This advantage is gained at the expense of an exceptional number of sets.
```
    stop time is          32477390000
    IPC: 0.229732
    L1 I Cache:    1173378 hits,       1280 misses,    2356592 cycles,      7.684 penalty
    L2 I Cache:        900 hits,        380 misses,       5997 cycles,     11.045 penalty
    L1 D Cache:      73801 hits,        135 misses,     149261 cycles,     12.289 penalty
    L2 D Cache:        106 hits,         87 misses,       1254 cycles,     11.977 penalty
    $finish at simulation time          32520420000
```

512 wordsize, 16 sets, 16 ways *OR* 512 wordsize, 32 sets, 8 ways
- Larger word size introduces heavier miss penalty, which is starting to outweigh the benefit of reducing misses.
- So we would rather go for the fine-grained approach with smaller words and more sets.
```
    stop time is          33299490000
    IPC: 0.223949
    L1 I Cache:    1259468 hits,        505 misses,    2524084 cycles,     10.194 penalty
    L2 I Cache:        305 hits,        200 misses,       3634 cycles,     15.120 penalty
    L1 D Cache:      73890 hits,         46 misses,     148641 cycles,     18.717 penalty
    L2 D Cache:          2 hits,         45 misses,        723 cycles,     15.978 penalty
    $finish at simulation time          33341460000
```

1024 wordsize, 16 sets, 8 ways *OR* 1024 wordsize, 32 sets, 4 ways
- Penalty is almost doubled and we are worse off!
- Although the 17252KB Coremark instructions finally seems to fit in the L1 I cache.
```
    stop time is          33378390000
    IPC: 0.223395
    L1 I Cache:    1269162 hits,        139 misses,    2541183 cycles,     20.568 penalty
    L2 I Cache:         36 hits,        103 misses,       2443 cycles,     23.019 penalty
    L1 D Cache:      73912 hits,         24 misses,     148481 cycles,     27.375 penalty
    L2 D Cache:          0 hits,         24 misses,        585 cycles,     24.375 penalty
    $finish at simulation time          33419590000
```


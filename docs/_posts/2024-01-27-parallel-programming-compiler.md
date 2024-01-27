---
layout: post
title:  "Parallel Programming + Compiler"
summary: "Paper review for 2 papers @ UofT"
author: moomoohorse
date: '2024-01-27 05:48:21 -0600'
category: ['parallel-programming']
thumbnail: /assets/img/posts/parallel-programming-plus-compiler.png
keywords: parallel-programming, GPU, compiler
permalink: /blog/parallelprogrammingcompiler-01
usemathjax: true22
---

# Register Tiling for Unstructured Sparsity in Neural Network Inference

## Overview of Contributions

This paper proposes Sparse Register Tiling with unroll-and-sparse-jam technique to jam the code to improve the register reuse.

Traditionally, there are register tiling methods such as 1-D register tiling and 2-D block tiling, with many implementation-wise differences. These methods are limited by their use of Compressed Sparse Row (CSR) method as a way to store the non-zero values. Using CSR methods has nice(little) storage format overhead compared to storing it as a dense matrix. However, it will require the SpMM implementation to load zeros to perform the matrix multiplication, as the positions of non-zeros are not statically known. These extra zeros loaded are noted as redundant FLOPs. This motivates this paper to explore a way to optimize the performance and storage needed on SpMM workload, by treating SpMM as dense matrix multiplication with unroll-and-sparse-jam optimization to reduce the extra storage and computing overhead introduced by additional branches and zeros to store.

## Strength and Weakness

While the old works on SpMM optimization made incremental changes to CSR-based register tiling approach, this work starts from treating SpMM as dense matrix multiplication and utilizes untroll-and-sparse-jam optimization to achieve better storage efficiency and computational overhead. This fundamentally differentiates this work to other works.

This innovative idea is backed by robust approaches to eliminate the issues arise from moving from CSR to the current storage method. The number of enumerated code blocks increase significantly when the tile size grows. To reduce the number of enumerated code blocks, a sparse-jam solver tries to find a subset of enumerated block to replace the excessive enumerated blocks. The trade-off within this mapping (sparse-jam solver) is between the size of generated merged enumerated blocks $R$ and the number of registers required to load the block, meaning if the set size of $R$ is too small, then it will degrade into dense matrix multiplication, and if the size of $R$ is too big, then instruction cache won’t fit the code generated. The strength of this method is that merging enumerated blocks can guarantee correctness and the profiling process can be done off-line and reused. However, the weakness of such method is that because the profiling result is directly related to a specific type of workload, the solver’s result relies too much on the workload used to profile. Despite the fact that the profiling sample size is huge, the nature of the profiling workload can change, which might make the optimization unstable in the long run.

To further optimize the memory usage, the data of sparse matrix is first compressed using a data compressor. The strength of this method is that it improves the spatial locality, but the run-time nature of data compression introduces additional computational overhead for a program.

## Possible extension of the work

Based on the potential in sparse-jam solver, I think different solvers with different trade-offs between $R$ size and code size can be further explored. And we can explore more options than look-up table implementation, so that we can gain more genearality as the current implementation depends on profiling too much. Currently the workload is using weight matrices in pruned transformer and ResNet50 models, I think by making more experiments on other workloads can help find more bottlenecks in this problem as this approach is workload-dependent. This is possible because this paper assumes that the data movement in SpMM is optimized for cache hierarchy, while many of the components within this work can influence the data movement for cache hierarchy. Hence we can try to lift this assumption, and look at trade-offs between memory efficiency and register tiling.

# Combining Run-time checks and compile time analysis to improve control flow auto-vectorization

## Overview of Contribution

The auto-vectorization has been explored without combining dynamic uniformity and dependence, VecRC provides a way to do compile-time and run-time optimization under dynamic uniformity. VecRC mainly contributes to the cases where control-dependent loop-carried dependence exists. This case wasn’t able to be efficiently optimized because stride length can change in run-time.

## Strength and Weakness

In compile-time analysis part, under dynamic uniformity, VecRC uses the vectorization to improve the performance when dependency exists. This consideration extends the previous auto-vectorization.

In the run-time analysis, the trade-off between scalarization and vectorization and the cost of run-time check are considered. However, this modeling is under the assumption that the branch probability is independent from other iterations. For many scenarios, it does not hold, such as when the condition is dependent on the value assignment under that condition. Additionally, the probability is obtained from Profile-Guided Optimization, which heavily relies on the similar branch patterns. The branch pattern can vary significantly for different workload for the same program or even for the same workload for the same program.

## Possible ideas

The compile-time analysis for the auto-vectorization under dynamic uniformity is very nicely explored and analysed in VecRC. Because the branch patterns and many necessary information for vectorization or scalarization are not valid at comile-time, I think exploring run-time analysis is more valuable. The branch probability can be replaced by a set of parameters learnt by ML models and we can map those parameters to a trained decision tree to select the most profitable strategy for  auto-vectorization. In other words, we can extend the retrieving execution profile from PGO to using ML to optimize the best strategy.

# Thoughts about Parallel Programming w/ Compiler

This area is very important because the applications today require more and more machine learning and cloud. ML acts as workload for the underlying architecture, hence it gives more opportunities to computer architecture. In reverse, ML also drives the development of architecture and compiler by being integrated into different parts of architectures and compilers. The same is true for cloud, which is another huge trend, to supply computing as a service rather than a product. To fit those programs into the underlying architecture, many optimization has to be done, including compile-time and run-time optimization. VecRC is a good example to showcase how to  fit a certain workload to let a program run more efficiently. Sparse Register Tiling is also a very nice example to see the exploration and benefits of exploiting SpMM under ML workload.
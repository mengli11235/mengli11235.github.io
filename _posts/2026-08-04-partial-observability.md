---
layout: post
title: "What Should a Representation Remember When the World Is Partially Observable?"
subtitle: "Partial observability turns representation learning from image compression into an inference problem."
date: 2026-08-04 10:00:00 +0200
reading_time: 6
tags: [Reinforcement learning, Partial observability, State representation]
---
Most reinforcement-learning benchmarks present an agent with observations, not states. A frame tells the agent what is visible now; it may not reveal velocity, hidden objects, delayed consequences, or the event that occurred one moment earlier.

That distinction changes the representation-learning problem. In a fully observable setting, a compact encoding of the current frame may be sufficient. In a partially observable setting, a useful representation must help infer the latent state from incomplete evidence.

## The hidden variable behind the image

Consider a ball moving across a screen. One image provides position but not direction. Two nearby frames reveal motion. The task-relevant variable is therefore not contained in a single observation; it must be inferred from temporal context.

This is why partial observability is not just an augmentation problem. Randomly masking pixels can improve robustness, but it does not by itself specify what the representation should remember across time.

## Learning from temporal relationships

Our work extends a spatiotemporal contrastive representation-learning framework for partially observable Atari environments. The learning signal asks the encoder to preserve information that remains predictive across local space and time.

The central design intuition is that **a representation should encode the latent causes that make neighboring observations coherent**. When a current image is ambiguous, temporal relationships provide evidence about motion, persistence, and event history.

## Evaluation must probe latent factors

A representation can achieve a low training loss while failing to expose the variables an agent needs. We therefore evaluate learned features through annotated factors in the Atari-based benchmark rather than relying only on reconstruction quality.

The reported experiments show substantial gains over the supervised comparison in the partially observable setting. More importantly, they demonstrate that self-supervision can exploit temporal structure that is not made explicit by frame-level labels.

## A general lesson

For robotics, health monitoring, and neural data, the same issue appears in different forms. A sensor snapshot is incomplete; the underlying condition is distributed across time, channels, or modalities. Good representations must therefore act as **compact inference states**, not merely compressed observations.

## References

- [Unsupervised Representation Learning in Partially Observable Atari Games](https://arxiv.org/abs/2303.07437)
- [Related code repository](https://github.com/mengli11235/MST_DIM)

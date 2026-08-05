---
layout: post
title: "The Unbalanced Atlas: Why Representation Spaces Need More Than One Local View"
subtitle: "An intuitive account of our ICLR 2024 work on manifold-aware self-supervised state representation learning."
date: 2024-05-01 09:00:00 +0200
reading_time: 7
tags: [Self-supervised learning, Manifolds, ICLR 2024]
---
Representation learning asks a deceptively simple question: **what should a model keep, and what should it discard?** In reinforcement learning, the answer matters because an agent rarely needs a photorealistic reconstruction of every observation. It needs a representation that exposes the factors useful for prediction and control.

A common starting point is the manifold hypothesis: high-dimensional observations often vary along a lower-dimensional structure. A game frame may contain tens of thousands of pixels, while the task-relevant state is governed by a much smaller set of factors—positions, velocities, object identities, and events.

## One chart is often not enough

In differential geometry, an *atlas* describes a complicated space through multiple local coordinate systems, or charts. This analogy is useful for representation learning. A single globally uniform embedding may be an awkward fit when different parts of the data have different local complexity.

Our work introduces an **unbalanced atlas**: instead of giving every local region the same representational capacity, the model can allocate capacity unevenly. The design is deliberately asymmetric. Regions that need more expressive coordinates can use them, while simpler regions are not forced into the same template.

## From an idea to DIM-UA

We integrated this principle into Spatiotemporal DeepInfomax, producing **DIM-UA**. The method keeps the self-supervised signal grounded in temporal and local relationships while changing the geometry of the target representation.

The important point is not merely that the embedding is “manifold-based.” The learning objective and the representation geometry are designed together. As the target dimensionality increases, the unbalanced atlas continues to use that capacity effectively rather than treating extra dimensions as undifferentiated storage.

## What the experiments show

We evaluated the method on the Atari Annotated RAM Interface benchmark, where learned representations are tested against annotated latent factors. At 16,384 hidden units, DIM-UA reached an average F1 score of roughly 75%, compared with roughly 70% for ST-DIM in the reported setting.

This result supports a broader lesson: **larger representations are not automatically better; their geometry determines whether additional capacity becomes useful structure or redundant freedom.**

## Why this matters beyond Atari

The unbalanced-atlas idea is relevant whenever data contains heterogeneous local structure. Examples include robotic observations, medical images, neural signals, and multimodal records. In each case, the intrinsic complexity may vary across regions, subjects, channels, or conditions.

The larger research direction is therefore not “find one perfect embedding.” It is to develop representation spaces that adapt to the structure of the data while remaining trainable with modern self-supervised objectives.

## References

- [State Representation Learning Using an Unbalanced Atlas — OpenReview](https://openreview.net/forum?id=cWdAYDLmPa)
- [arXiv version](https://arxiv.org/abs/2305.10267)
- [Code: DIM-UA](https://github.com/mengli11235/DIM-UA)

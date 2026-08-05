---
layout: post
title: "Exploration Needs Disagreement: Noise, Priors, and Bootstrapped DQN"
subtitle: "Why ensemble diversity is not a cosmetic property but a mechanism for deep exploration."
date: 2026-08-05 09:00:00 +0200
reading_time: 6
tags: [Deep reinforcement learning, Exploration, DQN]
---
Exploration is often described as choosing a random action occasionally. That works for local uncertainty, but it is weak when useful behavior requires a long sequence of coordinated choices.

Bootstrapped DQN offers a different perspective. Multiple value-function heads are trained in parallel, and each head can represent a distinct plausible estimate of the environment. Acting according to one sampled head produces temporally extended behavior: the agent follows a coherent hypothesis rather than injecting independent randomness at every step.

## Diversity is the engine

The mechanism only works when the heads remain meaningfully different. If every head converges to nearly the same value function, the ensemble becomes computationally expensive duplication.

Randomized prior functions were introduced to preserve differences between heads. Our work asks whether fixed priors are the only way to achieve this goal. We replace the priors with Gaussian noise and examine whether stochastic variation can sustain useful diversity.

## Why noise can help

A fixed prior establishes a persistent bias. Noise instead creates continuing perturbations during learning. The objective is not to make predictions arbitrarily unstable; it is to prevent premature collapse to one shared estimate before the agent has collected enough evidence.

This highlights an important distinction:

- **Unstructured action noise** changes what the agent does at one moment.
- **Value-function diversity** changes the agent’s belief about which long-term strategy may be promising.

The second form is better suited to deep exploration because it can influence a sequence of actions consistently.

## What we observed

Across the reported Atari experiments, replacing priors with noise improved the evaluation performance of Bootstrapped DQN relative to the compared variants. The findings support the interpretation that maintaining ensemble diversity is central to the algorithm rather than an incidental side effect.

## Broader implications

The same principle appears in uncertainty estimation, active learning, and scientific modeling: a useful ensemble should preserve multiple plausible explanations until evidence justifies convergence. Diversity is valuable when it is structured, consequential, and connected to decision-making.

## References

- [Improving the Diversity of Bootstrapped DQN by Replacing Priors With Noise](https://arxiv.org/abs/2203.01004)
- [Code repository](https://github.com/mengli11235/Bootstrapped-DQN-with-NP)

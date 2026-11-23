---
layout: post
title: "A copy of the measurements is hard to beat"
subtitle: "Our Virtual Cell Challenge 2026 entry finished 41st of 807. Most of its score came from moving measured effects onto new cell lines with care. The winners did the same, with far more data and more learning."
date: 2026-11-23 18:00:00 +0100
reading_time: 9
tags: [Perturbation prediction, Single-cell, Foundation models, Virtual Cell Challenge]
description: What Team UiO learned from the Virtual Cell Challenge 2026, where effects measured in public screens beat perturbation models on unseen cell lines.
---
In October the Arc Institute posed a question that sounds like the definition of a virtual cell. Take a human cell line that has never been perturbed in the lab. You are given its control cells, 18,400 of them, and nothing else about it. Now predict what happens to it when each of 300 genes is knocked down with CRISPRi, as 400 single cells per knockdown. Three such lines made 360,000 cells to generate. An evaluator, cell-eval2, scored them on six metrics, each scaled so that 0 is the line's mean and 1 is an independent replicate of the experiment.

We entered as Team UiO on 13 October and submitted our final entry on 5 November. It finished 41st of 807 on the final leaderboard, with a score of 0.2594. This note is about what got us there, which was less a model than a way of handling measurements, and about what the winners did that we did not. The full account, with every component attributed to whoever built it, is in [the paper on the project page]({{ '/vcc2026/' | relative_url }}).

## The baseline that would not lose

The first thing we tried was the obvious one, a model trained to predict perturbation responses. It did badly. On our first local fold, copying the measured effects of the same knockdowns in another cell line, HEK293T, scored 0.286. Stack, a model built for this kind of prediction, scored −0.012 zero-shot and −0.049 after fine-tuning. State's perturbation model, run zero-shot, landed about 0.39 below the plain mean of the measured tables.

The reason is not mysterious once you look at the data. A knockdown that has been measured in other cell lines is a strong prior for a new one, and by the organisers' count all but one of the 300 test targets had been measured somewhere. A model has to beat that prior, not zero. So we built on measurements, and every learned part had to prove itself against them.

## A skeleton we did not build

The skeleton came from AtlasShift, a public baseline under the MIT licence. It takes per-knockdown effects from public screens, moves them onto each new line's own control cells, and draws cells to match with a count generator. Adopting its generator was our largest single jump on the validation board, from 0.078 to 0.182, and it is not our work. The paper says so in a table, and we think every challenge write-up should have one.

What we added sits between its profile step and its generator. Effects came from five screens: K562 genome-wide, HCT116 and HEK293T, the 2025 challenge's H1 cells, and KOLF2.1J. We shrank each source by its own sampling noise, with an adaptive-shrinkage prior fitted per expression decile, and fused the sources by direction so that each had the same say. We removed the top 15 axes of variation in the new line's control cells from every predicted change, an idea we took from other teams' notes on the board. And because the K562 screen measures only 7,681 genes, we filled in the rest with a regression on the new line's control axes. In our folds 47% of the truth's energy lay on those missing genes.

On top of the tables sit residual heads, TabPFN regressors on frozen embeddings from 16 single-cell foundation models. They are only allowed to amplify changes the table already makes, never to add a new direction. A call list then lifts genes that sit just past a per-gene detection line, in the direction of a pooled posterior. Two external predictors, UPM and PIE, contribute direction only, with their weights read on cell lines that neither they nor our sources had seen.

## Filling to the kink

The most unusual step is the last one, and it comes from the metric rather than the biology. cell-eval2's mse term gives each prediction a sampling correction, capped by a budget equal to the prediction's own spread across knockdowns. The evaluator's documentation notes a consequence. Below the cap, putting more energy along the predicted direction costs nothing in the distance, and only the alignment with the truth counts. Past the cap, the usual quadratic cost returns.

In a toy model with a single direction, this means a weakly aligned prediction should be scaled up exactly to the kink. Our fill rule estimates the budget-to-claim ratio from the submission alone, using the evaluator's own functions, and scales each line toward a ratio of 1.04. An earlier package of ours sat at about 0.72, well below the kink, and was leaving score on the table for no reason. This step has no biological meaning. It is calibration to an evaluator, and we say so.

## How much the foundation models did

We counted, step by step, what each change added and whether it touched a foundation model. Foundation models gave about a tenth of our improvement. Most of that tenth sits at the two ends of the project, in the first residual heads and in the external tables of the final entry, and the latter are estimates rather than measurements.

Two readings make the number less flattering than it looks. On the package of 27 October, removing the whole residual head changed the score by −0.0003, not separable from zero. And a head of the same form without the single-cell embeddings, still with a TabPFN regressor and protein features, added as much as the head with them. Without that control we would have credited the embeddings.

This is not a verdict on foundation models in general. It says what they added on top of careful measurements, in a setting with three unseen lines and a fixed evaluator.

## The result, and a forecast that was too high

Our best validation upload scored 0.1882, rank 347 of 1,635 on the frozen board. On the final leaderboard, scored on three other lines, the entry reached 0.2594 and ranked 41st. Thirteen other entries lie within 0.004 of ours, and the organisers report that redrawing an entry's cells moved its score by up to 0.004, so our rank is really one of a band from 33 to 46.

Our local folds had forecast about 0.32. That forecast rested on a single pair of local and board scores, made on the validation lines, and on folds reused for hundreds of comparisons. We cannot separate those causes from each other or from the change of cell lines. The shortfall sits in mse, nmae and reach, not in pds.

## What the winners did

The organisers' wrap-up describes the three winning entries, at 0.4399, 0.3348 and 0.3263. All three share our structure. Each estimates a knockdown's effect from measured responses in other cell types, adapts the estimate to the new line through its control cells, and generates the cells. Their differences from ours are in degree, and the degree is large.

The first-place entry, from Illumina, added a large cell atlas and weighted each reference per gene and knockdown, from how similar its controls are to the new line, its noise and the knockdown's efficiency. The second-place entry learned its response model from 222 datasets in 86 cellular contexts, trained with whole contexts held out, and used no pretrained model. The third, from Xaira, trained a diffusion model on more than 37 million Perturb-seq cells and then did not submit its raw output. It used the model to decide, gene by gene, how much of each measured effect to carry over. The only foundation model on the podium was used to select and scale measurements.

The organisers concluded that reference data and the care of its transfer counted at least as much as architecture. Our own accounting points the same way.

## How we judged data

Looking back, the gaps between our entry and the winners have one root, and it is the way we tested public data. After AtlasShift's generator had lifted our score, every new public table was tested as one more source of a fixed average, or one more axis of the call list, against the current entry on our three folds. One table moves an average very little. Each read a few thousandths, often inside the spread of its permuted control, and was dropped. We judged about 30 tables this way and kept none.

That test measures what a table adds to a fixed average. It does not measure what a model trained across all of them could learn, where every table is one more training context and their number is what counts. We also picked tables by how many test targets they covered, which made sense for a source and none for a training context. What a model learns from a training context is how an effect moves from one line to another, and for that the test targets do not need to be in it. The question of why the remaining data were not used together was raised twice inside the team, on 3 and 4 November. Our answer stayed inside the fixed pipeline.

## Lessons

We take three. First, test data the way it will be used. Data meant for a model should go in as a batch with whole contexts held out, so that the reading is of the model and not of one table. Second, a model earns credit only against a control of the same form, which is how we found that the embeddings in our heads were not doing what we thought. Third, asking why a model predicts what it does can yield a method that outlives the model. PIE's detection probabilities led us to the call floor, which stayed in the entry after PIE's own directions had been replaced.

If we did it again, the first place we would look is the size of each predicted change. The mse term carries 37% of our distance to first place, and our sizes came from rules, one gain per line and a fill computed from the metric. Both the first- and third-place entries learned or calibrated sizes per gene. None of this was run, so it is a guess from the comparison and not a measurement.

The paper, the timeline and the charts are on the [project page]({{ '/vcc2026/' | relative_url }}). The [paper itself]({{ '/assets/papers/vcc2026-li-meng-team-uio.pdf' | relative_url }}) lists every component with its owner and licence, and the code is on [GitHub](https://github.com/mengli11235/vcc2026).

#!/bin/bash

experiment_name="vampire-bats-6"
experiment_dir="azure-ai-studio-ft/dataset/${experiment_name}-files"

dataset_path_ft_eval="${experiment_dir}/${experiment_name}-ft.eval.small.jsonl"
dataset_path_ft_eval_score="${experiment_dir}/${experiment_name}-ft.eval.small.score.jsonl"

python pfeval.py \
    --input $dataset_path_ft_eval \
    --output $dataset_path_ft_eval_score

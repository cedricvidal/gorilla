set -a # automatically export all variables
source ../.env
set +a

experiment_name="vampire-bats-6"
experiment_dir="dataset/${experiment_name}-files"
dataset_path_hf_eval="${experiment_dir}/${experiment_name}-hf.eval.jsonl"
dataset_path_hf_eval_answer="${experiment_dir}/${experiment_name}-hf.eval.answer.jsonl"

unset AZURE_OPENAI_ENDPOINT
unset AZURE_OPENAI_API_KEY
unset OPENAI_API_VERSION
export OPENAI_BASE_URL=$EVAL_OPENAI_BASE_URL_FT
export OPENAI_API_KEY=$EVAL_OPENAI_API_KEY_FT

echo "OPENAI_BASE_URL=${OPENAI_BASE_URL}"

python ../eval.py \
    --question-file $dataset_path_hf_eval \
    --answer-file $dataset_path_hf_eval_answer \
    --model $EVAL_OPENAI_DEPLOYMENT_BASE \
    --workers 1

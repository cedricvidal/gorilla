doc_path="sample_data/vampire-bats/"
ds_path="azure-ai-studio-ft/dataset/vampire-bats-7"

python3 raft.py \
    --datapath $doc_path \
    --output $ds_path \
    --distractors 3 \
    --doctype pdf \
    --chunk_size 512 \
    --questions 10 \
    --workers 1 \
    --system-prompt-key llama \
    --completion_model llama3-70b \
    --embedding_model text-embedding-ada-002

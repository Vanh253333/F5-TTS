#!/usr/bin/env bash

# Thiết lập GPU sử dụng
export CUDA_VISIBLE_DEVICES=0 

log() {
    echo "$@"
}

DATASET_DIR="data/vivoice"
EXP_NAME="F5TTS_v1_Base"
DATASET_NAME="vivoice"
BATCH_SIZE=1600
NUM_WOKERS=8
WARMUP_UPDATES=40000
SAVE_UPDATES=10000
LAST_UPDATES=10000
PRETRAIN_CKPT="ckpts/your_training_dataset/pretrained_model_1200000.pt"

stage=5
stop_stage=5

if [ $stage -le 4 ] && [ $stop_stage -ge 4 ]; then
    log "Feature extraction ... "
    python src/f5_tts/train/datasets/prepare_vivoice.py "$DATASET_DIR" "$DATASET_DIR" --workers "$NUM_WOKERS"
fi

# Chạy quá trình fine-tuning
if [ $stage -le 5 ] && [ $stop_stage -ge 5 ]; then
    log "Start fine-tuning F5-TTS with your dataset ... "
    python src/f5_tts/train/finetune_cli.py \
        --exp_name "$EXP_NAME" \
        --dataset_name "$DATASET_NAME" \
        --batch_size_per_gpu "$BATCH_SIZE" \
        --num_warmup_updates "$WARMUP_UPDATES" \
        --save_per_updates "$SAVE_UPDATES" \
        --last_per_updates "$LAST_UPDATES" \
        --finetune \
        --pretrain "$PRETRAIN_CKPT"
fi

log "Fine-tuning F5-TTS done."
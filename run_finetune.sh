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
# Bản .safetensors  load_checkpoint bị lỗi safetensorerror: error while deserializing header: headertoolarge, nên dùng bản .pt cũ
PRETRAIN_CKPT="ckpts/vivoice/pretrained_model_1250000.safetensors"


stage=1
stop_stage=1

if [ $stage -le 0 ] && [ $stop_stage -ge 0 ]; then
    log "Normalize text and save to metadata.csv ... "
    python prepare_metadata.py 
fi

if [ $stage -le 1 ] && [ $stop_stage -ge 1 ]; then
    log "Feature extraction ... "
    python src/f5_tts/train/datasets/prepare_vivoice.py "$DATASET_DIR" "$DATASET_DIR" --workers "$NUM_WOKERS"
fi

# Mở rộng embedding của mô hình pretrained để hỗ trợ bộ từ vựng mới
if [ $stage -le 2 ] && [ $stop_stage -ge 2 ]; then
    log "Extend embedding pretrained with new vocab ... "
    python extend_embedding_vocab.py
fi

# Chạy quá trình fine-tuning
if [ $stage -le 3 ] && [ $stop_stage -ge 3 ]; then
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
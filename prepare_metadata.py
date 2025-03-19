"""
Chuẩn hóa lại text và lưu thông tin vào file metadata.csv dưới dạng audio_file|text
"""

from vinorm import TTSnorm
import re
import pandas as pd
import os
import csv

def custom_TTSnorm(text, punc=False, lower=True):
    # Tìm tất cả các từ có dấu nháy đơn
    words_with_apostrophe = re.findall(r"\b\w+'\w+\b", text)

    # Chuẩn hóa văn bản bằng TTSnorm
    normalized_text = TTSnorm(text, punc=punc, lower=lower)

    # Thay thế các từ đã được chuẩn hóa bằng từ gốc (có dấu nháy đơn)
    for word in words_with_apostrophe:
        normalized_word = word.replace("'", " ")
        if normalized_word in normalized_text:
            normalized_text = normalized_text.replace(normalized_word, word)

    # Khôi phục dấu câu liền kề với từ
    def restore_punctuation(match):
        return match.group(1) + match.group(2)

    normalized_text = re.sub(r"(\w+)\s+([.,!?;:])", restore_punctuation, normalized_text)
    # loại bỏ 2 dấu chấm câu liền kề
    eol = -1
    for i,p in reversed(list(enumerate(normalized_text))):
        if p not in ["..",""," ",".","  "]:
            eol = i
            break
    normalized_text = normalized_text[:eol+1] + "." 

    return normalized_text

def process_csv_and_apply_norm(input_csv, output_csv, custom_TTSnorm):

    results = []
    count = 0
    header_written = False  # Biến để kiểm tra xem tiêu đề đã được ghi chưa

    with open(input_csv, 'r', encoding='utf-8') as infile:
        reader = csv.DictReader(infile)
        for row in reader:
            audio_file = row['file_wav_name']  # Lấy tên file wav
            text = row['text']
            normalized_text = custom_TTSnorm(text)  # Áp dụng hàm chuẩn hóa

            results.append(f"wavs/{audio_file}|{normalized_text}")
            count += 1

            if count % 10000 == 0:
                _save_results(results, output_csv, header_written)
                results = []  # Reset danh sách kết quả
                header_written = True # đánh dấu là đã ghi header rồi

        # Lưu lại phần dư (nếu có)
        _save_results(results, output_csv, header_written)


def _save_results(results, output_csv, header_written):
    """
    Lưu danh sách kết quả vào file CSV đầu ra.
    """
    mode = 'a' if os.path.exists(output_csv) else 'w'
    with open(output_csv, mode, encoding='utf-8') as outfile:
        if mode == 'w' or not header_written:
          outfile.write("audio_file|text\n")
        outfile.write('\n'.join(results) + '\n') 

if __name__ == "__main__":
    input_csv = "data/vivoice/vivoice_infor.csv" # thay đổi đường dẫn đến file csv chứa thông tin ban đầu
    output_csv = "data/vivoice/metadata.csv" 

    process_csv_and_apply_norm(input_csv, output_csv, custom_TTSnorm)
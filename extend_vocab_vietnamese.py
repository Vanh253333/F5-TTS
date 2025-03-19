# Vietnamese character list
vietnamese_characters = [
    'a', 'á', 'à', 'ả', 'ã', 'ạ', 'ă', 'ắ', 'ằ', 'ẳ', 'ẵ', 'ặ', 'â', 'ấ', 'ầ', 'ẩ', 'ẫ', 'ậ',
    'b', 'c', 'd', 'đ',
    'e', 'é', 'è', 'ẻ', 'ẽ', 'ẹ', 'ê', 'ế', 'ề', 'ể', 'ễ', 'ệ',
    'g', 'h',
    'i', 'í', 'ì', 'ỉ', 'ĩ', 'ị',
    'k', 'l', 'm', 'n',
    'o', 'ó', 'ò', 'ỏ', 'õ', 'ọ', 'ô', 'ố', 'ồ', 'ổ', 'ỗ', 'ộ', 'ơ', 'ớ', 'ờ', 'ở', 'ỡ', 'ợ',
    'p', 'q', 'r', 's', 't',
    'u', 'ú', 'ù', 'ủ', 'ũ', 'ụ', 'ư', 'ứ', 'ừ', 'ử', 'ữ', 'ự',
    'v', 'x', 'y', 'ý', 'ỳ', 'ỷ', 'ỹ', 'ỵ',
    'A', 'Á', 'À', 'Ả', 'Ã', 'Ạ', 'Ă', 'Ắ', 'Ằ', 'Ẳ', 'Ẵ', 'Ặ', 'Â', 'Ấ', 'Ầ', 'Ẩ', 'Ẫ', 'Ậ',
    'B', 'C', 'D', 'Đ',
    'E', 'É', 'È', 'Ẻ', 'Ẽ', 'Ẹ', 'Ê', 'Ế', 'Ề', 'Ể', 'Ễ', 'Ệ',
    'G', 'H',
    'I', 'Í', 'Ì', 'Ỉ', 'Ĩ', 'Ị',
    'K', 'L', 'M', 'N',
    'O', 'Ó', 'Ò', 'Ỏ', 'Õ', 'Ọ', 'Ô', 'Ố', 'Ồ', 'Ổ', 'Ỗ', 'Ộ', 'Ơ', 'Ớ', 'Ờ', 'Ở', 'Ỡ', 'Ợ',
    'P', 'Q', 'R', 'S', 'T',
    'U', 'Ú', 'Ù', 'Ủ', 'Ũ', 'Ụ', 'Ư', 'Ứ', 'Ừ', 'Ử', 'Ữ', 'Ự',
    'V', 'X', 'Y', 'Ý', 'Ỳ', 'Ỷ', 'Ỹ', 'Ỵ'
]

def check_and_add_vietnamese_characters(file_old, file_new):
    """
    Checks if a file contains all Vietnamese characters and adds missing ones if necessary.

    Args:
        file_name: The name of the file to check.
    """
    try:
        with open(file_old, 'r') as f:
            file_content = f.read()

        existing_characters = set(file_content.splitlines())
        characters_to_add = [char for char in vietnamese_characters if char not in existing_characters]

        if characters_to_add:
            with open(file_new, 'a') as f:
                f.write('\n'.join(characters_to_add))
            print(f"Added missing Vietnamese characters to file '{file_new}'.")
        else:
            print(f"File '{file_old}' already contains all Vietnamese characters.")

    except FileNotFoundError:
        print(f"Error: File '{file_old}' not found.")
    except Exception as e:
        print(f"Error: An error occurred during processing: {e}")

if __name__ == "__main__":
    check_and_add_vietnamese_characters("data/Emilia_ZH_EN_pinyin/vocab.txt", "data/vivoice_char/vocab.txt")
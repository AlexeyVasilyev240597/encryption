from pathlib import Path
import sys

def get_begining(full_file_name: Path, key_len) -> str:
    file     = open(full_file_name, 'rb')
    begin_str = file.read(key_len)        
    file.close()
    return begin_str

def get_key(block_1: str, block_2: str) -> str:    
    key = bytes(a ^ b for a, b in zip(block_1, block_2))
    return key

if __name__ == '__main__':
    args = sys.argv[1:]
    if len(args) == 4:
        key_len = int(args[0])
        path_to_files = args[1]
        block_1 = get_begining(path_to_files / Path(args[2]), key_len)
        block_2 = get_begining(path_to_files / Path(args[3]), key_len)
        key = get_key(block_1, block_2)
        print(key)
    else:
        print("1 arg: approximate key length")
        print("2 arg: path to working directory")
        print("3 arg: encrypted file name")
        print("4 arg: original file name")
    

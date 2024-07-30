from pathlib import Path


def get_begining(full_file_name: Path, key_len) -> str:
    file     = open(full_file_name, 'rb')
    begin_str = file.read(key_len)        
    file.close()
    return begin_str

def get_key(block_1: str, block_2: str) -> str:    
    key = bytes(a ^ b for a, b in zip(block_1, block_2))
    return key

key_len = 40
path_to_files = Path('C:/Users/valex/Documents/fun')
block_1 = get_begining(path_to_files / Path('3JUS8n_BP'), key_len)
block_2 = get_begining(path_to_files / Path('smile.gif'), key_len)
key = get_key(block_1, block_2)
print(key)

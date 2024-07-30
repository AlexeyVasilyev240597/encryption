import re

from pathlib import Path
from transliterate import translit

alphabet = (list(map(chr, range(ord('A'), ord('Z')+1))) +
            list(map(chr, range(ord('a'), ord('z')+1))) +
            list(map(chr, range(ord('0'), ord('9')+1))) +
            ['_', '-', '.']) 
            # ['(', ')', '_', '-', ',', '.', '*', ' '])

def has_cyrillic(text):
    return bool(re.search('[а-яА-Я]', text))

def validate_var(key: str, var_name: str) -> bool:
    if has_cyrillic(key):
        key = translit(key, 'ru', reversed=True)
        print(f'The key is transformed into: {key}\n')
    for c in key:
        if not c in alphabet:
            if c == ' ':
                c = 'space'
            print(f'ERROR: {var_name} has unsupported characters as {c}')
            return False
    else:
        return True

def is_file_format_correct(full_file_name: str) -> bool:
    try:
        full_file_name = Path(full_file_name)
    except:
        return False
    if not full_file_name.exists():
        print(f'ERROR: not fourd {full_file_name}')
        return False
    file_name = str(full_file_name.name)
    if not validate_var(file_name, 'file name'):
        return False
    return True

# Caesar cipher
def crypt_name(file_name: str, key:str, mode: str) -> str:
    if mode == 'en':
        shift_dir = 1
    elif mode == 'de':
        shift_dir = -1
    N_a = len(alphabet)
    N_k = len(key)
    
    new_file_name = list(file_name)
    for i in range(len(new_file_name)):
        cur_pos = alphabet.index(new_file_name[i])
        new_file_name[i] = alphabet[(cur_pos + 
                                     shift_dir*ord(key[i % N_k])) 
                                    % N_a]
    new_file_name = "".join([str(c) for c in new_file_name])
    
    return new_file_name

# XOR cipher
def crypt_content(path_to_files: Path, file_name: Path, 
                  new_file_name: Path, key: str) -> None:
    N_k = len(key)
    file     = open(path_to_files / file_name,     'rb')
    new_file = open(path_to_files / new_file_name, 'wb')
    
    key = bytes(key, 'utf-8')
    while (block_in := file.read(N_k)):
        block_out = bytes(a ^ b for a, b in zip(block_in, key))
        new_file.write(block_out)
    
    file.close()
    new_file.close()

def crypt_file(full_file_name: str, mode: str) -> None:    
    print('Put the key:')
    while validate_var(key := input(), 'key') == False:
        pass
    
    file_name = full_file_name.name
    new_file_name = Path(crypt_name(file_name, key, mode))
    print(new_file_name)
    crypt_content(full_file_name.parent, file_name, new_file_name, key)
    
if __name__ == '__main__':
    print('Put the file name')
    while is_file_format_correct(file_name := input()) == False:
        pass
    
    print('Put mode: en to encrypt, de to decrypt')
    is_mode_correct = lambda mode: True if mode == 'en' or mode == 'de' else False
    while is_mode_correct(mode := input()) == False:
        print('Wrong input')
    
    crypt_file(Path(file_name), mode)
    
    print('Done')
    

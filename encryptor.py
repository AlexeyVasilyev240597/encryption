import sys
from pathlib import Path

alphabet = (list(map(chr, range(ord('A'), ord('Z')+1))) +
            list(map(chr, range(ord('a'), ord('z')+1))) +
            list(map(chr, range(ord('0'), ord('9')+1))) +
            ['_', '-', '.'])
            # ['(', ')', '_', '-', ',', '.', '*', ' '])

def validate_var(key: str, var_name: str) -> bool:
    for c in key:
        if not c in alphabet:
            if c == ' ':
                c = 'space'
            print(f'ERROR: {var_name} has unsupported characters as {c}')
            return False
    else:
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
    print('Done')

def crypt_file(full_file_name: str, mode: str) -> None:
    full_file_name = Path(full_file_name)
    if not full_file_name.exists():
        print(f'ERROR: not fourd {full_file_name}')
        return
    file_name = str(full_file_name.name)
    if not validate_var(file_name, 'file name'):
        return    
    
    print('Put the key:')
    key = input()
    if not validate_var(key, 'key'):
        return
    
    new_file_name = crypt_name(file_name, key, mode)
    new_file_name = Path(new_file_name)
    crypt_content(full_file_name.parent, file_name, new_file_name, key)
    
if __name__ == '__main__':
    args = sys.argv[1:]
    help_message = 'Put the file name and mode: en to encrypt, de to decrypt'
    if len(args) == 2:
        if args[1] == 'en' or args[1] == 'de':
            crypt_file(args[0], args[1])
        else:
            print(help_message)
    else:
        print(help_message)

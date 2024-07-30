from enum import IntEnum
import re

from pathlib import Path
from transliterate import translit

class Mode(IntEnum):
    ENCRYPT = 1,
    DECRYPT = -1

MIN_KEY_LEN = {'FILE_NAME': 6, 'CONTENT': 15}

alphabet = (
        list(map(chr, range(ord('A'), ord('Z')+1))) +
        list(map(chr, range(ord('a'), ord('z')+1))) +
        list(map(chr, range(ord('0'), ord('9')+1))) +
        ['_', '-', '.']) 

class InputEditor:
    def fix_key(key: str) -> str:
        new_key = key
        if bool(re.search('[а-яА-Я]', key)):
            new_key = translit(key, 'ru', reversed=True)
        new_key = list(new_key)
        for i in range(len(new_key)):
            c = new_key[i]
            if not c in alphabet:
                if c == ' ':
                    new_key[i] = '_'
                else:
                    new_key[i] = '-'
        new_key = "".join(new_key)
        if not new_key == key:
            print(f'The key is transformed into: {new_key}\n')
        return new_key

    def is_file_name_correct(full_file_name: str) -> bool:
        try:
            full_file_name = Path(full_file_name)
        except:
            return False
        if not full_file_name.exists():
            print(f'ERROR: not fourd {full_file_name}')
            return False
        new_file_name = Path(InputEditor.fix_key(str(full_file_name.name)))
        full_file_name.rename(Path(full_file_name.parent / new_file_name))
        return True


class Encryptor:    
    def __init__(self, mode: Mode) -> None:
        self.mode = mode

    # Caesar cipher
    def crypt_name(self, file_name: str, key: str) -> str:
        shift_dir = self.mode.value
        N_a = len(alphabet)
        N_k = len(key)

        new_file_name = list(file_name)
        for i in range(len(new_file_name)):
            cur_pos = alphabet.index(new_file_name[i])
            new_file_name[i] = alphabet[(cur_pos + shift_dir*ord(key[i % N_k])) % N_a]
        new_file_name = "".join([str(c) for c in new_file_name])

        return new_file_name
    
    # XOR cipher
    def crypt_content(seflf, path_to_files: Path, file_name: Path, 
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

    def crypt_file(self, full_file_name: str) -> None:    
        print('Put the key for file name:')
        while len(key := InputEditor.fix_key(input())) < MIN_KEY_LEN['FILE_NAME']:
            print('The key is too short, use another one')
            pass

        file_name = full_file_name.name
        new_file_name = Path(self.crypt_name(file_name, key))
        print(new_file_name)
        print('Put the key for file content:')
        while len(key := InputEditor.fix_key(input())) < MIN_KEY_LEN['CONTENT']:
            print('The key is too short, use another one')
            pass
        self.crypt_content(full_file_name.parent, file_name, new_file_name, key)
    

    
if __name__ == '__main__':
    print('Put the file name')
    while not InputEditor.is_file_name_correct(file_name := input()):
        pass

    print('Put mode: en to encrypt, de to decrypt')
    is_mode_correct = lambda mode: True if mode == 'en' or mode == 'de' else False
    while not is_mode_correct(mode := input()):
        print('Wrong input')
    mode = Mode.ENCRYPT if mode == 'en' else Mode.DECRYPT
    coder = Encryptor(mode)
    coder.crypt_file(Path(file_name))

    print('Done')
    

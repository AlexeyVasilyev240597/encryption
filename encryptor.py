
from enum import IntEnum
from pathlib import Path

class Mode(IntEnum):
    # ENCRYPT = 1,
    # DECRYPT = -1
    EN =  1,
    DE = -1

MIN_KEY_LEN = {'FILE_NAME': 6, 'CONTENT': 15}

alphabet = (
        list(map(chr, range(ord('0'), ord('9')+1))) +
        list(map(chr, range(ord('A'), ord('Z')+1))) +
        list(map(chr, range(ord('a'), ord('z')+1))) +
        ['-', '.', '_']) 

class Encryptor:
    # Caesar cipher
    def crypt_name(file_name: str, mode: Mode, key: str) -> str:
        shift_dir = mode.value
        N_a = len(alphabet)
        N_k = len(key)

        new_file_name = list(file_name)
        for i in range(len(new_file_name)):
            cur_pos = alphabet.index(new_file_name[i])
            new_file_name[i] = alphabet[(cur_pos + shift_dir*ord(key[i % N_k])) % N_a]
        new_file_name = "".join([str(c) for c in new_file_name])

        return new_file_name
    
    # XOR cipher
    def crypt_content(path_to_files: str, file_name: str, 
                      new_file_name: str, key: str) -> None:
        file     = open(path_to_files + '/' + file_name,     'rb')
        new_file = open(path_to_files + '/' + new_file_name, 'wb')

        file_size = Path(path_to_files + '/' + file_name).stat().st_size
        repeat_num = min(2**20 // len(key), file_size)
        key = key * repeat_num
        key = bytes(key, 'utf-8')
        N_k = len(key)
        while (block_in := file.read(N_k)):
            block_out = bytes(a ^ b for a, b in zip(block_in, key))
            new_file.write(block_out)

        file.close()
        new_file.close()

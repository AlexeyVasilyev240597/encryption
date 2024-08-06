import glob
import os

from encryptor import Mode, Encryptor

class FileManager:
    def __init__(self) -> None:
        self.working_dir = ''
    
    def set_working_dir(self, working_dir: str):
        self.working_dir = working_dir
        self._list_of_files()
        
    def set_files_to_crypt(self, files, mode):
        self.mode = mode
        files = [file.split('/')[-1] for file in files]
        indices_of_chosen = []
        for i in range(len(self.files_names)):
            if self.files_names[i] in files:
                indices_of_chosen.append(i)
        print(indices_of_chosen)
        if not len(indices_of_chosen) == len(files):
            print('WARNING: not all chosen files were found')
        else:
            self.files_names = [self.files_names[index] for index in indices_of_chosen]
            print(self.files_names)
            self.new_files_names[mode] = [self.new_files_names[mode][index] for index in indices_of_chosen]
            print(self.new_files_names[mode])
            
    def _list_of_files(self) -> str:
        if not self.working_dir:
            return 'ERROR: The working dir is not set'
        self.files_names = glob.glob(str(self.working_dir) + os.sep + '*')
        self.files_names = [fn.split(os.sep)[-1] for fn in self.files_names]
        if len(self.files_names) == 0:
            return f'There are no files in {self.working_dir}'
            
        return f'{self.working_dir} contains the following file(s):'
        # [print("%3d: %s" % (i, self.files_names[i])) for i in range(len(self.files_names))]
    
    def transform_names(self) -> None:
        # cur_dir = working_dir.split(os.sep)[-1]
        cur_dir = self.working_dir.split('/')[-1]
        self.new_files_names = {Mode.EN: [], Mode.DE: []}
        for fn in self.files_names:
            for mode in Mode:
                self.new_files_names[mode].append(Encryptor.crypt_name(fn, mode, cur_dir))

    def transform_content(self, key: str) -> bool:
        if len(key) <= 15:
            print('WARNING: Too short key!')
            return False
        for i in range(len(self.files_names)):
            Encryptor.crypt_content(self.working_dir, self.files_names[i], 
                                    self.new_files_names[self.mode][i], key)
        return True

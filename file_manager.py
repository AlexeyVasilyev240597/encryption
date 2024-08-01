import glob
import os

from encryptor import Mode, Encryptor

from pathlib import Path

class FileManager:
    def __init__(self) -> None:
        self.working_dir = ''    
    
    def set_working_dir(self, working_dir: str) -> str:
        self.cur_dir = working_dir.split(os.sep)[-1]
        working_dir = Path(working_dir)
        if working_dir.exists():
            self.working_dir = working_dir
            self._list_of_files()
            return 'Working dir is set up'
        else:
            return 'ERROR: Passed working dir name does not exist'
    
    def _list_of_files(self) -> str:
        if not self.working_dir:
            return 'ERROR: The working dir is not set'
        self.files_names = glob.glob(str(self.working_dir) + os.sep + '*')
        self.files_names = [fn.split(os.sep)[-1] for fn in self.files_names]
        if len(self.files_names) == 0:
            return f'There are no files in {self.working_dir}'
            
        return f'{self.working_dir} contains the following file(s):'
        # [print("%3d: %s" % (i, self.files_names[i])) for i in range(len(self.files_names))]
    
    def transform_names(self, mode: Mode) -> None:
        self.new_files_names = []
        for fn in self.files_names:
            self.new_files_names.append(Encryptor.crypt_name(fn, mode, self.cur_dir))

    def transform_content(self, key: str) -> None:
        if not len(self.files_names) == len(self.new_files_names):
            print('ERROR: there are not new files names')
            return
        for i in range(len(self.files_names)):
            Encryptor.crypt_content(self.working_dir, self.files_names[i], self.new_files_names[i], key)

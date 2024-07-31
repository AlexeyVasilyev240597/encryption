import glob
import sys

from pathlib import Path


class FileManager:
    def __init__(self) -> None:
        self.working_dir = ''
    
    
    def set_working_dir(self, working_dir: str) -> bool:
        working_dir = Path(working_dir)
        if working_dir.exists():
            self.working_dir = working_dir
            self.list_of_files()
            return True
        else:
            print('Passed working dir name does not exist')
            return False
    
    
    def list_of_files(self):
        if not self.working_dir:
            print('The working dir is not set')
            return
        self.files_names = glob.glob(str(self.working_dir) + '\*')
        self.files_names = [fn.split('\\')[-1] for fn in self.files_names]
        if len(self.files_names) == 0:
            print(f'There are no files in {self.working_dir}')
            return
        print(f'{self.working_dir} contains the following file(s)')
        [print("%3d: %s" % (i, self.files_names[i])) for i in range(len(self.files_names))]
    
    def parse_indices(self, indxs_str):
        indices = []
        indxs_str = indxs_str.split(',')
        for sub_str in indxs_str:
            if '-' in sub_str:
                sub_str = sub_str.split('-')
                [indices.append(i) for i in range(int(sub_str[0]), int(sub_str[1])+1)]
            else:
                indices.append(int(sub_str))
        return indices
    
if __name__ == '__main__':
    args = sys.argv[1:]
    fm = FileManager()
    fm.set_working_dir(args[0])
    if len(args) == 2:
        indices = fm.parse_indices(args[1])
        print(indices)

# TODO: 
# create .bat file by indices passed by user


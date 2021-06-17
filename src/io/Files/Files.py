import os
import glob


class Files(object):
    def __init__(self, root='.'):
        self.root = root

    def fetch_latest_from_folder(self, folder, filetype='csv'):
        filetype = '/*' + filetype
        folder_path = self.root if self.root[-1] == '/' else self.root + '/'
        folder_path += folder
        files_glob = glob.glob(folder_path + filetype)
        return max(files_glob, key=os.path.getctime)

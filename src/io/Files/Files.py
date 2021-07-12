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


def retrieve_latest_file(identifier: "substring",
                         data_folder: "child director(ies) inside src/data"):
    list_of_files = glob.glob('../../../data/' + data_folder + '/*')
    filtered_list_of_files = list(filter(lambda x: identifier in x, list_of_files))
    latest_file = max(filtered_list_of_files, key=os.path.getctime)
    return latest_file

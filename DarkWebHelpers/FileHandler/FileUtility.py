import hashlib
import json
import os

from DarkWebHelpers.app import AppConfigurations

config = AppConfigurations()


class DeleteDuplicate:
    def __init__(self):
        self.photoBuffer = list()
        self.ListDir()

    @staticmethod
    def FileRemoval(file):
        try:
            if os.path.exists(file):
                os.remove(file)
            else:
                config.debug("The file does not exist")
        except BaseException as e:
            config.debug(e)

    @staticmethod
    def ReadFile(file):
        try:
            with open(file, 'rb') as f:
                return f.read()
        except BaseException as e:
            config.debug(e)

    def ListDir(self):
        try:
            for root, folders, f in os.walk(config.MAIN_DIR):
                for file_ in os.listdir(root):
                    file_path = os.path.join(root, file_)
                    if os.path.isdir(file_path):
                        pass
                    else:
                        hasher = hashlib.md5()
                        hasher.update(self.ReadFile(file_path))
                        #config.debug(hasher.hexdigest())
                        if hasher.hexdigest() in self.photoBuffer:
                            self.FileRemoval(file_path)
                            #config.debug("File Duplicated Removed {}".format(file_path))
                        else:
                            self.photoBuffer.append(hasher.hexdigest())
        except BaseException as e:
            config.debug('Error deleting duplicate files {}'.format( e))
        finally:
            del self.photoBuffer


def write_json(path: os.path, name: str, data_file: dict) -> None:
    """Write results into JSON file

    Args:
        name ([str]): [The name of the file]
        data_file ([dict]): The data to be written
        :param data_file: dictionary object to be saved into json file
        :param name:  file name
        :param path: a path refers to current keyword path
    """
    try:

        with open(os.path.join(path, f'{name}.json'), 'w') as fp:
            json.dump(data_file, fp, indent=3, sort_keys=True)
            fn = os.path.join(path, f'{name}.json')
            config.debug(f"File {fn} has been created")
    except BaseException as e:
        config.debug("Error Writing json")
        config.debug(e)

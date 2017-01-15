"""
Tools for accessing NARVAL-II data from everywhere.
"""
import re

import requests

class SwiftBrowserAccessor(object):
    object_prefix = "https://swiftbrowser.dkrz.de/tempcollection_objects/"
    download_prefix = "https://swiftbrowser.dkrz.de/tempcollection_download/"
    def __init__(self, base_folder):
        self.base_folder = base_folder
    def object_url_of(self, suffix):
        return self.object_prefix + self.base_folder + suffix
    def download_url_of(self, suffix):
        return self.download_prefix + self.base_folder + suffix
    def fetch_object(self, suffix):
        return requests.get(self.object_url_of(suffix))
    def fetch_download(self, suffix):
        return requests.get(self.download_url_of(suffix))
    def list_folder(self, folder=None):
        if folder is None:
            folder = []
        suffix = "".join(map("{}/".format, folder))
        result = self.fetch_object(suffix)
        members = re.findall("<a[^>]+href=\"(/(?:tempcollection_download|tempcollection_objects)/[^\"]*)\"", result.text)
        members = [member.split(self.base_folder) for member in members]
        members = [(category, path[len(suffix):])
                   for category, path in members
                   if path.startswith(suffix)]
        folders = [path[:-1] for category, path in members if "objects" in category and path]
        files = [path for category, path in members if "download" in category]
        return folders, files
    def walk_files(self, folder=None):
        if folder is None:
            folder = []
        folders, files = self.list_folder(folder)
        for folder2 in folders:
            for filename in self.walk_files(folder + [folder2]):
                yield filename
        for filename in files:
            yield folder + [filename]
    def get_file(self, filepath):
        return self.fetch_download("/".join(filepath)).content


def mk_narval_ii_swift_browser_accessor():
    return SwiftBrowserAccessor("d06cc700c5017596938fccbce6974415e6cffa6d/2/1489853226/dkrz_1e33ba3a-9ecb-452f-93b9-583cf4a66e57/NARVAL/0/")

def _main():
    import requests_cache
    requests_cache.install_cache("test_cache")
    
    sba = mk_narval_ii_swift_browser_accessor()
    print(sba.list_folder(["HALO_data"]))
    for filename in sba.walk_files(["HALO_data"]):
        if "Dropsondes_ASPEN" in filename:
            print(filename)

if __name__ == '__main__':
    _main()

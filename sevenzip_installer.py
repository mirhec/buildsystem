from base import BaseBuilder, task

import os
import shutil
import subprocess


class SevenZipInstaller(BaseBuilder):
    # path to 7z.exe
    path_to_7zip = 'C:/Program Files/7-Zip/7z.exe'
    self_extracting = True
    # path to txt file which contains the base directory on the first line and
    # all files to pack from line 2 to the end
    filestxt = 'files.txt'
    dest = 'package.7z'

    @task('gen-file-name')
    def generate_file_name(self):
        if self.self_extracting:
            self.dest = 'Setup-' + self.product_title + '-' + self.version + '.exe'
        else:
            self.dest = '' + self.product_title + '-' + self.version + '.7z'

    @task('clean')
    def clean(self):
        if os.path.exists(self.dest):
            os.remove(self.dest)

    @task('build-package')
    def build_package(self):
        curdir = os.getcwd()

        lines = tuple(open(self.filestxt, 'r'))
        lines = [l.replace('\n', '').replace('\r', '') for l in lines]
        basefolder = lines[0]
        os.chdir(basefolder)
        files = lines[1:]

        if not self.self_extracting:
            cmd = [self.path_to_7zip, 'a', 'package.7z']
            cmd = cmd + files
            self.run(cmd)
            shutil.move('package.7z', os.path.join(curdir, self.dest))
        else:
            cmd = [self.path_to_7zip, 'a', '-sfx7z.sfx', 'installer.exe']
            cmd = cmd + files
            self.run(cmd)
            shutil.move('installer.exe', os.path.join(curdir, self.dest))

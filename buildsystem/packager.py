from .base import BaseBuilder, task
import os
import zipfile
import glob

class Packager(BaseBuilder):
    """
        This Builder creates a zip package of all files that are listed in a simple txt file.
        Each line in the txt file represents one file (or a bunch of files) that will be copied
        to the archive. Each line can have the following definitions:
        
            SRC_FILE : DEST_FOLDER : DEST_NAME
        
        You only need to specify the SRC_FILE, therfore you can use wildcards if you want to.
        The other parameters are optional. If htey are not present, the file will be at the same
        path as the SRC_FILE.

        Here is an example:

            bin/Release/some.dll : bin : some.1.2.dll
            bin/Release/*.lib : lib

        NOTE: The parameters must be seperated with a ' : ' string (don't forget the spaces).
        NOTE: If you use wildcards you should not define a DEST_NAME unless you know for sure there
              is only one file that matches these wildcards.
    """
    file_list = 'files.txt'
    target = 'archive.zip'

    @task('package-files')
    def package_files(self):
        if not os.path.exists(self.file_list):
            raise Exception('File %s does not exist' % self.file_list)
        
        lines = tuple(open(self.file_list, 'r'))
        lines = [l.replace('\n', '').replace('\r', '') for l in lines]
        
        zf = zipfile.ZipFile(self.target, 'w')

        for line in lines:
            parameter = line.split(' : ')
            src = parameter[0]
            dst_dir = parameter[1] if len(parameter) > 1 else None
            dst_name = parameter[2] if len(parameter) > 2 else None
            src_list = glob.glob(src)
            if len(src_list) == 0:
                print('WARNING: No files found for pattern %s!' % src)
            else:
                for file in src_list:
                    name = dst_name if dst_name is not None else os.path.basename(file)
                    zf.write(file, arcname=None if dst_dir is None else os.path.join(dst_dir, name))

        zf.close()

from .base import BaseBuilder, Builder, task
from .java import JavaBuilder

import os
import shutil
import zipfile


class KotlinBuilder(JavaBuilder):
    kotlinpath = 'Y:/Bin/kotlinc'
    
    @task('compile', 4)
    def kotlin_compile(self):
        '''Compile Kotlin files.'''
        if not os.path.exists(self.bindir):
            os.mkdir(self.bindir)
        if not os.path.exists(self.bindir + '/classes/'):
            os.mkdir(self.bindir + '/classes/')
        cp = ';'.join([self.libdir + '/' + s for s in self.depends])
        kotlinc = os.path.join(self.kotlinpath, 'bin', 'kotlinc.bat')
        cmd = [kotlinc, '-nowarn', '-cp', cp, '-d', self.bindir + '/classes', self.srcdir]
        self.run(cmd)

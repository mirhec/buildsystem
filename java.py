from builder import Builder

import os
import shutil
import sys
import zipfile
sys.path.append('/Scripts')
from color_console import *


class JavaBuilder(Builder):

    def __init__(self):
        Builder.__init__(self)
        self.joborder = ['clean', 'dependencies', 'version', 'compile', 'crypt', 'resources', 'lib_classes', 'copy_meta_inf', 'jar', 'exe']
        self.jobs = ['clean', 'dependencies', 'version', 'compile', 'crypt', 'resources', 'lib_classes', 'copy_meta_inf', 'jar', 'exe']

    def initbuild(self):
        if 'libdir' not in dir(self):
            self.libdir = 'lib'
        if 'depdir' not in dir(self):
            self.depdir = 'Y:/Lib/Java'
        if 'srcdir' not in dir(self):
            self.srcdir = 'src'
        if 'bindir' not in dir(self):
            self.bindir = 'bin'
        if 'jar2exedir' not in dir(self):
            self.jar2exedir = 'cfg'
        self.cleandirs = [self.bindir, self.libdir]

    def do_clean(self):
        [shutil.rmtree(d) for d in self.cleandirs if os.path.exists(d)]

    def unpack(self, jar_file, out):
        '''Unpack single jar file `jar_file` to `out` directory.'''
        with open(jar_file, 'rb') as f:
            z = zipfile.ZipFile(f)
            for n in z.namelist():
                z.extract(n, out)

    def do_crypt(self):
        '''Crypt all class files and jars that are specified in `crypt`.'''
        # if 'crpyt' not in dir(self):
        #     return
        self.output('\n   ')
        shutil.copytree(self.bindir + '/classes/', self.bindir + '/classes_temp/')
        shutil.rmtree(self.bindir + '/classes/')
        for c in self.crypt:
            self.output('   -> ' + c + ' ... ')
            self.unpack('lib/%s' % c, self.bindir + '/classes_temp/')
            os.remove('lib/%s' % c)
            self.output('Ok\n   ', ok=True)
        self.output('   crypt all ... ')
        self.run(['java', '-jar', '/Lib/Java/allatori-5.3.jar', 'cfg/allatori2.xml'])
        shutil.rmtree(self.bindir + '/classes_temp/')

    def do_dependencies(self):
        if not os.path.exists(self.libdir):
            os.mkdir(self.libdir)
        [shutil.copyfile(self.depdir + '/' + l, self.libdir + '/' + l) for l in self.depends]

    def do_version(self):
        '''Get version from git branch.'''
        v = self.run(['git', 'rev-parse', '--abbrev-ref', 'HEAD'])
        v = v.rpartition('/')[2]
        v = v.replace('\n', '')
        self.version = v

    def do_compile(self):
        '''Compile Java files.'''
        if not os.path.exists(self.bindir):
            os.mkdir(self.bindir)
        if not os.path.exists(self.bindir + '/classes/'):
            os.mkdir(self.bindir + '/classes/')
        cp = ';'.join([self.libdir + '/' + s for s in self.depends])
        if hasattr(self, 'main_class'):
            main = '%s/%s.java' % ('src', self.main_class.replace('.', '/'),)
            cmd = ['javac', '-encoding', 'utf8', '-sourcepath', self.srcdir, '-cp', cp, '-d', self.bindir + '/classes', main]
            self.run(cmd)
        else:
            files = []
            for (p, dirs, fs) in os.walk(self.srcdir):
                for f in fs:
                    if f[-5:] == '.java':
                        file = p + '\\' + f
                        file = file.replace('\\', '/')
                        files.append(file)

            cmd = ['javac', '-sourcepath', self.srcdir, '-cp', cp, '-d', self.bindir + '/classes']
            cmd.extend(files)
            self.run(cmd)


    def do_resources(self):
        '''Copies all resources under `srcdir` dictionary, excluding *.java files.'''
        self.copytree(self.srcdir + '/', self.bindir + '/classes/', exclude_ext=['.java'])

    def do_lib_classes(self):
        self.output('\n      ')
        for d in self.depends:
            l = '%s/%s' % (self.libdir, d,)
            if os.path.exists(l):
                self.output('-> ' + d + ' ... ')
                self.unpack(l, self.bindir + '/classes/')
                self.output('Ok\n      ', ok=True)

    def do_copy_meta_inf(self):
        s = '%s/META-INF/' % self.srcdir
        b = '%s/classes/META-INF/' % self.bindir
        if os.path.exists(s):
            if os.path.exists(b):
                shutil.rmtree(b)
            self.copytree(s, b)

    def do_jar(self):
        '''Create jar file.'''
        if hasattr(self, 'main_class'):
            self.run(['jar', 'cfe', '%s/%s-%s.jar' % (self.bindir, self.product_title, self.version,), self.main_class, '-C', '%s/classes/' % self.bindir, '.'])
        else:
            self.run(['jar', 'cf', '%s/%s-%s.jar' % (self.bindir, self.product_title, self.version,), '-C', '%s/classes/' % self.bindir, '.'])

    def do_exe(self):
        '''Create exe file.'''
        d = os.getcwd()
        os.chdir(self.jar2exedir)
        self.run(['jar2exe.exe', '../' * (len(self.jar2exedir.split('\\'))) + '%s\\%s-%s.jar' % (self.bindir, self.product_title, self.version,)])
        os.chdir(d)

from base import BaseBuilder, Builder, task

import os
import shutil
import zipfile


class KotlinBuilder(BaseBuilder):
    libdir = 'lib'
    depdir = 'Y:/Lib/Java'
    srcdir = 'src'
    bindir = 'bin'
    jar2exedir = 'cfg'
    version_in_filename = True
    version = None
    pack_all_in_one_jar = True
    kotlinpath = 'Y:/Bin/kotlinc'
    
    def initbuild(self):
        self.cleandirs = [self.bindir, self.libdir]

    def unpack(self, jar_file, out):
        '''Unpack single jar file `jar_file` to `out` directory.'''
        with open(jar_file, 'rb') as f:
            z = zipfile.ZipFile(f)
            for n in z.namelist():
                z.extract(n, out)

    @task('clean')
    def do_clean(self):
        [shutil.rmtree(d) for d in self.cleandirs if os.path.exists(d)]

    @task('dependencies')
    def do_dependencies(self):
        if not os.path.exists(self.libdir):
            os.mkdir(self.libdir)
        [shutil.copyfile(self.depdir + '/' + l, self.libdir + '/' + l) for l in self.depends]

    @task('compile')
    def do_compile(self):
        '''Compile Kotlin files.'''
        if not os.path.exists(self.bindir):
            os.mkdir(self.bindir)
        if not os.path.exists(self.bindir + '/classes/'):
            os.mkdir(self.bindir + '/classes/')
        cp = ';'.join([self.libdir + '/' + s for s in self.depends])
        kotlinc = os.path.join(self.kotlinpath, 'bin', 'kotlinc.bat')
        cmd = [kotlinc, '-nowarn', '-cp', cp, '-d', self.bindir + '/classes', self.srcdir]
        self.run(cmd)
    
    @task('crypt')
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
        self.run(['java', '-jar', '/Lib/Java/allatori-5.3.jar', 'cfg/allatori.xml'])
        shutil.rmtree(self.bindir + '/classes_temp/')

    @task('resources')
    def do_resources(self):
        '''Copies all resources under `srcdir` dictionary, excluding *.kt and *.java files.'''
        self.copytree(self.srcdir + '/', self.bindir + '/classes/', exclude_ext=['.kt', '.java'])

    @task('lib_classes')
    def do_lib_classes(self):
        if self.pack_all_in_one_jar:
            self.output('\n      ')
            for d in self.depends:
                l = '%s/%s' % (self.libdir, d,)
                if os.path.exists(l):
                    self.output('-> ' + d + ' ... ')
                    self.unpack(l, self.bindir + '/classes/')
                    self.output('Ok\n      ', ok=True)
        else:
            self.output('Skipped\n      ', warn=True)

    @task('copy_meta_inf')
    def do_copy_meta_inf(self):
        s = '%s/META-INF/' % self.srcdir
        b = '%s/classes/META-INF/' % self.bindir
        if os.path.exists(s):
            if os.path.exists(b):
                shutil.rmtree(b)
            self.copytree(s, b)

    @task('jar')
    def do_jar(self):
        '''Create jar file.'''
        
        if self.version_in_filename:
            name = '%s/%s-%s.jar' % (self.bindir, self.product_title, self.version,)
        else:
            name = '%s/%s.jar' % (self.bindir, self.product_title,)

        if hasattr(self, 'main_class'):
            self.run(['jar', 'cfe', name, self.main_class, '-C', '%s/classes/' % self.bindir, '.'])
        else:
            self.run(['jar', 'cf', name, '-C', '%s/classes/' % self.bindir, '.'])

    @task('exe')
    def do_exe(self):
        '''Create exe file.'''
        d = os.getcwd()
        os.chdir(self.jar2exedir)
        minus = 0
        if self.jar2exedir is '.':
            minus = 1
        if self.version_in_filename:
            self.run(['jar2exe.exe', '../' * (len(self.jar2exedir.split('/')) - minus) + '%s\\%s-%s.jar' % (self.bindir, self.product_title, self.version,)])
        else:
            self.run(['jar2exe.exe', '../' * (len(self.jar2exedir.split('/')) - minus) + '%s\\%s.jar' % (self.bindir, self.product_title,)])
        os.chdir(d)

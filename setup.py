from base import BaseBuilder, task
import os


class SetupBuilder(BaseBuilder):
    setupdir = '.'
    setupscript = None
    product_title = 'Setup'

    @task('compile_setup')
    def do_compile_setup(self):
        '''Compiles the Inno Setup Script `setupscript` into directory `setupdir` if `setupscript` is specified and exists.
        `setupscript` has to be defined based on the directory `setupdir`.'''
        if self.setupscript and os.path.exists(os.path.join(self.setupdir, self.setupscript)):
            d = os.getcwd()
            os.chdir(self.setupdir)
            # write version information into git.txt
            with open('git.txt', 'w') as f:
                f.write(self.version)
                
            # run setup
            self.run([r'C:\Program Files (x86)\Inno Setup 5\ISCC.exe', self.setupscript])
            
            # remove git.txt
            os.remove('git.txt')
            os.chdir(d)

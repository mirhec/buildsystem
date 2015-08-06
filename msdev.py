from base import BaseBuilder, task
import os
import shutil


class MsdevBuilder(BaseBuilder):
    msbuild_exe = r'\Lib\MSBuild.exe'
    solution_file = None
    target = None
    out_dir = 'bin'

    @task('compile')
    def compile_it(self):
        '''Compiles MSDev solution.'''
        if self.solution_file and self.target:
            me = os.getcwd()
            print me + '/' + self.out_dir
            self.run([self.msbuild_exe, '/t:build', '/p:Configuration=Release;TargetName=%s' % self.target, '/property:OutDir=%s' % me + '/' + self.out_dir, self.solution_file])

            # now move it to the right location and rename it
            base = os.path.join(self.out_dir, self.target)
            exts_to_move = ['.dll', '.exe', '.lib']
            for f in exts_to_move:
                if os.path.exists(base + f):
                    shutil.move(base + f, base + '-' + self.version + f)

    @task('clean')
    def clean(self):
        files = os.listdir(self.out_dir)
        for f in files:
            if f[-4:] not in ['.dll', '.exe', '.lib']:
                os.remove(os.path.join(self.out_dir, f))

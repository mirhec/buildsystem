from base import BaseBuilder, task
import os
import shutil


class MsdevBuilder(BaseBuilder):
    msbuild_exe = r'\Lib\MSBuild.exe'
    solution_file = None
    target = None
    out_dir = 'bin'
    build_conf = 'Release'
    append_version = True

    @task('compile')
    def compile_it(self):
        '''Compiles MSDev solution.'''
        if self.solution_file and self.target:
            me = os.getcwd()
            self.run([self.msbuild_exe, '/t:build', '/p:Configuration=%s;TargetName=%s' % (self.build_conf, self.target,), '/property:OutDir=%s' % me + '/' + self.out_dir, self.solution_file])

            # now move it to the right location and rename it
            base = os.path.join(self.out_dir, self.target)
            exts_to_move = ['.dll', '.exe', '.lib']
            v = '-' + self.version if self.append_version else ''
            for f in exts_to_move:
                if os.path.exists(base + f):
                    shutil.move(base + f, base + v + f)

    @task('clean')
    def clean(self):
        files = os.listdir(self.out_dir)
        for f in files:
            p = os.path.join(self.out_dir, f)
            if os.path.isfile(p) and f[-4:] not in ['.dll', '.exe', '.lib']:
                os.remove(p)
            elif os.path.isdir(p):
                shutil.rmtree(p)

# -*- coding: iso-8859-1 -*-
import os
import shutil
import sys
import time
import subprocess
sys.path.append('/Scripts')
from color_console import *

class Builder:

    '''Base class for all Build System Builder.'''

    def __init__(self):
        self.starttime = time.time()
        pass

    def conf(self, **kwargs):
        '''Defines all possible configurations for this builder.'''
        for key in kwargs:
            self.__dict__[key] = kwargs[key]

    def initbuild(self):
        pass

    def build(self):
        self.initbuild()
        # Get command line args and use them as jobs
        if len(sys.argv) > 1:
            self.jobs = sys.argv[1:]
        self.output(self.__class__.__name__ + ' builds ' + self.product_title, True)
        if self.joborder and self.jobs:
            cnt = 1
            for job in self.joborder:
                self.output('   ' + str(cnt) + '. ' + job + ' ... ')
                if job in self.jobs and 'do_' + job in dir(self) and callable(getattr(self, 'do_' + job)):
                    try:
                        getattr(self, 'do_' + job)()
                        self.output('Done', True, ok=True)
                    except subprocess.CalledProcessError, ce:
                        self.output('Failed', True, err=True)
                        self.log(job, str(ce))
                        self.log(job, ce.output)
                    except Exception, e:
                        self.output('Failed', True, err=True)
                        self.log(job, str(e))
                elif job not in self.jobs:
                    self.output('Skipped', True, warn=True)
                elif job in self.jobs:
                    self.output('Not implemented', True, err=True)
                cnt += 1

    def log(self, task, what):
        if 'log_enabled' in dir(self) and self.log_enabled:
            with open('build.log', 'a') as f:
                f.write('%s :: [%s] :: %s\n' % (str(int((time.time() - self.starttime) * 1000)), task, what,))

    def output(self, what, newline=False, err=False, ok=False, warn=False):
        old = get_text_attr()
        if ok:
            set_text_attr(FOREGROUND_GREEN)
        if warn:
            set_text_attr(FOREGROUND_YELLOW)
        if err:
            set_text_attr(FOREGROUND_RED)
        sys.stdout.write(what)
        if newline:
            sys.stdout.write('\n')
        set_text_attr(old)

    def run(self, args):
        '''Simple wrapper for subprocess.check_output().'''
        return subprocess.check_output(args, stderr=subprocess.STDOUT)

    def copytree(self, src, dst, exclude_ext=None):
        '''- Creating the output directory if not already exists
           - Doing the copy directory by recursively calling my own method.
           - When we come to actually copying the file I check if the file is modified then only we should copy.'''

        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                self.copytree(s, d, exclude_ext)
            elif exclude_ext is None or True not in [d.endswith(ext) for ext in exclude_ext]:
                if not os.path.exists(d) or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                    shutil.copy2(s, d)

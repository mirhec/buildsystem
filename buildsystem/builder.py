# -*- coding: iso-8859-1 -*-
import os
import shutil
import sys
import time
import subprocess
from .color_console import *

jobindex = 1

def optional_arg_decorator(fn):
    def wrapped_decorator(*args):
        if len(args) == 1 and callable(args[0]):
            return fn(args[0])

        else:
            def real_decorator(decoratee):
                return fn(decoratee, *args)

            return real_decorator

    return wrapped_decorator

@optional_arg_decorator
def task(fn, name, jobidx = -1):
    global jobindex
    fn.decorator = task
    if jobidx != -1:
        fn.jobindex = jobidx
    else:
        fn.jobindex = jobindex
        jobindex += 1
    fn.name = name
    return fn


class Builder:
    '''Base class for all Build System Builder.'''
    product_title = ''
    skip = []
    logpath = 'build.log'

    def __init__(self):
        self.starttime = time.time()
        self.logpath = os.path.join(os.getcwd(), 'build.log')

    def conf(self, **kwargs):
        '''Defines all possible configurations for this builder.'''
        for key in kwargs:
            self.__dict__[key] = kwargs[key]

    def initbuild(self):
        pass

    def build(self):
        self.output(self.__class__.__name__ + ' builds ' + self.product_title, True)
        self.initbuild()

        tasks = list(self.get_all_tasks())
        tasks = self.sorttasks(tasks)
        cnt = 1
        max_job_nr = max([f.jobindex for f in tasks])

        # for job in tasks:
        for i in range(1, max_job_nr + 1):
            jobs = [f for f in tasks if f.jobindex == i]
            if len(jobs) <= 0:
                continue
            job = jobs[-1]
            self.output('   ' + str(cnt) + '. ' + job.name + ' ... ')
            if job.name not in self.skip and (job.name in sys.argv[1:] or len(sys.argv) <= 1):
                try:
                    job()
                    self.output('Done', True, ok=True)
                except subprocess.CalledProcessError as ce:
                    self.output('Failed', True, err=True)
                    self.log(job.name, str(ce))
                    self.log(job.name, ce.output)
                    exit(-1)
                except Exception as e:
                    self.output('Failed', True, err=True)
                    self.log(job.name, str(e))
                    exit(-2)
            elif job.name not in sys.argv[1:] or job.name in self.skip:
                self.output('Skipped', True, warn=True)
            else:
                self.output('Not implemented', True, err=True)
            cnt += 1

    def log(self, task, what):
        if 'log_enabled' in dir(self) and self.log_enabled:
            with open(self.logpath, 'a') as f:
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

    def copytree(self, src, dst, exclude_ext=None, compare_date=True):
        '''- Creating the output directory if not already exists
           - Doing the copy directory by recursively calling my own method.
           - When we come to actually copying the file I check if the file is modified then only we should copy.'''

        if not os.path.exists(dst):
            os.makedirs(dst)
        for item in os.listdir(src):
            s = os.path.join(src, item)
            d = os.path.join(dst, item)
            if os.path.isdir(s):
                self.copytree(s, d, exclude_ext, compare_date)
            elif exclude_ext is None or True not in [d.endswith(ext) for ext in exclude_ext]:
                if not os.path.exists(d) or not compare_date or os.stat(src).st_mtime - os.stat(dst).st_mtime > 1:
                    shutil.copy2(s, d)

    def get_all_tasks(self):
        for maybeDecorated in dir(self):
            maybeDecorated = getattr(self, maybeDecorated)
            if hasattr(maybeDecorated, 'decorator'):
                if maybeDecorated.decorator == task:
                    yield maybeDecorated

    def sorttasks(self, tasks):
        for passnum in range(len(tasks) - 1, 0, -1):
            for i in range(passnum):
                if tasks[i].jobindex > tasks[i+1].jobindex:
                    tmp = tasks[i]
                    tasks[i] = tasks[i+1]
                    tasks[i+1] = tmp
        return tasks

from builder import Builder, task
import os


class BaseBuilder(Builder):
    @task('version')
    def do_version(self):
        '''Get version from git branch.'''
        v = self.run(['git', 'describe', '--tags', '--abbrev=0'])
        v = v.replace('\n', '')
        self.version = v

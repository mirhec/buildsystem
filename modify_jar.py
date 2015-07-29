from java import JavaBuilder, task


class ModifyJarBuilder(JavaBuilder):
    joborder = ['clean', 'dependencies', 'version', 'version_properties', 'lib_classes', 'overwrite', 'jar', 'exe']
    overwrite_dir = None
    version_properties = None

    @task('version_properties')        
    def do_version_properties(self):
        '''Write a .properties file with version information, if conf string `version_properties` is given.'''
        if self.version_properties and self.version:
            with open(self.version_properties, 'w') as f:
                f.write('VERSION=%s' % self.version)

    @task('overwrite')
    def do_overwrite(self):
        '''Copies all files under `overwrite_dir` into `bindir`/classes if `overwrite_dir` is set.'''
        if self.overwrite_dir:
            self.copytree(self.overwrite_dir + '/', self.bindir + '/classes/', compare_date=False)

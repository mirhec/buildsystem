import os
try:
    from urllib import urlretrieve
except:
    from urllib.request import urlretrieve

class DependencyResolver:
    def resolve(self, dependency, destination):
        raise NotImplementedError('You should instanciate a concrete class!')

class FileDependencyResolver:
    def __init__(self, depdir):
        self.depdir = depdir

    def resolve(self, dependency, destination):
        shutil.copyfile(os.path.join(self.depdir, dependency, os.path.join(destination, dependency)))

class HttpDependencyResolver:
    def __init__(self, baseurl):
        self.baseurl = baseurl
    
    def resolve(self, dependency, destionation):
        urlretrieve(self.baseurl + '/' + dependency, os.path.join(destionation, dependency))
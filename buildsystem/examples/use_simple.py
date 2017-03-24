# Prepare the buildsystem
from subprocess import Popen, call
from os.path import exists
if exists('buildsystem'):
    Popen(['git', 'pull', 'origin'], cwd='buildsystem').wait()
else:
    call(['git', 'clone', 'https://github.com/mirhec/buildsystem', 'buildsystem'])

# Import the builder
from buildsystem.simple import MyBuilder

# Create and configure the builder
builder = MyBuilder()
builder.my_name = 'Conroe'

# Run the build
builder.build()
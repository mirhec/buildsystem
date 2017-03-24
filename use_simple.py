from subprocess import call
call(['git', 'clone', 'https://github.com/mirhec/buildsystem', 'buildsystem'])

from buildsystem.simple import MyBuilder

builder = MyBuilder()
builder.my_name = 'Conroe'
builder.build()
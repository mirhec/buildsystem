# Buildsystem

This is a very simple build system written in python that is hackable and easy to extend. 
The problem I had so far with other build systems was the lack of scripting ability that 
I needed many times.

## How to use
Here's an example on how to use the MsdevBuilder. The MsdevBuilder allows you to
compile and clean your Msdev-Solution (.sln) and specify some options. Here's an
example usage file `build.py`:

```python
from buildsystem.msdev import MsdevBuilder

msdevbuilder = MsdevBuilder()
msdevbuilder.conf(product_title='SIMAVIS H',
             solution_file='src/simavis_h.sln',
             target='simavis_h',
             build_conf='Release',
             log_enabled=True)
msdevbuilder.log_enabled = False
msdevbuilder.build()
```

As you can see there are some properties we could define. You have multiple options
to set them, either by calling the `conf` method, or by setting them via direct call.

## How to add your own builder
Adding your own builder is very easy. You just have to create a new class that inherits
from `Builder` and add your tasks in that order to be executed and add to each of them
the `task` decorator. Here is an example:

```python
from builder import Builder, task

class MyBuilder(Builder):
    # here you could declare some configuration properties if you want to
    my_name = 'Nobody'
    
    @task('greet-me')
    def greet_me(self):
        # to output something with the right indentation, use self.output
        # You can define the color by specifying an ok=True, warn=True or error=True.
        self.output('Hello ' + self.my_name + '. ', ok=True)
    
    @task('greet-all')
    def greet_world(self):
        self.output('Hello to all others! ')
```

You can now use it by simple writing

```python
from simple import MyBuilder

builder = MyBuilder()
builder.my_name = 'Conroe'
builder.build()
```

## Commandline options
If you want to skip some tasks, you can do this by adding them to the `skip` list by
just calling

```python
builder.skip.append('greet-all')
```

If you want to only execute some tasks you can call your build script with the task-names
of the arguments you want to run:

```
python build.py greet-me
```

This would only run the `greet_me` method and output the `greet-all` task as skipped.

![sample](https://cloud.githubusercontent.com/assets/5173805/11562974/8493d2f4-99d1-11e5-801c-698179ca6705.gif)

## Using the git version info in an Inno Script setup file

The setup.py build script first creates a git.txt file containing the version information read
from the git tags. After compiling the setup this file will be deleted. If you want to add the
version information in your Inno Script setup, you just need to read this file by adding the following
code to your Setup.iss file:

```
#define FileHandle
#define FileLine
#sub ProcessFileLine
  #pragma message FileLine
#endsub
#for {FileHandle = FileOpen("git.txt"); FileHandle && !FileEof(FileHandle); FileLine = FileRead(FileHandle)} ProcessFileLine
#if FileHandle
  #expr FileClose(FileHandle)
#endif
#define VERSION Copy(FileLine, Pos("/", FileLine) + 1)
```

After this you can use the VERSION constant by inserting `{#VERSION}` into your script, for example in your [Setup] section: 
```
AppVersion={#VERSION}
```

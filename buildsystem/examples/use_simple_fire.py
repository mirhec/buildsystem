"""Example how to use fire to create a build script."""
from buildsystem.fire_builder import FireBuilder

# with this call you can manually select the build steps (to build all use use_simple_fire.py build)
FireBuilder(name='James').create()

# or if you always want to build all build steps:
FireBuilder(name='Jim').build()

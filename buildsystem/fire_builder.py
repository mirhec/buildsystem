"""This is an example for a python-fire based build script"""
import fire
from buildsystem.builder import Builder


class FireBuilder(Builder):
    """Simple FireBuilder class"""
    # here you could declare some configuration properties if you want to
    def __init__(self, name='Nobody'):
        Builder.__init__(self)
        self.my_name = name

    def greet_me(self):
        """Greet me"""
        self.output('Hello ' + self.my_name + '. ', ok=True)

    def greet_world(self):
        """Greet the whole world"""
        self.output('Hello to all others! ')

    def build(self):
        self.greet_me()
        self.greet_world()

    def create(self):
        """Create the fire cli."""
        fire.Fire(self)

if __name__ == '__main__':
    fire.Fire(FireBuilder)
    # FireBuilder().create()

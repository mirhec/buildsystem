from .builder import Builder, task


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
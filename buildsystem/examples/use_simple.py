# Import the builder
from buildsystem.simple import MyBuilder

# Create and configure the builder
builder = MyBuilder()
builder.my_name = 'Conroe'

# Run the build
builder.build()
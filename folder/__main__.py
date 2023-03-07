import os

# set the directory path
directory = '/folder/to/directory'

# loop through all files in the directory
for filename in os.listdir(directory):
    filepath = os.path.join(directory, filename)
    # check if the file is a Python file
    if filename.endswith('.py'):
        # run the file
        os.system(f'python {filepath}')

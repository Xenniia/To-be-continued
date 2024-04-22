#change one extension of the file

import os

# Entering path of the file

file_path = input('Enter the file path :').replace('"', '')

base_file, extension = os.path.splitext(file_path)
extension = extension.replace('.','')

# Entering future extension of the file

new_extension = input('Enter extension future file :')
new_file_path = base_file + '.' + new_extension

# Rename extension of the file

os.rename(file_path, new_file_path)
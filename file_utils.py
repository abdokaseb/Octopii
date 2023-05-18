"""
MIT License

Copyright (c) 2022 Owais Shaikh 
Research @ RedHunt Labs Pvt Ltd
Email: owais.shaikh@redhuntlabs.com

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import json, os

def list_local_files(local_path):
    files_list = []
    for root, subdirectories, files in os.walk(local_path):
        for file in files:
            relative_path = (os.path.join(root, file))
            files_list.append(relative_path)

    return files_list

def append_to_output_file(data, file_name):
    try:
        loaded_json = []
        try: 
            with open(file_name, 'r+') as read_file:    
                loaded_json = json.loads(read_file.read())
        except: # No file
            print ("Creating new file named \'" + file_name + "\' and writing to it.")

        with open(file_name, 'w') as write_file:
            loaded_json.append(data)
            write_file.write(json.dumps(loaded_json, indent=4))
            
    except:
        print ("Couldn't write to "+ file_name +". Please check if the path is correct and try again.")
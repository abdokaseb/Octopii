"""
MIT License

Copyright (c) Research @ RedHunt Labs Pvt Ltd
Written by Owais Shaikh
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

output_file = "output.json"

import json, sys, os, json
import file_utils, text_utils

def print_logo():
    logo = '''⠀⠀⠀ ⠀⡀⠀⠀⠀⢀⢀⠀⠀⠀⢀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠋⠓⡅⢸⣝⢷⡅⢰⠙⠙⠁⠀⠀⠀⠀
⠀⢠⣢⣠⡠⣄⠀⡇⢸⢮⡳⡇⢸⠀⡠⡤⡤⡴⡄⠀    O C T O P I I
⠀⠀⠀⠀⠀⡳⠀⠧⣤⡳⣝⢤⠼⠀⡯⠀⠀⠈⠀⠀    A PII scanner
⠀⠀⠀⠀⢀⣈⣋⣋⠮⡻⡪⢯⣋⢓⣉⡀⠀⠀⠀⠀(c) 2023 RedHunt Labs Pvt Ltd
⠀⠀⠀⢀⣳⡁⡡⣅⠀⡗⣝⠀⡨⣅⢁⣗⠀⠀⠀⠀
⠀⠀⠀⠀⠈⠀⠸⣊⣀⡝⢸⣀⣸⠊⠀⠉⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⠈⠀⠀⠈⠈'''
    print (logo)

def help_screen():
    help = '''Usage: python octopii.py <file, local path>
Note: Only Unix-like filesystems are supported.'''
    print(help)

def search_pii(file_path):
    
    try:
        with open(file_path, "r") as fin:
            text = fin.read()
            intelligible = text_utils.string_tokenizer(text)
    except:
        print ("Couldn't find file '" + file_path + "'")
        exit(-1)

    addresses = text_utils.regional_pii(text)
    emails = text_utils.email_pii(text, rules)
    phone_numbers = text_utils.phone_pii(text, rules)

    keywords_scores = text_utils.keywords_classify_pii(rules, intelligible)
    score = max(keywords_scores.values())
    pii_class = list(keywords_scores.keys())[list(keywords_scores.values()).index(score)]

    country_of_origin = rules[pii_class]["region"]

    identifiers = text_utils.id_card_numbers_pii(text, rules)

    if score < 5:
        pii_class = None

    if len(identifiers) != 0:
        identifiers = identifiers[0]["result"]

    result = {
        "file_path" : file_path,
        "pii_class" : pii_class,
        "score" : score,
        "country_of_origin": country_of_origin,
        "identifiers" : identifiers,
        "emails" : emails,
        "phone_numbers" : phone_numbers,
        "addresses" : addresses
    }

    return result
    

if __name__ in '__main__':

    if len(sys.argv) > 1:
        location = sys.argv[1] 
    else: 
        print_logo()
        help_screen()
        exit(-1)

    rules=text_utils.get_regexes()

    files = []
    items = []

    print("Scanning '" + location + "'")

    _, extension = os.path.splitext(location)
    if extension != "":
        files.append(location)
    else:
        files = file_utils.list_local_files(location)

    if len(files) == 0:
        print ("Invalid path provided. Please provide a non-empty directory or a file as an argument.")
        sys.exit(0)

    for file_path in files:
        results = search_pii(file_path)
        print(json.dumps(results, indent=4))
        file_utils.append_to_output_file(results, output_file)

    print ("Output saved in " + output_file)

    sys.exit(0)
            
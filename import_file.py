#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Import a file from file system and extract text from it using Tika
"""

import os
from tika import parser


# get file path
file_name = "test.pdf"
cwd = os.path.dirname(os.path.realpath(__file__))
print(cwd)

#print(root_path)
file_path = os.path.join(cwd, "data/"+file_name)
print(file_path)


parsedPDF = parser.from_file(file_path, 'http://localhost:9998/tika')

#display parsed content
print(parsedPDF['content'])
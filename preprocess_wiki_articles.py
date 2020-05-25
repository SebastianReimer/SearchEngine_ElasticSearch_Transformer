#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
preprocess data

* remove articles containing lists
* save each article in one txt-file

"""
import os
import json
import re
import shutil



root_dir = '/home/sebastian/SideProject/QA/wikiextractor/extracted/json_files'

all_folders = os.listdir(root_dir)

save_dir = '/home/sebastian/SideProject/QA/wikiextractor/preprocessed'

i = 0
folder_nr = 1
for folder in sorted(all_folders)[:2]:
   # print(folder)
        
    #path_procdir = os.path.join(save_dir, folder)
    #if os.path.exists(path_procdir):
    #    shutil.rmtree(path_procdir)
    #os.mkdir(path_procdir)

    
    path = os.path.join(root_dir, folder)
    for file in sorted(os.listdir(path)):
        path_file = os.path.join(path, file)
        #text files containing several json strings --> prepare so that json.loads can handle them
        with open(path_file, 'r') as f:
            text_file =  f.read()
        json_data = re.findall('\{{1}.*\}{1}',text_file) # find json files
        #convert json strings to dicts
        list_articles= [json.loads(article) for article in json_data] 
        
        #remove articles containing 'Liste' in title
        pattern = 'Liste.*'
        for article in list_articles:
            #create folder containing 10000 articles
            if i % 10000 == 0:
                print(i)
                path_procdir = os.path.join(save_dir, 'folder_' + str(folder_nr))
                folder_nr += 1
                if os.path.exists(path_procdir):
                    shutil.rmtree(path_procdir)
                os.mkdir(path_procdir)
            if not re.match(pattern, article['title']):
                path_procfile = os.path.join(path_procdir, article['id']+'.txt')
                with open(path_procfile, 'w') as out:
                    out.write(article['text'])
                    i += 1

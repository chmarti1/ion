#!/usr/bin/python

import os

data_dir = '../data'
month_map = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Nov', 'Dec']

contents = os.listdir(data_dir)
contents.sort(reverse=True)
for target in contents:
    target_dir = os.path.join(data_dir, target)
    if os.path.isdir(target_dir) and len(target) == 14 and target.isdigit():
        directories = []
        datfiles = 0
        
        for this in os.listdir(target_dir):
            this_full = os.path.join(target_dir, this)
            if os.path.isdir(this_full):
                directories.append(this)
            elif this.endswith('.dat'):
                datfiles += 1
                
        year = target[:4]
        month = month_map[int(target[4:6])-1]
        day = target[6:8] if target[6]!='0' else ' '+target[7]
        hour = target[8:10] if target[8]!='0' else ' '+target[9]
        minute = target[10:12]
        second = target[12:14]
        out = month + ' ' + day + ' ' + year + ' ' + hour + ':' + minute + ':' + second
        out += '  [' + str(datfiles) + ']'
        directories.sort()
        for this in directories:
            out += '  ' + this
        print(out)

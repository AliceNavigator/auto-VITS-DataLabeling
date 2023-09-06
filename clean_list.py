import os
import re

new_annos = []
cleaned_new_annos = []

if os.path.exists("./barbara.list"):
    with open("./barbara.list", 'r', encoding='utf-8') as f:
        long_character_anno = f.readlines()
        new_annos += long_character_anno
else:
    print('barbara.list cannot be found, please confirm that the path is correct')
    exit()

for line in new_annos:
    path, name, lang, text = line.split("|")
    text += "\n" if not text.endswith("\n") else ""
    if len(text) >= 5:
        my_re = re.compile(r'[A-Za-z]', re.S)
        res = re.findall(my_re, text)
        if len(res):
            print(f'Skip non-kanji text : {text}')
        else:
            cleaned_new_annos.append(path + "|" + name + "|" + lang+ "|" + text)
    else:
        print(f'skip too short wav : {text}')


with open("./clean_barbara.list", 'w', encoding='utf-8') as f:
    for line in cleaned_new_annos:
        f.write(line)

print('Done! save as clean_barbara.list')

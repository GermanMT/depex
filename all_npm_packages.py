import json
import os

json_file = open("names.json", "r")
names = json.load(json_file)

if os.path.exists("all_npm_packages"):
    os.system("rm -rf " + "all_npm_packages/")
os.mkdir("all_npm_packages")

j = 0
i = 0
len_ = 1000
while i < len(names):
    part = names[i:i+len_]
    file = open(f"all_npm_packages/all_npm_packages_{j}.txt", "w")
    for index, package in enumerate(part):
        if index == len_ - 1:
            file.write(package)
            break
        file.write(package + "\n")
    file.close()
    i += len_
    j += 1
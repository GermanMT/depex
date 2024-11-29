import requests
import os

response = requests.get("https://pypi.org/simple/")

all_packages = []
for x in response.text.split("\n"):
    if "<a href=\"/simple/" in x:
        all_packages.append(x.replace("<a href=\"/simple/", "").split("/")[0] + "\n")

if os.path.exists("all_pypi_packages"):
    os.system("rm -rf " + "all_pypi_packages/")
os.mkdir("all_pypi_packages")

j = 0
i = 0
while i < len(all_packages):
    part = all_packages[i:i+100]
    file = open(f"all_pypi_packages/all_pypi_packages_{j}.txt", "w")
    for package in part:
        file.write(package)
    file.close()
    i += 100
    j += 1
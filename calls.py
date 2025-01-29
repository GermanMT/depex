from requests import post

final_file = 5885
for i in range(1, 2):
    record_file = open("recorded_packages.txt", "w")
    with open(f"partes/parte_{i}.txt", "r") as file:
        text = file.read()
        packages = text.split("\n")
        for package in packages:
            print("Iniciando extracción para el paquete: ", package)
            record_file.write(package + "\n")
            post(f"http://localhost:8000/graph/nuget/package/init?package_name={package}")
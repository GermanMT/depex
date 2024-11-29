from requests import post

record_file = open("recorded_packages.txt", "w")
with open("all_pypi_packages/all_pypi_packages_0.txt", "r") as file:
    text = file.read()
    packages = text.split("\n")

    for package in packages:
        print("Iniciando extracción para el paquete: ", package)
        record_file.write(package)
        post(f"http://localhost:8000/graph/pypi/package/init?package_name={package}")

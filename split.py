def dividir_archivo(archivo_entrada, lineas_por_archivo=1000):
    # Abre el archivo de entrada en modo lectura
    with open(archivo_entrada, 'r', encoding='utf-8') as f:
        numero_archivo = 1
        while True:
            # Lee las siguientes 'lineas_por_archivo' líneas
            lineas = [f.readline() for _ in range(lineas_por_archivo)]

            for x in lineas[:]:
                if not x.strip():
                    lineas.remove(x)
            
            # Si no hay más líneas, termina el bucle
            if not any(lineas):
                break
            
            # Crea un nuevo archivo de salida
            nombre_archivo_salida = f'partes/parte_{numero_archivo}.txt'
            with open(nombre_archivo_salida, 'w', encoding='utf-8') as f_out:
                for i, linea in enumerate(lineas):
                    if i == len(lineas) - 1:
                        f_out.write(linea.replace("\n", ""))
                        break
                    f_out.write(linea)
            
            print(f'Creado: {nombre_archivo_salida}')
            numero_archivo += 1

# Llama a la función con el nombre de tu archivo de entrada
dividir_archivo('nuget_packages.txt')

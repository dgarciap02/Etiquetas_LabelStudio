import json
import glob
import re

def leer_json(ruta_ref, ruta_datasheet) :
    # Abre el archivo en modo lectura
    with open(ruta_ref, 'r') as archivo_ref:
        # Carga los datos del archivo en un objeto JSON
        ref_clases = json.load(archivo_ref)

    with open(ruta_datasheet, 'r') as archivo_datasheet:
        # Carga los datos del archivo en un objeto JSON
        datasheet_clases = json.load(archivo_datasheet)

    return ref_clases['categories'], datasheet_clases['categories']

ref_clases, datasheet_clases = leer_json('notes.json','337/notes.json')
# print(ref_clases, '===================================')
# print(datasheet_clases, '===================================')

def eliminar_etiquetas(ref_clases, datasheet_clases):
    lista_borrar= []
    for clase in datasheet_clases:
        encontrado = False
        for clase_ref in ref_clases:
            if clase["name"] == clase_ref["name"]:
                encontrado = True
        if not encontrado:
            lista_borrar.append(clase)
    for clase_borrar in lista_borrar:
            datasheet_clases.remove(clase_borrar)

    return datasheet_clases, lista_borrar

datasheet_clases_nuevo, lista_borrar = eliminar_etiquetas(ref_clases, datasheet_clases)
# print((datasheet_clases_nuevo),'====000=====================')
# print((lista_borrar),'====000=====================')

def comparar_etiquetas(ref_clases, datasheet_clases_nuevo): 
    ids_etiquetas = {}
    for clase in datasheet_clases_nuevo:
        for clase_ref in ref_clases:
            if clase["name"] == clase_ref["name"]:
                ids_etiquetas[clase['id']] = clase_ref['id']
    return ids_etiquetas

ids_etiquetas = comparar_etiquetas(ref_clases, datasheet_clases_nuevo)
# print(ids_etiquetas,'=====================')

def eliminar_txts(ruta_txt, lista_borrar):
    lista_archivos = glob.glob(ruta_txt + '/*.txt')
    for clase_borrar in lista_borrar:
        id_borrar_str = str(clase_borrar['id'])
        # print(id_borrar_str, '===============')
        for archivo in lista_archivos:
            # print(archivo, '-------------------------------')
            with open(archivo, "r+") as file:
                lineas = file.readlines()
                file.seek(0)
                for linea in lineas:
                    palabras = linea.split()
                    # print(palabras[0], '--------------')
                    if palabras[0] != id_borrar_str:
                        file.write(linea)
                file.truncate() 

def modificar_txts(ruta_txt, ids_etiquetas):
    lista_archivos = glob.glob(ruta_txt + '/*.txt')
    
    for archivo in lista_archivos:
        # print(archivo, '-------------------------------')
        with open(archivo, "r+") as file:
            lineas = file.readlines()
            file.seek(0)
            for linea in lineas:
                palabras = linea.split()
                print(palabras,'===========')
                for id_antigua, id_nueva in ids_etiquetas.items(): 
                    if palabras[0] == str(id_antigua):
                        palabras[0] = str(id_nueva)
                        print(palabras,'----------------')
                        nueva_linea = " ".join(palabras) + "\n"
                        print(nueva_linea)
                        file.write(nueva_linea) 

eliminar_txts('337/labels',lista_borrar)
modificar_txts('337/labels',ids_etiquetas)


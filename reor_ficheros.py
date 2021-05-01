import sys, os, shutil
import zipfile
import rarfile

##rarfile.UNRAR_TOOL = "/usr/local/bin/unrar"
rarfile.UNRAR_TOOL = "C:\\Program Files\\WinRAR\\unrar.exe"


image_ext = [".jpeg", ".jpg", ".png"]
max_ext = [".max", ".mat", ".mar"]



def findImage(filename):
    for e in image_ext:
        if os.path.isfile(filename + e):
            return e
    return "none"

def findMax(ext):
    for e in max_ext:
        if ext.lower() == e:
            return True
    return False

def desComp(file_name, ext):
    print("Expanding file: "+file_name+ext)
    if ext == ".zip":
        file_comp = zipfile.ZipFile(file_name + ".zip", 'r')
    elif ext == ".rar":
        file_comp = rarfile.RarFile(file_name + ".rar", 'r')
    try:
        file_comp.extractall(file_name)
    except rarfile.RarCRCError as error:
        print(error.args)
    file_comp.close()
    os.remove(file_name + ext)


def procFolder(folder, pathf, ext_jpg):
    print("Processing FOLDER: " + pathf)
    for f in os.listdir(pathf):
        (filename, ext) = os.path.splitext(f)
        # Si es una carpeta
        if os.path.isdir(os.path.join(pathf,f)):
            filename = f
            ext = ""
            procFolder(folder, os.path.join(pathf, filename), ext_jpg)
        # Si he encontrado un fichero comprimido
        elif ext.lower() == ".zip" or ext.lower() == ".rar":
            desComp(os.path.join(pathf, filename), ext)
            procFolder(folder, os.path.join(pathf, filename), ext_jpg)
        # Si he encontrado un fichero .max
        elif findMax(ext):
            # Si estoy en una subcarpeta, y el .max no existía ya en la carpeta principal, subo el .max a la carpeta principal
            if folder != pathf:
                if not os.path.isfile(os.path.join(folder, f)):
                    print("Moving " + ext.upper() + " file: " + os.path.join(pathf, f) + " to: " + folder)
                    shutil.move(os.path.join(pathf, f), folder)
                else:
                    print(ext.upper() + " file " + os.path.join(pathf, f) + " already existed in " + folder)
            # Copio la imagen principal con el nombre del fichero .max, dentro de la carpeta principal
            if not os.path.isfile(os.path.join(folder, filename) + ext_jpg):
                shutil.copyfile(os.path.join(folder, folder) + ext_jpg, os.path.join(folder, filename) + ext_jpg)


# Comienza el programa

os.chdir(sys.argv[1])

print()
print("Processing " + sys.argv[1])
print()

for f in os.listdir():
    print("Processing " + f)
    # Si es una carpeta
    if os.path.isdir(f):
        filename = f
        ext = ""
    # Si es un fichero
    else:
        (filename, ext) = os.path.splitext(f)
        # Si no es .zip o .rar, no me interesa, voy a mirar el siguiente
        if not (ext.lower() == ".zip" or ext.lower() == ".rar"):
            continue
    #Si hay fichero de imagen con el mismo nombre que la carpeta o fichero comprimido
    print("Processing " + filename)
    ext_jpg = findImage(filename)
    if ext_jpg != "none":
        #Si es un fichero comprimido
        if ext.lower() == ".zip" or ext.lower() == ".rar":
            desComp(filename, ext)
        #Copia el fichero de imagen dentro de la carpeta
        if not os.path.isfile(os.path.join(filename, filename) + ext_jpg):
            print("Copying IMAGE file " + filename + ext_jpg + " into folder " + filename)
            shutil.copyfile(filename + ext_jpg, os.path.join(filename, filename) + ext_jpg)
        else:
            print("IMAGE file " + filename + ext_jpg + " already existed in folder " + filename)
        #Procesa la carpeta descomprimida
        procFolder(filename, filename, ext_jpg)
        #Elimina la imagen de la carpeta principal, una vez procesada la subcarpeta
        if os.path.isfile(filename + ext_jpg):
            print("Removing IMAGE file " + filename + ext_jpg)
            os.remove(filename + ext_jpg)
        print()

sys.exit()
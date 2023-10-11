import cv2
from os import listdir,remove,rename,mkdir,path
from PIL import Image,ImageChops
import numpy as np
from sys import argv

def TakeElement(elemento,retiravel):
    return elemento[:elemento.find(retiravel)]

def FrameOrganizer(Path_Do_Arquivo):
    teste = listdir(Path_Do_Arquivo)
    lista = []
    for x in teste:
        x = TakeElement(x,".jpg")
        lista.append(int(x))
    lista.sort()
    nova_lista = []
    for x in lista:
        x = Path_Do_Arquivo+"\\"+str(x)+".jpg"
        nova_lista.append(x)
    return nova_lista
    
def Help_Rename(elemento):
    if ("(" in elemento or ")" in elemento):
        variavel = elemento[elemento.find("("):]
        variavel = variavel[:variavel.find(".jpg")]
        variavel = variavel[1:-1]
        item = str(int(variavel) + 1)
        final = elemento.replace("("+variavel+")","("+item+")")
        return final
    else:
        Um = elemento[elemento.find(".jpg"):]
        variavel = " (1)"+Um
        elemento = elemento.replace(Um,variavel)
        return (elemento)

def Compare_Density(FirsImage,SecondImage): #Compara a densidade das duas imagens
    imagem1 = Image.open(FirsImage)
    imagem2 = Image.open(SecondImage)
    subtracao = ImageChops.subtract(imagem1,imagem2,scale=1,offset=0)
    image_data = np.asarray(subtracao)
    variavel_contadora = 0
    diferente = 0
    for i in range(len(image_data)):
        for j in range(len(image_data[0])):
            #arquivo.write(str(image_data[i][j]))
            #print(image_data[i][j])
            if(str(image_data[i][j]) == "[0 0 0]"):
                variavel_contadora += 1
            else:
                diferente += 1
    print("Positivo "+str(variavel_contadora)+" Diferente "+str(diferente))
    return ((variavel_contadora/(variavel_contadora+diferente))*100)


def Partial_Compress(Path_Do_Arquivo):
    lista = FrameOrganizer(Path_Do_Arquivo)
    x = 0
    while (x + 1 < len(lista)):
        print("Densidade "+str(Compare_Density(lista[x],lista[x+1])))
        if (Compare_Density(lista[x],lista[x+1]) >= 92.000):
            remove(lista[x+1])
            lista.remove(lista[x+1])
            rename(lista[x],Help_Rename(lista[x]))
            lista[x] = Help_Rename(lista[x])
        else:
            x += 1
    print(listdir(Path_Do_Arquivo))

def Bound(elemento1,primeiro,segundo):
    try:
        variavel = elemento1[elemento1.find(primeiro) + len(primeiro):]
        return variavel[:variavel.find(segundo)]
    except:
        return ""

def SeparationThing(Name):
    variavel = list(reversed(Name))
    algo = "".join(variavel)
    valor = algo[:algo.find("\\")]
    valor = "".join(list(reversed(valor))) #String reversa
    resposta = Name[:Name.find("\\") + len("\\")]
    return valor,resposta

def Funcao_Renomeia(Nome_Do_Arquivo):
    elemento1,elemento2 = SeparationThing(Nome_Do_Arquivo)
    algo = elemento1
    resultado = Bound(algo,"(",")")
    lista = []
    if (resultado == ""):
        resultado = 0
    for x in range(int(resultado) + 1):
        if (x == 0):
            lista.append(elemento2+algo.replace(" ("+resultado+")",""))
        else:
            variavel = algo[:algo.find("(")]
            variavel = int(variavel)
            lista.append(elemento2+str(variavel + x) + ".jpg")
    return lista

def Partial_Decompress(Nome_Do_Arquivo):
    variavel = cv2.imread(Nome_Do_Arquivo)
    lista = Funcao_Renomeia(Nome_Do_Arquivo)
    for x in lista:
        cv2.imwrite(x,variavel)

def Decompress(Nome_Do_Arquivo):
    if (Nome_Do_Arquivo.endswith("\\")):
        Nome_Do_Arquivo = Nome_Do_Arquivo.replace("\\","",1)
    variavel = listdir(Nome_Do_Arquivo)
    for x in variavel:
        if ("(" in (Nome_Do_Arquivo+"\\"+x)):
            Partial_Decompress(Nome_Do_Arquivo+"\\"+x)
            remove(Nome_Do_Arquivo+"\\"+x)
    print("Descompresso")


def MovieFunction(Path_Do_Arquivo,Nome_Do_MP4,FPS):
    teste = listdir(Path_Do_Arquivo)
    lista = []
    for x in teste:
        x = TakeElement(x,".jpg")
        lista.append(int(x))
    lista.sort()
    nova_lista = []
    for x in lista:
        x = Path_Do_Arquivo+"\\"+str(x)+".jpg"
        nova_lista.append(x)
    array_de_imagens = []
    #parte de salvamento do video
    imagem = cv2.imread(nova_lista[0])
    height,width,layers = imagem.shape
    size = (width,height)
    for x in nova_lista:
        imagem = cv2.imread(x)
        array_de_imagens.append(imagem)
    out = cv2.VideoWriter(Nome_Do_MP4,cv2.VideoWriter_fourcc(*'DIVX'),FPS,size)
    for x in array_de_imagens:
        out.write(x)
    out.release()

def Decompress_Video(Path_Do_Arquivo,FPS,Nome_Do_Arquivo_Final):
    Decompress(Path_Do_Arquivo)
    if(".mp4" in Nome_Do_Arquivo_Final):
        Nome_Do_Avi = Nome_Do_Avi.replace(".mp4",".avi")
    elif (Nome_Do_Arquivo_Final[-4:] != ".avi"):
        Nome_Do_Arquivo_Final = Nome_Do_Arquivo_Final + ".avi"
    MovieFunction(Path_Do_Arquivo,Nome_Do_Arquivo_Final,FPS)

def VideoToFrames(Path,Nome):
    capture = cv2.VideoCapture(Nome)
    variavel = 0
    while (True):
        ret,frame = capture.read()
        Parcial = str(variavel) + ".jpg"
        cv2.imwrite(Path+"\\"+Parcial,frame)
        variavel += 1
        if(ret == False):
            break
    capture.release()
    cv2.destroyAllWindows()

def Compress(Nome_Do_Avi):
    Nome_Real = Nome_Do_Avi
    video = cv2.VideoCapture(Nome_Do_Avi)
    fps = video.get(cv2.CAP_PROP_FPS)
    while ("(" in Nome_Do_Avi or ")" in Nome_Do_Avi):
        Nome_Do_Avi = Nome_Do_Avi.replace("(","")
        Nome_Do_Avi = Nome_Do_Avi.replace(")","")
    video.release()
    if(".mp4" in Nome_Do_Avi or ".avi" in Nome_Do_Avi or ".mkv" in Nome_Do_Avi or ".webm" in Nome_Do_Avi):
        Nome_Do_Avi = Nome_Do_Avi.replace(".mp4","")
        Nome_Do_Avi = Nome_Do_Avi.replace(".avi","")
        Nome_Do_Avi = Nome_Do_Avi.replace(".mkv","")
        Nome_Do_Avi = Nome_Do_Avi.replace(".webm","")
    mkdir(Nome_Do_Avi+" Comprimido")
    Path_Do_Diretorio = Nome_Do_Avi+" Comprimido"
    print ("Comprimindo...")
    VideoToFrames(Path_Do_Diretorio,Nome_Real)
    Partial_Compress(Path_Do_Diretorio)
    print("Arquivo Comprimido\n\n\n")

if __name__ == "__main__":
    if(len(argv) == 3):
        if(argv[1] == "-C" or argv[1] == "-c"):
            try:
                
                if(path.exists(argv[2])):
                    Nome_Do_Arquivo = argv[2]
                    Compress(Nome_Do_Arquivo)
            except:
                #print("\n\nPath de arquivo ilegal ou nao presente em diretorio especificado\n\n")
                exit()
        else:
            print("Parametro nao interpretado pelo sistema")
            exit()
    elif(len(argv) == 5):
        if(argv[1] == "-D" or argv[1] == "-d"):
            if(path.exists(argv[2])):
                if(argv[3].isdigit()):
                    if(len(argv[4]) > 0):
                        Nome_Video = argv[2]
                        FPS = int(argv[3])
                        Arquivo_Final = argv[4]
                        Decompress_Video(Nome_Video,FPS,Arquivo_Final)
                    else:
                        print("Nome de arquivo final improprio")
                else:
                    print("Valor Numerico FPS Nao eh numerico")
            else:
                print("\n\nPath de arquivo ilegal ou nao presente em diretorio especificado\n\n")    
        else:
            print("Parametro nao interpretado pelo sistema")

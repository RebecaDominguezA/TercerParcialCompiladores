import os
import sys

# Definición de automata
estados_nfa = {
    #Estado inicial
    'q0': { "'": {'q1'},'"': {'q2'},'Number': {'q3'},'symbol': {'q7'},
           #Puede tratarse de PR
           'a': {'q8'},'e': {'q9'}, 'f': {'q10'}, 'm': {'q500.'}, 'i': {'q12'},
           'n': {'q13'}, 'p': {'q14'}, 'r': {'q15'}, 't': {'q16'},'v': {'q17'},
           'w': {'q18'},'o': {'q25'}," ": {'q0',},"any": {'q500',} 
        },
    
    #Palabras reservadas
    'q8': {'n': {'q19'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}}, 
    'q19': {'d': {'q20'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}}, 
    'q20': {"symbol": {'q7'},'Number': {'q500'},"'": {'q1'},'"': {'q2'}," ": {'q0'},'any': {'q500'}}, #AND
    
    'q9': {'l': {'q21'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q21': {'s': {'q22'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q22': {'e': {'q23'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q23': {"symbol": {'q7'},'Number': {'q500'},"'": {'q1'},'"': {'q2'}," ": {'q0'},'any': {'q500'}}, #ELSE Y FALSE y TRUE Y WHILE
    
    'q10': {'a': {'q24'},'o': {'q25'},'u': {'q27'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},#FA o FO
    'q24': {'l': {'q21'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},#Retorna a q21 si todo va bien
    'q25': {'r': {'q26'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q26': {"symbol": {'q7'},'Number': {'q500'},"'": {'q1'},'"': {'q2'}," ": {'q0'},'any': {'q500'}}, #FOR y OR Y VAR
    
    'q27': {'n': {'q28'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q28': {"symbol": {'q7'},'Number': {'q500'},"'": {'q1'},'"': {'q2'}," ": {'q0'},'any': {'q500'}}, #FUN y RETURN
    
    'q12': {'f': {'q29'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q29': {"symbol": {'q7'},'Number': {'q500'},"'": {'q1'},'"': {'q2'}," ": {'q0'},'any': {'q500'}}, #IF
    
    'q13': {'u': {'q30'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q30': {'l': {'q31'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q31': {'l': {'q32'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q32': {"symbol": {'q7'},'Number': {'q500'},"'": {'q1'},'"': {'q2'}," ": {'q0'},'any': {'q500'}}, #NULL
    
    'q14': {'r': {'q33'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q33': {'i': {'q34'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q34': {'n': {'q35'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q35': {'t': {'q36'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q36': {"symbol": {'q7'},'Number': {'q500'},"'": {'q1'},'"': {'q2'}," ": {'q0'},'any': {'q500'}}, #PRINT
    
    'q15': {'e': {'q37'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q37': {'t': {'q38'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q38': {'u': {'q39'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q39': {'r': {'q27'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},#mandamos a q28 pues termina en n
    
    'q16': {'r': {'q40'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q40': {'u': {'q41'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q41': {'e': {'q23'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},#mandamos a q23 pues termina en e
    
    'q17': {'a': {'q42'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q42': {'r': {'q26'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},#mandamos a q26 pues termina en r
    
    'q18': {'h': {'q43'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q43': {'i': {'q44'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q44': {'l': {'q45'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},
    'q45': {'e': {'q23'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'any': {'q500'}},#mandamos a q23 pues termina en e
    
    
    #Cadenas
    'q1': {'any': {'q2'},'Number': {'q2'},'symbol': {'q2'}, "'": {'q0'}},
    'q2': {'any': {'q2'},'Number': {'q2'},'symbol': {'q2'}, '"': {'q0'}},
    
    #Numeros
    'q3': {'Number': {'q3'}, "^": {'q4'}, ".": {'q5'},"symbol": {'q7'}," ": {'q0'}, "any": {'q500'},   "'": {'q0'},'"': {'q0'}},#Entero
    'q4': {'Number': {'q4'}, " ": {'q0'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}, "any": {'q500'}},#Exponenciales
    'q5': {'Number': {'q5'}, " ": {'q0'}, "symbol": {'q7'},"'": {'q0'},'"': {'q0'}, "any": {'q500'}},#Decimales
    
    #Simbolos , empezamos en q60
    'q7': {'symbol': {'q60'}, " ": {'q0'},"'": {'q0'},'"': {'q0'},'Number': {'q3'},
           'a': {'q8'},'e': {'q9'}, 'f': {'q10'}, 'm': {'q500'}, 'i': {'q12'},
           'n': {'q13'}, 'p': {'q14'}, 'r': {'q15'}, 't': {'q16'},'v': {'q17'},
           'w': {'q18'},'o': {'q25'},
           'any': {'q500'}},
    'q60': {},#Si se llega a q60, se hace siempre una comparacion de que simbolo fue el anterior. Y se sacan conclusiones. Cso 1,2,3,4,5,6
    
    #Identificadores en 500
    'q500': {'symbol': {'q7'},"'": {'q0'},'"': {'q0'}," ": {'q0'},'Number': {'q500'},'any': {'q500'}}
}

# Diccionario de simbolos a reconocer
simbolos = ["<", ">", "!", "=", "+", "-", "*", "/", "{", "}", "(", ")", ",", ".", ";"]
#Diccionario de palabras a reconocer
palabras_reservadas=["and","else","false","for","fun","if","null","or","print","return","true","var","while"]

#Diccionario de letras a reconocer
PosiblesPR=["a", "e", "f", "h", "i", "l", "o", "p", "r", "s", "t", "u", "v" ,"w","n"]

#Vocabulario
Vocabulario=["a","b","c","d","e", "f", "g", "h", "i", "j", "k", "l","m","n","o","p","q","r","s","t", "u", "v" ,"w","x",
             "y","z","<", ">", "!", "=", "+", "-", "*", "/", "{", "}", "(", ")", ",", ".", ";",":",
             "A","B","C","D","E", "F", "G", "H", "I", "J", "K", "L","Ã","¡","M","N","O","P","Q","R","S","T", "U", "V" ,"W","X",
             "Y","Z"," "]

#Estados Finales PR
estados_FPR=["q20","q23","q26","q28","q29","q32","q36"]
#Estados FINALES para String
estados_FString=["q1","q2"]

# Definición de diccionario de simbolos
nombres_simbolos = {
    '<': 'MENOR_QUE', # se trata del simbolo <
    '>': 'MAYOR_QUE', # se trata del simbolo >
    '!': 'BANG', # se trata del simbolo !
    '=': 'IGUAL', # se trata del simbolo =
    '<=': 'MENOR_IGUAL_QUE', # se trata del simbolo <=
    '>=': 'MAYOR_IGUAL_QUE', # se trata del simbolo >=
    '!=': 'DIFERENTE_QUE', # se trata del simbolo !=
    '==': 'IGUAL_IGUAL', # se trata del simbolo ==
    '+': 'SUMA', # se trata del simbolo +
    '-': 'RESTA', # se trata del simbolo -
    '*': 'ESTRELLA', # se trata del simbolo *
    '{': 'LLAVE_ABRE', # se trata del simbolo {
    '}': 'LLAVE_CIERRA', # se trata del simbolo }
    '(': 'PARENTESIS_ABRE', # se trata del simbolo (
    ')': 'PARENTESIS_CIERRA', # se trata del simbolo )
    ',': 'COMA', # se trata del simbolo ,
    '.': 'PUNTO', # se trata del simbolo .
    ';': 'PUNTO_Y_COMA', # se trata del simbolo ;
    '/': 'SLASH' # se trata del simbolo /
}

class MisTokens:
    def __init__(self, tipo, valor1, valor2):
        self.tipo = tipo
        self.valor1 = valor1
        self.valor2 = valor2

# Lista para almacenar objetos
lista_objetos = []

def evaluar_simbolo(caracter, simbolos):#Esta evaluador me dira si la letra de entrada pertenece al diccionario de simbolos por reconocer
    if caracter in simbolos:
        return "symbol"
    else:
        return None  # El carácter no es un símbolo

def evaluar_numero(caracter):#Esta evaluador me dira si la letra de entrada pertenece al diccionario de numeros por reconocer
    if caracter.isdigit():
        return "Number"
    else:
        return None  # Opcional: puedes devolver None si el carácter no es un dígito

def evaluar_caracter_any(caracter):
    if caracter == '"' or caracter == "'":
        return caracter
    else:
        return "any"


def interprete(caracter, simbolos,PosiblesPR,guardar_como_any):
    if caracter in simbolos:
        return "symbol"
    elif caracter.isdigit():
        return "Number"
    elif caracter == '"' or caracter == "'":
        return caracter
    else:
        if guardar_como_any==1:
            if caracter in Vocabulario:
                return "any"
            else:
                print("Analisis:")
                for objeto in lista_objetos:
                    print("<"+objeto.tipo + ","+objeto.valor1+","+objeto.valor2+">")
                sys.exit("Error: No se reconoce el caracter "+caracter+".")
        elif caracter==" ":
            #print("Caso vacio")
            return caracter
        else:
            return caracter
            #if (caracter in PosiblesPR):
                #return caracter
            #else:
                #return "any"
    
def analizar_codigo(ruta_archivo,caso):
    #print(ruta_archivo)
    if caso==1:
        
        try:
            with open(ruta_archivo, "r") as archivo:
                contador_caracteres = 0
                total_caracteres=0
                memoria=""
                # Utilizamos la función readlines() para leer todas las líneas del archivo en una lista.
                lineas = archivo.readlines()
                #for linea in lineas:
                    #print(linea)LEXEMA ACTUAL
                    
                # Abre el archivo en modo lectura
                with open(ruta_archivo, "r") as archivo:
                    # Lee el archivo caracter por caracter
                    while True:
                        caracter = archivo.read(1)  # Lee un caracter
                        if not caracter:
                            break  # Fin del archivo
                        contador_caracteres += 1
                total_caracteres=contador_caracteres
                
                #print("caracteres"+ str(total_caracteres))
                estado_inicial="q0"
                estado_anterior=""
                estado_actual=estado_inicial
                BanderaT1=0
                BanderaT2=0
                contador_caracteres = 1
                guardar_como_any=0
                lexema=""
                caracter_esperado=""
                inicio=1
                primero=1
                segundo=0
                # Abre el archivo en modo lectura
                with open(ruta_archivo, "r") as archivo:
                    
                    # Lee el archivo caracter por caracter
                    while True:
                        caracter = archivo.read(1)  
                        if not caracter:
                            if BanderaT2==1:
                                print("Antes de cerrar por Error se imprime objetos que se lograron guardar.")
                                for objeto in lista_objetos:
                                    print("<"+objeto.tipo + ","+objeto.valor1+","+objeto.valor2+">")
                                sys.exit("Error: No se cerro comentario multilinea.")
                            elif estado_actual=="q2" or estado_actual=="q1":
                                print("Antes de cerrar por Error: se imprime objetois que se lograron guardar")
                                for objeto in lista_objetos:
                                    print("<"+objeto.tipo + ","+objeto.valor1+","+objeto.valor2+">")
                                sys.exit("Error: No se cerro cadena en el ultimo token String.")
                            #print("Guardamos la ultima expresion si es que hay")
                            #print(estado_anterior)
                            #print(estado_actual)
                            #print(estado_siguiente)
                            
                            if estado_siguiente =="q0":
                                #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                                #print("Estamos a punto de guardar YA QUE ESTADO SIG ES Q0:"+lexema)
                                #print("E actual:"+estado_actual)
                                if estado_actual in estados_FPR:
                                    #print("Estado actual pertenece a estados finales de reservadas")
                                    if(caracter==" "):
                                        #print("quitamos espacio")
                                        lexema = lexema[:-1]
                                    else:
                                        lexema = lexema[:-1] 
                                        memoria+=caracter
                                    #print(lexema+"in reservadas")
                                    if lexema in palabras_reservadas:
                                        #print("yes")
                                        objeto=MisTokens(lexema.upper(),lexema,"null")
                                        lista_objetos.append(objeto)
                                        guardar_como_any=0
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    else:
                                        #print("El objeto guardado fue:"+lexema)
                                        #input("Que paso")
                                        objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                        lista_objetos.append(objeto)
                                        guardar_como_any=0
                                elif estado_actual in estados_FString:
                                    objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                                    lista_objetos.append(objeto)
                                    guardar_como_any=0
                                elif estado_actual =="q3":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    #print("se guardo"+lexema)
                                    objeto=MisTokens("ENTERO",lexema,lexema)
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual =="q4":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual =="q5":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    valor_decimal = float(lexema)
                                    objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual =="q7":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    #print("guardamos:"+lexema)
                                    objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual=="q500":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual=="q0":
                                    
                                    #verificamos de donde viene
                                    #print("estado anterior:"+estado_anterior)
                                    #if estado_anterior==
                                    #Hubo un espacio inecesario
                                    lexema=""
                            
                            elif (estado_siguiente=="q2" or estado_siguiente=="q1") and (estado_actual in estados_FPR):
                                
                                lexema = lexema[:-1] 
                                memoria+=caracter
                                #print(lexema+"in reservadas")
                                if lexema in palabras_reservadas:
                                    #print("yes")
                                    objeto=MisTokens(lexema.upper(),lexema,"null")
                                    lista_objetos.append(objeto)
                                    guardar_como_any=1
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                else:
                                    #print("El objeto guardado fue:"+lexema)
                                    #input("Que paso")
                                    objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                    lista_objetos.append(objeto)
                                    guardar_como_any=1
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                            
                            elif estado_siguiente=="q500":
                                #print("En q500")
                                #Es posiblemente id, asi que verificamos
                                #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                                #print("Estamos a punto de guardar, recibimos algo y venimos un estado qn:"+lexema)
                                #print("E actual:"+estado_actual)
                                if estado_actual in estados_FPR:
                                    #print("Estado actual pertenece a estados finales de reservadas")
                                    if(caracter==" "):
                                        #print("quitamos espacio")
                                        lexema = lexema[:-1]
                                    else:
                                        lexema = lexema[:-1] 
                                        memoria+=caracter
                                    #print(lexema+"in reservadas")
                                    if lexema in palabras_reservadas:
                                        #print("yes")
                                        objeto=MisTokens(lexema.upper(),lexema,"null")
                                        lista_objetos.append(objeto)
                                        guardar_como_any=0
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    else:
                                        #print("El objeto guardado fue:"+lexema)
                                        input("Que paso")
                                        objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                        lista_objetos.append(objeto)
                                        guardar_como_any=0
                                elif estado_actual in estados_FString:
                                    objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                                    lista_objetos.append(objeto)
                                    guardar_como_any=0
                                elif estado_actual =="q3":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    #print("se guardo"+lexema)
                                    objeto=MisTokens("ENTERO",lexema,lexema)
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual =="q4":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual =="q5":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    valor_decimal = float(lexema)
                                    objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual =="q7":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    #print("guardamos:"+lexema)
                                    objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual=="q500":
                                    #lexema = lexema[:-1]
                                    memoria+=caracter
                                    objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual=="q0":
                                    #verificamos de donde viene
                                    print("")
                                    #if estado_anterior==
                                    #Hubo un espacio inecesario
                                    #lexema=""
                            
                                
                                guardar_como_any=1
                            elif estado_siguiente=="q60":
                                #Se escoge opciones de 6 casos
                                if caracter=="=" and estado_anterior=="q7":
                                    objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                    lista_objetos.append(objeto)
                                    guardar_como_any=0
                                    
                                elif caracter=="/":
                                    BanderaT1=1
                                elif caracter=="*":
                                    BanderaT2=1

                            elif estado_siguiente=="q7":
                                #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                                #print("Estamos a punto de guardar, recibimos un simbolo y venimos un estado qn:"+lexema)
                                #print("E actual:"+estado_actual)
                                if estado_actual in estados_FPR:
                                    #print("Estado actual pertenece a estados finales de reservadas")
                                    if(caracter==" "):
                                        #print("quitamos espacio")
                                        lexema = lexema[:-1]
                                    else:
                                        lexema = lexema[:-1] 
                                        memoria+=caracter
                                    #print(lexema+"in reservadas")
                                    if lexema in palabras_reservadas:
                                        #print("yes")
                                        objeto=MisTokens(lexema.upper(),lexema,"null")
                                        lista_objetos.append(objeto)
                                        guardar_como_any=0
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    else:
                                        #print("El objeto guardado fue:"+lexema)
                                        input("Que paso")
                                        objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                        lista_objetos.append(objeto)
                                        guardar_como_any=0
                                elif estado_actual in estados_FString:
                                    objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                                    lista_objetos.append(objeto)
                                    guardar_como_any=0
                                elif estado_actual =="q3":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    #print("se guardo"+lexema)
                                    objeto=MisTokens("ENTERO",lexema,lexema)
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                    
                                elif estado_actual =="q4":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual =="q5":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    valor_decimal = float(lexema)
                                    objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual =="q7":
                                    objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                    lista_objetos.append(objeto)
                                    guardar_como_any=0
                                elif estado_actual=="q500":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual=="q0":
                                    #verificamos de donde viene
                                    print("")
                                    #if estado_anterior==
                                    #Hubo un espacio inecesario
                                    #lexema=""

                            else:
                                if estado_actual=="q7":
                                    #print("Estamos a punto de guardar, venimos de simbolo hacia opciones:"+lexema)
                                    #print("E actual:"+estado_actual)
                                    #if caracter not in estados_nfa.get(estado_actual, {}):
                                    if caracter in PosiblesPR:
                                        lexema = lexema[:-1]
                                        memoria+=caracter
                                        #print("guardamos:"+lexema)
                                        objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                        lista_objetos.append(objeto)
                                        if caracter==" ":
                                            lexema=""
                                            memoria=""
                                        else:   
                                            if memoria:
                                                lexema=memoria
                                                memoria=""
                                            else:
                                                lexema=""
                                        guardar_como_any=0
                                
                                elif estado_actual in estados_FPR:
                                    #print("Estado actual pertenece a estados finales de reservadas")
                                    if(caracter==" "):
                                        #print("quitamos espacio")
                                        lexema = lexema[:-1]
                                    else:
                                        #lexema = lexema[:-1] 
                                        memoria+=caracter
                                    #print(lexema+"in reservadas")
                                    if lexema in palabras_reservadas:
                                        #print("yes")
                                        objeto=MisTokens(lexema.upper(),lexema,"null")
                                        lista_objetos.append(objeto)
                                        guardar_como_any=0
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    else:
                                        #print("El objeto guardado fue:"+lexema)
                                        #input("Que paso")
                                        objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                        lista_objetos.append(objeto)
                                        guardar_como_any=0
                                
                            break  # Fin del archivo
                        elif BanderaT1==1:# Comentario 1
                            if caracter=="\n":
                                #print("Caracter de salto de linea. Se vuele a leer")
                                #print("t1estado_anterior"+estado_anterior)
                                #print("t1estado actual:"+estado_actual)
                                #print("t1estado siguiente:"+estado_siguiente)
                                lexema=""
                                BanderaT1=0
                                guardar_como_any=0
                                estado_actual=estado_inicial
                        elif BanderaT2==1:# Comentario 2, no hacemos nada hasta detectar cierre
                            if primero==1:
                                if caracter=="*":
                                    primero=0
                                    segundo=1
                                    caracter_esperado="/"
                            elif segundo==1:
                                if caracter==caracter_esperado:
                                    #Reset desde bandera
                                    BanderaT2=0
                                    primero=1
                                    segundo=0
                                    caracter_esperado=""
                                    guardar_como_any=0
                                    lexema=""
                                    estado_actual=estado_inicial
                                    #print("t2estado_anterior"+estado_anterior)
                                    #print("t2estado actual:"+estado_actual)
                                    #print("t2estado siguiente:"+estado_siguiente)
                                else:
                                    #Reset de lectura
                                    primero=1
                                    segundo=0
                                    caracter_esperado=""
                                
                        else:
                            #print("Caracter actual--:"+caracter)
                            if caracter=="\n":
                                guardar_como_any=0
                                #print("estado_anterior"+estado_anterior)
                                #print("estado actual:"+estado_actual)
                                estado_siguiente=estado_inicial
                                #print("estado siguiente:"+estado_siguiente)
                                #print("Caracter de salto de linea implicito.")
                                #print("LEXEMA ACTUAL:"+lexema)
                                if estado_actual in estados_FPR:
                                    #print("Estado actual pertenece a estados finales de reservadas")
                                    if(caracter==" "):
                                        #print("quitamos espacio")
                                        lexema = lexema[:-1]
                                    else:
                                        lexema = lexema[:-1] 
                                        memoria+=caracter
                                    #print(lexema+"in reservadas")
                                    if lexema in palabras_reservadas:
                                        #print("yes")
                                        objeto=MisTokens(lexema.upper(),lexema,"null")
                                        lista_objetos.append(objeto)
                                        guardar_como_any=0
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    else:
                                        #print("El objeto guardado fue:"+lexema)
                                        #input("Que paso")
                                        objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                        lista_objetos.append(objeto)
                                        guardar_como_any=0
                                elif estado_actual in estados_FString:
                                    for objeto in lista_objetos:
                                        print("<"+objeto.tipo + ","+objeto.valor1+","+objeto.valor2+">")
                                    sys.exit("Error: No se cerro STRING: "+lexema+"")
                                    #objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                                    #lista_objetos.append(objeto)
                                    #guardar_como_any=0
                                elif estado_actual =="q3":
                                    #lexema = lexema[:-1]
                                    memoria+=caracter
                                    #print("se guardo"+lexema)
                                    objeto=MisTokens("ENTERO",lexema,lexema)
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual =="q4":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual =="q5":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    valor_decimal = float(lexema)
                                    objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual =="q7":
                                    #lexema = lexema[:-1]
                                    memoria+=caracter
                                    #print("guardamos:"+lexema)
                                    objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual=="q500":
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                elif estado_actual=="q0":
                                    #verificamos de donde viene
                                    #print("estado anterior:"+estado_anterior)
                                    #if estado_anterior==
                                    #Hubo un espacio inecesario
                                    lexema=""
                            
                                
                                
                                
                                lexema=""
                                estado_actual=estado_inicial
                                if estado_actual=="q2" or estado_actual=="q1":
                                    sys.exit("Error: No se cerro cadena.")                           
                            else:
                                lexema+=caracter
                                #print(caracter)
                                #print(estado_actual)
                                #print("LEXEMA ACTUAL:"+lexema)
                                #En dicha variable guardaremos si se trata de, Number, symbol, ", ', posible PR, o any (candidata a ID)
                                caso=""
                                #Debemos evaluar de que tipo de letra se trata, llamamos a evaluadores/Interpretes
                                if caracter in estados_nfa.get(estado_actual, {}):
                                    guardar_como_any=0
                                else:
                                    guardar_como_any=1
                                caso=interprete(caracter,simbolos,PosiblesPR,guardar_como_any)
                                #print("caso:"+caso)
                                if inicio==1:
                                    inicio=1
                                    if caso == "'":
                                        #estado_anterior=estado_actual
                                        estado_siguiente = next(iter(estados_nfa[estado_actual][caso]))
                                        guardar_como_any=1
                                    elif caso== '"':
                                        #estado_anterior=estado_actual
                                        estado_siguiente = next(iter(estados_nfa[estado_actual][caso]))
                                        guardar_como_any=1
                                    elif caso=="Number":
                                        #estado_anterior=estado_actual
                                        estado_siguiente = next(iter(estados_nfa[estado_actual][caso]))
                                        guardar_como_any=1
                                    elif caso=="symbol":
                                        #estado_anterior=estado_actual
                                        estado_siguiente = next(iter(estados_nfa[estado_actual][caso]))
                                    else:
                                        #estado_anterior=estado_actual
                                        estado_siguiente = next(iter(estados_nfa[estado_actual][caso]))
                                    
                                    #print("Estado actual:"+estado_actual)
                                    #print("Estado siguiente:"+estado_siguiente)


                                    if estado_siguiente =="q0":
                                        #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                                        #print("Estamos a punto de guardar YA QUE ESTADO SIG ES Q0:"+lexema)
                                        #print("E actual:"+estado_actual)
                                        if estado_actual in estados_FPR:
                                            #print("Estado actual pertenece a estados finales de reservadas")
                                            if(caracter==" "):
                                                #print("quitamos espacio")
                                                lexema = lexema[:-1]
                                            else:
                                                lexema = lexema[:-1] 
                                                memoria+=caracter
                                            #print(lexema+"in reservadas")
                                            if lexema in palabras_reservadas:
                                                #print("yes")
                                                objeto=MisTokens(lexema.upper(),lexema,"null")
                                                lista_objetos.append(objeto)
                                                guardar_como_any=0
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            else:
                                                #print("El objeto guardado fue:"+lexema)
                                                #input("Que paso")
                                                objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                                lista_objetos.append(objeto)
                                                guardar_como_any=0
                                        elif estado_actual in estados_FString:
                                            #lexema = lexema[:-1]
                                            memoria+=caracter
                                            #print("guardamos:"+lexema)
                                            objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                    lexema=""
                                                else:
                                                    lexema=""
                                            
                                            guardar_como_any=0
                                        elif estado_actual =="q3":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            #print("se guardo"+lexema)
                                            objeto=MisTokens("ENTERO",lexema,lexema)
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual =="q4":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual =="q5":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            valor_decimal = float(lexema)
                                            objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual =="q7":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            #print("guardamos:"+lexema)
                                            objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual=="q500":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual=="q0":
                                            #verificamos de donde viene
                                            #print("estado anterior:"+estado_anterior)
                                            #if estado_anterior==
                                            #Hubo un espacio inecesario
                                            lexema=""
                                        
                                        else:
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                            
                                            
                                            
                                    elif (estado_siguiente=="q2" or estado_siguiente=="q1") and (estado_actual in estados_FPR):
                                        lexema = lexema[:-1] 
                                        memoria+=caracter
                                        #print(lexema+"in reservadas")
                                        if lexema in palabras_reservadas:
                                            #print("yes")
                                            objeto=MisTokens(lexema.upper(),lexema,"null")
                                            lista_objetos.append(objeto)
                                            guardar_como_any=1
                                            if memoria:
                                                lexema=memoria
                                                memoria=""
                                            else:
                                                lexema=""
                                        else:
                                            #print("El objeto guardado fue:"+lexema)
                                            #input("Que paso")
                                            objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                            lista_objetos.append(objeto)
                                            guardar_como_any=1
                                            if memoria:
                                                lexema=memoria
                                                memoria=""
                                            else:
                                                lexema=""
                                    elif estado_siguiente=="q3":
                                        if estado_actual=="q7":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            #print("guardamos:"+lexema)
                                            objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                    elif estado_siguiente=="q500":
                                        #print("En q500")
                                        #Es posiblemente id, asi que verificamos
                                        #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                                        #print("Estamos a punto de guardar, recibimos algo y venimos un estado qn:"+lexema)
                                        #print("E actual:"+estado_actual)
                                        if (estado_actual in estados_FPR) and ((caso!="any") and(caso!="Number")):
                                            #print("Estado actual pertenece a estados finales de reservadas")
                                            if(caracter==" "):
                                                #print("quitamos espacio")
                                                lexema = lexema[:-1]
                                            else:
                                                lexema = lexema[:-1] 
                                                memoria+=caracter
                                            #print(lexema+"in reservadas")
                                            if lexema in palabras_reservadas:
                                                #print("yes")
                                                objeto=MisTokens(lexema.upper(),lexema,"null")
                                                lista_objetos.append(objeto)
                                                guardar_como_any=0
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            else:
                                                #print("El objeto guardado fue:"+lexema)
                                                input("Que paso")
                                                objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                                lista_objetos.append(objeto)
                                                guardar_como_any=0
                                        elif estado_actual in estados_FString:
                                            objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                                            lista_objetos.append(objeto)
                                            guardar_como_any=0
                                        elif estado_actual =="q3":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            #print("se guardo"+lexema)
                                            objeto=MisTokens("ENTERO",lexema,lexema)
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual =="q4":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual =="q5":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            valor_decimal = float(lexema)
                                            objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual =="q7":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            #print("guardamos:"+lexema)
                                            objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual=="q0":
                                            #verificamos de donde viene
                                            print("")
                                            #if estado_anterior==
                                            #Hubo un espacio inecesario
                                            #lexema=""
                                        
                                        elif estado_actual=="q500":
                                            #print("Sigue con any")
                                            guardar_como_any=1
                                        
                                        
                                    
                                        
                                        guardar_como_any=1
                                    elif estado_siguiente=="q60":
                                        #Se escoge opciones de 6 casos
                                        #print("estado anterior"+estado_anterior)
                                        if caracter=="=" and ((estado_anterior=="q7") or(estado_actual=="q7")):
                                            
                                            objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                            lista_objetos.append(objeto)
                                            estado_siguiente=estado_inicial
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                    
                                                else:
                                                    lexema=""
                                            
                                            guardar_como_any=0
                                        elif caracter=="/":
                                            BanderaT1=1
                                            estado_siguiente=estado_inicial
                                        elif caracter=="*":
                                            BanderaT2=1
                                            estado_siguiente=estado_inicial
                                        
                                        else:
                                            #es otro simbolo
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            #print("lexema"+lexema)
                                            objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                    
                                                else:
                                                    lexema=""
                                            
                                            guardar_como_any=0
                                            estado_siguiente="q7"
                                    elif estado_siguiente=="q7":
                                        #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                                        #print("Estamos a punto de guardar, recibimos un simbolo y venimos un estado qn:"+lexema)
                                        #print("E actual:"+estado_actual)
                                        if estado_actual in estados_FPR:
                                            #print("Estado actual pertenece a estados finales de reservadas")
                                            if(caracter==" "):
                                                #print("quitamos espacio")
                                                lexema = lexema[:-1]
                                            else:
                                                lexema = lexema[:-1] 
                                                memoria+=caracter
                                            #print(lexema+"in reservadas")
                                            if lexema in palabras_reservadas:
                                                #print("yes")
                                                objeto=MisTokens(lexema.upper(),lexema,"null")
                                                lista_objetos.append(objeto)
                                                guardar_como_any=0
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            else:
                                                #print("El objeto guardado fue:"+lexema)
                                                #input("Que paso")
                                                objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                                lista_objetos.append(objeto)
                                                guardar_como_any=0
                                        elif estado_actual in estados_FString:
                                            objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                                            lista_objetos.append(objeto)
                                            guardar_como_any=0
                                        elif estado_actual =="q3":
                                            if caracter==".":
                                                #print("Aun no guardamos, puede ser decimal")
                                                estado_siguiente="q5"
                                            else:
                                                lexema = lexema[:-1]
                                                memoria+=caracter
                                                #print("se guardo"+lexema)
                                                objeto=MisTokens("ENTERO",lexema,lexema)
                                                lista_objetos.append(objeto)
                                                if caracter==" ":
                                                    lexema=""
                                                    memoria=""
                                                else:   
                                                    if memoria:
                                                        lexema=memoria
                                                        memoria=""
                                                    else:
                                                        lexema=""
                                                guardar_como_any=0
                                            
                                        elif estado_actual =="q4":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual =="q5":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            valor_decimal = float(lexema)
                                            objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual =="q7":
                                            objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                            lista_objetos.append(objeto)
                                            guardar_como_any=0
                                        elif estado_actual=="q500":
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                        elif estado_actual=="q0":
                                            #verificamos de donde viene
                                            print("")
                                            #Hubo un espacio inecesario
                                            #lexema=""
                                        
                                        else:
                                            lexema = lexema[:-1]
                                            memoria+=caracter
                                            objeto=MisTokens("IDENTIFICADOR",lexema,lexema)
                                            lista_objetos.append(objeto)
                                            if caracter==" ":
                                                lexema=""
                                                memoria=""
                                            else:   
                                                if memoria:
                                                    lexema=memoria
                                                    memoria=""
                                                else:
                                                    lexema=""
                                            guardar_como_any=0
                                    else:
                                        if estado_actual=="q7":
                                            #print("Estamos a punto de guardar, venimos de simbolo hacia opciones:"+lexema)
                                            #print("E actual:"+estado_actual)
                                            #if caracter not in estados_nfa.get(estado_actual, {}):
                                            if caracter in PosiblesPR:
                                                lexema = lexema[:-1]
                                                memoria+=caracter
                                                #print("guardamos:"+lexema)
                                                objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                                lista_objetos.append(objeto)
                                                if caracter==" ":
                                                    lexema=""
                                                    memoria=""
                                                else:   
                                                    if memoria:
                                                        lexema=memoria
                                                        memoria=""
                                                    else:
                                                        lexema=""
                                                guardar_como_any=0
                                                
                        estado_anterior=estado_actual        
                        estado_actual=estado_siguiente        
                        #print()
                            
                        contador_caracteres += 1
                        
                #print("caracteres"+ str(contador_caracteres-1))
                tamanio_caracteres_totales=contador_caracteres
                contador_caracteres = 0
                
        
            #print("\nAnalisis lexico:")
            for objeto in lista_objetos:
                print("<"+objeto.tipo + ","+objeto.valor1+","+objeto.valor2+">")
            print("<EOF,eof,null>")      
        except FileNotFoundError:
            return "El archivo no se encontró."
        except PermissionError:
            return "No tienes permisos para acceder al archivo."
    
    elif caso==2:
        contador_caracteres = 0
        total_caracteres=0
        memoria=""
        # Utilizamos la función readlines() para leer todas las líneas del archivo en una lista.
        lineas = ruta_archivo
        lineas+=" "
        indice=0
        
        estado_inicial="q0"
        estado_anterior=""
        estado_actual=estado_inicial
        BanderaT1=0
        BanderaT2=0
        contador_caracteres = 1
        guardar_como_any=0
        lexema=""
        caracter_esperado=""
        inicio=1
        primero=1
        segundo=0
        while indice < len(lineas):
            caracter = lineas[indice]
            if not caracter:
                if BanderaT2==1:
                    print("Antes de cerrar por Error se imprime objetos que se lograron guardar.")
                    for objeto in lista_objetos:
                        print("<"+objeto.tipo + ","+objeto.valor1+","+objeto.valor2+">")
                    sys.exit("Error: No se cerro comentario multilinea.")
                elif estado_actual=="q2" or estado_actual=="q1":
                    print("Antes de cerrar por Error: se imprime objetois que se lograron guardar")
                    for objeto in lista_objetos:
                        print("<"+objeto.tipo + ","+objeto.valor1+","+objeto.valor2+">")
                    sys.exit("Error: No se cerro cadena en el ultimo token String.")
                #print("Guardamos la ultima expresion si es que hay")
                #print(estado_anterior)
                #print(estado_actual)
                #print(estado_siguiente)
                
                if estado_siguiente =="q0":
                    #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                    #print("Estamos a punto de guardar YA QUE ESTADO SIG ES Q0:"+lexema)
                    #print("E actual:"+estado_actual)
                    if estado_actual in estados_FPR:
                        #print("Estado actual pertenece a estados finales de reservadas")
                        if(caracter==" "):
                            #print("quitamos espacio")
                            lexema = lexema[:-1]
                        else:
                            lexema = lexema[:-1] 
                            memoria+=caracter
                        #print(lexema+"in reservadas")
                        if lexema in palabras_reservadas:
                            #print("yes")
                            objeto=MisTokens(lexema.upper(),lexema,"null")
                            lista_objetos.append(objeto)
                            guardar_como_any=0
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        else:
                            #print("El objeto guardado fue:"+lexema)
                            #input("Que paso")
                            objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                            lista_objetos.append(objeto)
                            guardar_como_any=0
                    elif estado_actual in estados_FString:
                        objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                        lista_objetos.append(objeto)
                        guardar_como_any=0
                    elif estado_actual =="q3":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        #print("se guardo"+lexema)
                        objeto=MisTokens("ENTERO",lexema,lexema)
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual =="q4":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual =="q5":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        valor_decimal = float(lexema)
                        objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual =="q7":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        #print("guardamos:"+lexema)
                        objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual=="q500":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual=="q0":
                        
                        #verificamos de donde viene
                        #print("estado anterior:"+estado_anterior)
                        #if estado_anterior==
                        #Hubo un espacio inecesario
                        lexema=""
                
                elif (estado_siguiente=="q2" or estado_siguiente=="q1") and (estado_actual in estados_FPR):
                    
                    lexema = lexema[:-1] 
                    memoria+=caracter
                    #print(lexema+"in reservadas")
                    if lexema in palabras_reservadas:
                        #print("yes")
                        objeto=MisTokens(lexema.upper(),lexema,"null")
                        lista_objetos.append(objeto)
                        guardar_como_any=1
                        if memoria:
                            lexema=memoria
                            memoria=""
                        else:
                            lexema=""
                    else:
                        #print("El objeto guardado fue:"+lexema)
                        #input("Que paso")
                        objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                        lista_objetos.append(objeto)
                        guardar_como_any=1
                        if memoria:
                            lexema=memoria
                            memoria=""
                        else:
                            lexema=""
                
                elif estado_siguiente=="q500":
                    #print("En q500")
                    #Es posiblemente id, asi que verificamos
                    #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                    #print("Estamos a punto de guardar, recibimos algo y venimos un estado qn:"+lexema)
                    #print("E actual:"+estado_actual)
                    if estado_actual in estados_FPR:
                        #print("Estado actual pertenece a estados finales de reservadas")
                        if(caracter==" "):
                            #print("quitamos espacio")
                            lexema = lexema[:-1]
                        else:
                            lexema = lexema[:-1] 
                            memoria+=caracter
                        #print(lexema+"in reservadas")
                        if lexema in palabras_reservadas:
                            #print("yes")
                            objeto=MisTokens(lexema.upper(),lexema,"null")
                            lista_objetos.append(objeto)
                            guardar_como_any=0
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        else:
                            #print("El objeto guardado fue:"+lexema)
                            input("Que paso")
                            objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                            lista_objetos.append(objeto)
                            guardar_como_any=0
                    elif estado_actual in estados_FString:
                        objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                        lista_objetos.append(objeto)
                        guardar_como_any=0
                    elif estado_actual =="q3":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        #print("se guardo"+lexema)
                        objeto=MisTokens("ENTERO",lexema,lexema)
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual =="q4":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual =="q5":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        valor_decimal = float(lexema)
                        objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual =="q7":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        #print("guardamos:"+lexema)
                        objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual=="q500":
                        #lexema = lexema[:-1]
                        memoria+=caracter
                        objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual=="q0":
                        #verificamos de donde viene
                        print("")
                        #if estado_anterior==
                        #Hubo un espacio inecesario
                        #lexema=""
                
                    
                    guardar_como_any=1
                elif estado_siguiente=="q60":
                    #Se escoge opciones de 6 casos
                    if caracter=="=" and estado_anterior=="q7":
                        objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                        lista_objetos.append(objeto)
                        guardar_como_any=0
                        
                    elif caracter=="/":
                        BanderaT1=1
                    elif caracter=="*":
                        BanderaT2=1

                elif estado_siguiente=="q7":
                    #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                    #print("Estamos a punto de guardar, recibimos un simbolo y venimos un estado qn:"+lexema)
                    #print("E actual:"+estado_actual)
                    if estado_actual in estados_FPR:
                        #print("Estado actual pertenece a estados finales de reservadas")
                        if(caracter==" "):
                            #print("quitamos espacio")
                            lexema = lexema[:-1]
                        else:
                            lexema = lexema[:-1] 
                            memoria+=caracter
                        #print(lexema+"in reservadas")
                        if lexema in palabras_reservadas:
                            #print("yes")
                            objeto=MisTokens(lexema.upper(),lexema,"null")
                            lista_objetos.append(objeto)
                            guardar_como_any=0
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        else:
                            #print("El objeto guardado fue:"+lexema)
                            input("Que paso")
                            objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                            lista_objetos.append(objeto)
                            guardar_como_any=0
                    elif estado_actual in estados_FString:
                        objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                        lista_objetos.append(objeto)
                        guardar_como_any=0
                    elif estado_actual =="q3":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        #print("se guardo"+lexema)
                        objeto=MisTokens("ENTERO",lexema,lexema)
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                        
                    elif estado_actual =="q4":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual =="q5":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        valor_decimal = float(lexema)
                        objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual =="q7":
                        objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                        lista_objetos.append(objeto)
                        guardar_como_any=0
                    elif estado_actual=="q500":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual=="q0":
                        #verificamos de donde viene
                        print("")
                        #if estado_anterior==
                        #Hubo un espacio inecesario
                        #lexema=""

                else:
                    if estado_actual=="q7":
                        #print("Estamos a punto de guardar, venimos de simbolo hacia opciones:"+lexema)
                        #print("E actual:"+estado_actual)
                        #if caracter not in estados_nfa.get(estado_actual, {}):
                        if caracter in PosiblesPR:
                            lexema = lexema[:-1]
                            memoria+=caracter
                            #print("guardamos:"+lexema)
                            objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                            lista_objetos.append(objeto)
                            if caracter==" ":
                                lexema=""
                                memoria=""
                            else:   
                                if memoria:
                                    lexema=memoria
                                    memoria=""
                                else:
                                    lexema=""
                            guardar_como_any=0
                    
                    elif estado_actual in estados_FPR:
                        #print("Estado actual pertenece a estados finales de reservadas")
                        if(caracter==" "):
                            #print("quitamos espacio")
                            lexema = lexema[:-1]
                        else:
                            #lexema = lexema[:-1] 
                            memoria+=caracter
                        #print(lexema+"in reservadas")
                        if lexema in palabras_reservadas:
                            #print("yes")
                            objeto=MisTokens(lexema.upper(),lexema,"null")
                            lista_objetos.append(objeto)
                            guardar_como_any=0
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        else:
                            #print("El objeto guardado fue:"+lexema)
                            #input("Que paso")
                            objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                            lista_objetos.append(objeto)
                            guardar_como_any=0
                    
                break  # Fin del archivo
            elif BanderaT1==1:# Comentario 1
                if caracter=="\n":
                    #print("Caracter de salto de linea. Se vuele a leer")
                    #print("t1estado_anterior"+estado_anterior)
                    #print("t1estado actual:"+estado_actual)
                    #print("t1estado siguiente:"+estado_siguiente)
                    lexema=""
                    BanderaT1=0
                    guardar_como_any=0
                    estado_actual=estado_inicial
            elif BanderaT2==1:# Comentario 2, no hacemos nada hasta detectar cierre
                if primero==1:
                    if caracter=="*":
                        primero=0
                        segundo=1
                        caracter_esperado="/"
                elif segundo==1:
                    if caracter==caracter_esperado:
                        #Reset desde bandera
                        BanderaT2=0
                        primero=1
                        segundo=0
                        caracter_esperado=""
                        guardar_como_any=0
                        lexema=""
                        estado_actual=estado_inicial
                        #print("t2estado_anterior"+estado_anterior)
                        #print("t2estado actual:"+estado_actual)
                        #print("t2estado siguiente:"+estado_siguiente)
                    else:
                        #Reset de lectura
                        primero=1
                        segundo=0
                        caracter_esperado=""
                    
            else:
                #print("Caracter actual--:"+caracter)
                if caracter=="\n":
                    guardar_como_any=0
                    #print("estado_anterior"+estado_anterior)
                    #print("estado actual:"+estado_actual)
                    estado_siguiente=estado_inicial
                    #print("estado siguiente:"+estado_siguiente)
                    #print("Caracter de salto de linea implicito.")
                    #print("LEXEMA ACTUAL:"+lexema)
                    if estado_actual in estados_FPR:
                        #print("Estado actual pertenece a estados finales de reservadas")
                        if(caracter==" "):
                            #print("quitamos espacio")
                            lexema = lexema[:-1]
                        else:
                            lexema = lexema[:-1] 
                            memoria+=caracter
                        #print(lexema+"in reservadas")
                        if lexema in palabras_reservadas:
                            #print("yes")
                            objeto=MisTokens(lexema.upper(),lexema,"null")
                            lista_objetos.append(objeto)
                            guardar_como_any=0
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        else:
                            #print("El objeto guardado fue:"+lexema)
                            #input("Que paso")
                            objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                            lista_objetos.append(objeto)
                            guardar_como_any=0
                    elif estado_actual in estados_FString:
                        for objeto in lista_objetos:
                            print("<"+objeto.tipo + ","+objeto.valor1+","+objeto.valor2+">")
                        sys.exit("Error: No se cerro STRING: "+lexema+"")
                        #objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                        #lista_objetos.append(objeto)
                        #guardar_como_any=0
                    elif estado_actual =="q3":
                        
                        #lexema = lexema[:-1]
                        memoria+=caracter
                        #print("se guardo"+lexema)
                        objeto=MisTokens("ENTERO",lexema,lexema)
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual =="q4":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual =="q5":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        valor_decimal = float(lexema)
                        objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual =="q7":
                        #lexema = lexema[:-1]
                        memoria+=caracter
                        #print("guardamos:"+lexema)
                        objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual=="q500":
                        lexema = lexema[:-1]
                        memoria+=caracter
                        objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                        lista_objetos.append(objeto)
                        if caracter==" ":
                            lexema=""
                            memoria=""
                        else:   
                            if memoria:
                                lexema=memoria
                                memoria=""
                            else:
                                lexema=""
                        guardar_como_any=0
                    elif estado_actual=="q0":
                        #verificamos de donde viene
                        #print("estado anterior:"+estado_anterior)
                        #if estado_anterior==
                        #Hubo un espacio inecesario
                        lexema=""
                
                    
                    
                    
                    lexema=""
                    estado_actual=estado_inicial
                    if estado_actual=="q2" or estado_actual=="q1":
                        sys.exit("Error: No se cerro cadena.")                           
                else:
                    lexema+=caracter
                    #print(caracter)
                    #print(estado_actual)
                    #print("LEXEMA ACTUAL:"+lexema)
                    #En dicha variable guardaremos si se trata de, Number, symbol, ", ', posible PR, o any (candidata a ID)
                    caso=""
                    #Debemos evaluar de que tipo de letra se trata, llamamos a evaluadores/Interpretes
                    if caracter in estados_nfa.get(estado_actual, {}):
                        guardar_como_any=0
                    else:
                        guardar_como_any=1
                    caso=interprete(caracter,simbolos,PosiblesPR,guardar_como_any)
                    #print("caso:"+caso)
                    if inicio==1:
                        inicio=1
                        if caso == "'":
                            #estado_anterior=estado_actual
                            estado_siguiente = next(iter(estados_nfa[estado_actual][caso]))
                            guardar_como_any=1
                        elif caso== '"':
                            #estado_anterior=estado_actual
                            estado_siguiente = next(iter(estados_nfa[estado_actual][caso]))
                            guardar_como_any=1
                        elif caso=="Number":
                            #estado_anterior=estado_actual
                            estado_siguiente = next(iter(estados_nfa[estado_actual][caso]))
                            guardar_como_any=1
                        elif caso=="symbol":
                            #estado_anterior=estado_actual
                            estado_siguiente = next(iter(estados_nfa[estado_actual][caso]))
                        else:
                            #estado_anterior=estado_actual
                            estado_siguiente = next(iter(estados_nfa[estado_actual][caso]))
                        
                        #print("Estado actual:"+estado_actual)
                        #print("Estado siguiente:"+estado_siguiente)


                        if estado_siguiente =="q0":
                            #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                            #print("Estamos a punto de guardar YA QUE ESTADO SIG ES Q0:"+lexema)
                            #print("E actual:"+estado_actual)
                            if estado_actual in estados_FPR:
                                #print("Estado actual pertenece a estados finales de reservadas")
                                if(caracter==" "):
                                    #print("quitamos espacio")
                                    lexema = lexema[:-1]
                                else:
                                    lexema = lexema[:-1] 
                                    memoria+=caracter
                                #print(lexema+"in reservadas")
                                if lexema in palabras_reservadas:
                                    #print("yes")
                                    objeto=MisTokens(lexema.upper(),lexema,"null")
                                    lista_objetos.append(objeto)
                                    guardar_como_any=0
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                else:
                                    #print("El objeto guardado fue:"+lexema)
                                    #input("Que paso")
                                    objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                    lista_objetos.append(objeto)
                                    guardar_como_any=0
                            elif estado_actual in estados_FString:
                                #lexema = lexema[:-1]
                                memoria+=caracter
                                #print("guardamos:"+lexema)
                                objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                        lexema=""
                                    else:
                                        lexema=""
                                
                                guardar_como_any=0
                            elif estado_actual =="q3":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                #print("se guardo"+lexema)
                                objeto=MisTokens("ENTERO",lexema,lexema)
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual =="q4":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual =="q5":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                valor_decimal = float(lexema)
                                objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual =="q7":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                #print("guardamos:"+lexema)
                                objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual=="q500":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual=="q0":
                                #verificamos de donde viene
                                #print("estado anterior:"+estado_anterior)
                                #if estado_anterior==
                                #Hubo un espacio inecesario
                                lexema=""
                            
                            else:
                                lexema = lexema[:-1]
                                memoria+=caracter
                                objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                                
                                
                                
                        elif (estado_siguiente=="q2" or estado_siguiente=="q1") and (estado_actual in estados_FPR):
                            lexema = lexema[:-1] 
                            memoria+=caracter
                            #print(lexema+"in reservadas")
                            if lexema in palabras_reservadas:
                                #print("yes")
                                objeto=MisTokens(lexema.upper(),lexema,"null")
                                lista_objetos.append(objeto)
                                guardar_como_any=1
                                if memoria:
                                    lexema=memoria
                                    memoria=""
                                else:
                                    lexema=""
                            else:
                                #print("El objeto guardado fue:"+lexema)
                                #input("Que paso")
                                objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                lista_objetos.append(objeto)
                                guardar_como_any=1
                                if memoria:
                                    lexema=memoria
                                    memoria=""
                                else:
                                    lexema=""
                        elif estado_siguiente=="q3":
                            if estado_actual=="q7":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                #print("guardamos:"+lexema)
                                objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                        elif estado_siguiente=="q500":
                            #print("En q500")
                            #Es posiblemente id, asi que verificamos
                            #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                            #print("Estamos a punto de guardar, recibimos algo y venimos un estado qn:"+lexema)
                            #print("E actual:"+estado_actual)
                            if (estado_actual in estados_FPR) and ((caso!="any") and(caso!="Number")):
                                #print("Estado actual pertenece a estados finales de reservadas")
                                if(caracter==" "):
                                    #print("quitamos espacio")
                                    lexema = lexema[:-1]
                                else:
                                    lexema = lexema[:-1] 
                                    memoria+=caracter
                                #print(lexema+"in reservadas")
                                if lexema in palabras_reservadas:
                                    #print("yes")
                                    objeto=MisTokens(lexema.upper(),lexema,"null")
                                    lista_objetos.append(objeto)
                                    guardar_como_any=0
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                else:
                                    #print("El objeto guardado fue:"+lexema)
                                    input("Que paso")
                                    objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                    lista_objetos.append(objeto)
                                    guardar_como_any=0
                            elif estado_actual in estados_FString:
                                objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                                lista_objetos.append(objeto)
                                guardar_como_any=0
                            elif estado_actual =="q3":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                #print("se guardo"+lexema)
                                objeto=MisTokens("ENTERO",lexema,lexema)
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual =="q4":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual =="q5":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                valor_decimal = float(lexema)
                                objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual =="q7":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                #print("guardamos:"+lexema)
                                objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual=="q0":
                                #verificamos de donde viene
                                print("")
                                #if estado_anterior==
                                #Hubo un espacio inecesario
                                #lexema=""
                            
                            elif estado_actual=="q500":
                                #print("Sigue con any")
                                guardar_como_any=1
                            
                            
                        
                            
                            guardar_como_any=1
                        elif estado_siguiente=="q60":
                            #Se escoge opciones de 6 casos
                            #print("estado anterior"+estado_anterior)
                            if caracter=="=" and ((estado_anterior=="q7") or(estado_actual=="q7")):
                                
                                objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                lista_objetos.append(objeto)
                                estado_siguiente=estado_inicial
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                        
                                    else:
                                        lexema=""
                                
                                guardar_como_any=0
                            elif caracter=="/":
                                BanderaT1=1
                                estado_siguiente=estado_inicial
                            elif caracter=="*":
                                BanderaT2=1
                                estado_siguiente=estado_inicial
                            
                            else:
                                #es otro simbolo
                                lexema = lexema[:-1]
                                memoria+=caracter
                                #print("lexema"+lexema)
                                objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                        
                                    else:
                                        lexema=""
                                
                                guardar_como_any=0
                                estado_siguiente="q7"
                        elif estado_siguiente=="q7":
                            #guardamos porque llegamos a q0 en la siguiente, pero hay que ver que guardaremos
                            #print("Estamos a punto de guardar, recibimos un simbolo y venimos un estado qn:"+lexema)
                            #print("E actual:"+estado_actual)
                            if estado_actual in estados_FPR:
                                #print("Estado actual pertenece a estados finales de reservadas")
                                if(caracter==" "):
                                    #print("quitamos espacio")
                                    lexema = lexema[:-1]
                                else:
                                    lexema = lexema[:-1] 
                                    memoria+=caracter
                                #print(lexema+"in reservadas")
                                if lexema in palabras_reservadas:
                                    #print("yes")
                                    objeto=MisTokens(lexema.upper(),lexema,"null")
                                    lista_objetos.append(objeto)
                                    guardar_como_any=0
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                else:
                                    #print("El objeto guardado fue:"+lexema)
                                    #input("Que paso")
                                    objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                    lista_objetos.append(objeto)
                                    guardar_como_any=0
                            elif estado_actual in estados_FString:
                                objeto=MisTokens("STRING",lexema,lexema.strip('"'))
                                lista_objetos.append(objeto)
                                guardar_como_any=0
                            elif estado_actual =="q3":
                                if caracter==".":
                                    #print("Aun no guardamos, puede ser decimal")
                                    estado_siguiente="q5"
                                else:
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    #print("se guardo"+lexema)
                                    objeto=MisTokens("ENTERO",lexema,lexema)
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                
                            elif estado_actual =="q4":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                objeto=MisTokens("EXPONENCIAL",lexema,lexema)
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual =="q5":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                valor_decimal = float(lexema)
                                objeto=MisTokens("DECIMAL",lexema,str(valor_decimal))
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual =="q7":
                                objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                lista_objetos.append(objeto)
                                guardar_como_any=0
                            elif estado_actual=="q500":
                                lexema = lexema[:-1]
                                memoria+=caracter
                                objeto=MisTokens("IDENTIFICADOR",lexema,"null")
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                            elif estado_actual=="q0":
                                #verificamos de donde viene
                                print("")
                                #Hubo un espacio inecesario
                                #lexema=""
                            
                            else:
                                lexema = lexema[:-1]
                                memoria+=caracter
                                objeto=MisTokens("IDENTIFICADOR",lexema,lexema)
                                lista_objetos.append(objeto)
                                if caracter==" ":
                                    lexema=""
                                    memoria=""
                                else:   
                                    if memoria:
                                        lexema=memoria
                                        memoria=""
                                    else:
                                        lexema=""
                                guardar_como_any=0
                        else:
                            if estado_actual=="q7":
                                #print("Estamos a punto de guardar, venimos de simbolo hacia opciones:"+lexema)
                                #print("E actual:"+estado_actual)
                                #if caracter not in estados_nfa.get(estado_actual, {}):
                                if caracter in PosiblesPR:
                                    lexema = lexema[:-1]
                                    memoria+=caracter
                                    #print("guardamos:"+lexema)
                                    objeto=MisTokens((nombres_simbolos[lexema]),lexema,"null")
                                    lista_objetos.append(objeto)
                                    if caracter==" ":
                                        lexema=""
                                        memoria=""
                                    else:   
                                        if memoria:
                                            lexema=memoria
                                            memoria=""
                                        else:
                                            lexema=""
                                    guardar_como_any=0
                                    
            estado_anterior=estado_actual        
            estado_actual=estado_siguiente        
            #print()
                
            contador_caracteres += 1
            indice += 1
        
        #print("\nAnalisis lexico:")
        for objeto in lista_objetos:
            print("<"+objeto.tipo + ","+objeto.valor1+","+objeto.valor2+">")
        print("<EOF,eof,null>")  
def main():
    bandera=0
    #print(str(len(sys.argv)))  
    if (len(sys.argv) == 2) and (sys.argv[-1].endswith(".txt")):
        #.txt
        #print("es txt")  
        argumento = sys.argv[1]
        bandera=1
    else:
        argumento = ' '.join(sys.argv[1:])
        bandera=2
        #print("bro")  
    #print(argumento)
    #while True:
        
        
    #entrada = input("$>>")
    # Limpia la lista de objetos por si esta llena
    lista_objetos.clear()
    # Verificar si la entrada es un archivo con una ruta completa de estilo Windows
    if bandera==1:
        caso=1
        ruta_archivo=os.path.dirname(os.path.realpath(__file__))
        ruta_archivo=ruta_archivo + '\\'+argumento
        ruta_archivo=ruta_archivo.replace("\\","/")
        resultado=analizar_codigo(ruta_archivo,caso)
        sys.exit("")
        #print()
        #input("\nPresiona Enter para continuar...")
        #os.system('cls' if os.name == 'nt' else 'clear')
    elif bandera==2:
        caso=2
        codigo = argumento
        resultado=analizar_codigo(codigo,caso)
        #print()
        #input("\nPresiona Enter para continuar...")
        #os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nSaliendo del programa.")

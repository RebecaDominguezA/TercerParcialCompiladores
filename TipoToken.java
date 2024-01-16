public enum TipoToken {
    // Tokens de un sólo caracter
    PARENTESIS_ABRE, PARENTESIS_CIERRA, LLAVE_ABRE, LLAVE_CIERRA,
    COMA, PUNTO, RESTA, SUMA, PUNTO_Y_COMA, SLASH, ESTRELLA,

    // Tokens de uno o dos caracteres
    BANG, DIFERENTE_QUE,
    IGUAL, IGUAL_IGUAL,
    MAYOR_QUE, MAYOR_IGUAL_QUE,
    MENOR_QUE, MENOR_IGUAL_QUE,

    // Literales
    IDENTIFICADOR, STRING, NUMBER, ENTERO,DECIMAL,

    // Palabras clave
    AND, ELSE, FALSE, FUN, FOR, IF, NULL, OR,
    PRINT, RETURN, TRUE, VAR, WHILE,

    EOF
}


import java.util.ArrayList;
import java.util.List;
import java.util.Arrays;

public class AST implements Parser {
    private int i = 0;
    private boolean hayErrores = false;
    private Token preanalisis;
    private final List<Token> tokens;

    public AST(List<Token> tokens){
        
        this.tokens = tokens;
        preanalisis = this.tokens.get(i);
    }

    //Clase para manejar errores
    public class ParserException extends Exception {
        public ParserException(String message) {
            super(message);
        }
    }
    
    @Override
    public boolean parse() {
        PROGRAM();
    
        if (preanalisis.tipo == TipoToken.EOF && !hayErrores) {
            System.out.println("Consulta correcta.");
            return true;
        } else {
            System.out.println("Se encontraron errores");
            // Puedes agregar más información sobre los errores aquí si es necesario
        }
        return false;
    }
    
    //PROGRAM -> DECLARATION
    public List<Statement> PROGRAM(){
        List<Statement> StateMts = new ArrayList<>();
        if(preanalisis.tipo == TipoToken.BANG
        || preanalisis.tipo == TipoToken.RESTA
        || preanalisis.tipo == TipoToken.TRUE
        || preanalisis.tipo == TipoToken.FALSE
        || preanalisis.tipo == TipoToken.NULL
        || preanalisis.tipo == TipoToken.ENTERO
        || preanalisis.tipo == TipoToken.DECIMAL
        || preanalisis.tipo == TipoToken.STRING
        || preanalisis.tipo == TipoToken.IDENTIFICADOR
        || preanalisis.tipo == TipoToken.PARENTESIS_ABRE
        || preanalisis.tipo == TipoToken.FOR
        || preanalisis.tipo == TipoToken.IF
        || preanalisis.tipo == TipoToken.PRINT
        || preanalisis.tipo == TipoToken.RETURN
        || preanalisis.tipo == TipoToken.WHILE
        || preanalisis.tipo == TipoToken.LLAVE_ABRE
        || preanalisis.tipo == TipoToken.FUN
        || preanalisis.tipo == TipoToken.VAR){
            DECLARATION(StateMts);
        }
        return StateMts;
    }

    //DEN

    //DEN

    //BECA

    //BECA
}

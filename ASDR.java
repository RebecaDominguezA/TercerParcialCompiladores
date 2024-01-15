import java.util.List;

public class ASDR implements Parser{
    //private TokenIterator tokenIterator;
    private int i = 0;
    private boolean hayErrores = false;
    private Token preanalisis;
    private final List<Token> tokens;

    public ASDR(List<Token> tokens){
        //this.tokenIterator = new TokenIterator(tokens);
        this.tokens = tokens;
        preanalisis = this.tokens.get(i);
    }

    @Override
    public boolean parse() {
        //System.out.println("INICIAMOS");
        //for(Token token : tokens){
            //System.out.println(token);
        //}
        //System.out.println(preanalisis);

        PROGRAM();
        if(preanalisis.tipo == TipoToken.EOF && !hayErrores){
            System.out.println("Consulta correcta");
            return  true;
        }else {
            System.out.println("Se encontraron errores");
        }
        
        return false;
    }

    //Programa
    private void PROGRAM(){
        DECLARATION();
    }
    
    // DECLARATION -> FUN_DECL DECLARATION | VAR_DECL DECLARATION 
    //                                      | STATEMENT DECLARATION | E
    private void DECLARATION(){
        if(hayErrores)
            return;

        if(preanalisis.tipo == TipoToken.FUN){//FUN_DECL DECLARATION
            FUN_DECL();
            DECLARATION();
        }
        else if (preanalisis.tipo == TipoToken.VAR) {//VAR_DECL DECLARATION 
            VAR_DECL();
            DECLARATION();
        }
        //STATEMENT DECLARATION
        else if (preanalisis.tipo == TipoToken.BANG
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
                ) {
            STATEMENT();
            DECLARATION();
        }
        //ELSE VACIO
    }


    //Aquui den

    //fin
  
}

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


    
    // FUN_DECL -> fun FUNCTION
    private void FUN_DECL(){
        if(hayErrores)
            return;
        
        if(preanalisis.tipo == TipoToken.FUN){
            match(TipoToken.FUN);
            FUNCTION();
        }
        else{
            hayErrores = true;
            System.out.println("Se esperaba un 'FUN'");
        }

    }

    // VAR_DECL -> var id VAR_INIT
    private void VAR_DECL(){
        if(hayErrores)
            return;
        if(preanalisis.tipo == TipoToken.VAR){
            match(TipoToken.VAR);
            match(TipoToken.IDENTIFICADOR);
            //System.out.println("checkpoint");
            //for(Token token : tokens){
                //System.out.println(token);
            //}
            VAR_INIT();
            match(TipoToken.PUNTO_Y_COMA);
        }
        else{
            hayErrores = true;
            System.out.println("Se esperaba un 'VAR'");
        }
    }
    
    // STATEMENT -> EXPR_STMT | FOR_STMT | IF_STMT
    //              | PRINT_STMT | RETURN_STMT | WHILE_STMT | BLOCK
    private void STATEMENT(){
        if(hayErrores)
            return;
        
        if (preanalisis.tipo == TipoToken.BANG
            || preanalisis.tipo == TipoToken.RESTA
            || preanalisis.tipo == TipoToken.TRUE
            || preanalisis.tipo == TipoToken.FALSE
            || preanalisis.tipo == TipoToken.NULL
            || preanalisis.tipo == TipoToken.ENTERO
            || preanalisis.tipo == TipoToken.DECIMAL
            || preanalisis.tipo == TipoToken.STRING
            || preanalisis.tipo == TipoToken.IDENTIFICADOR
            || preanalisis.tipo == TipoToken.PARENTESIS_ABRE){
            EXPR_STMT();
        }
        else if(preanalisis.tipo == TipoToken.FOR){
            FOR_STMT();
        }
        else if(preanalisis.tipo == TipoToken.IF){
            IF_STMT();
        }
        else if(preanalisis.tipo == TipoToken.PRINT){
            PRINT_STMT();
        }
        else if(preanalisis.tipo == TipoToken.RETURN){
            RETURN_STMT();
        }
        else if(preanalisis.tipo == TipoToken.WHILE){
            WHILE_STMT();
        }
        else if(preanalisis.tipo == TipoToken.LLAVE_ABRE){
            BLOCK();
        }else{
            hayErrores = true;
            System.out.println("Se esperaba 'BANG' or 'RESTA' or 'TRUE' or 'FALSE'"+
            "or 'NULL' or 'ENTERO' or 'DECIMAL' or 'STRING'  or 'IDENTIFICADOR' or 'PARENTESIS_ABRE' "+
            "or 'FOR' or 'IF' or 'PRINT' or 'RETURN' or 'WHILE' or '{'");
        }
    }

    // FUNCTION -> id ( PARAMETERS_OPC ) BLOCK
    private void FUNCTION(){
        if(hayErrores)
            return;
        if(preanalisis.tipo == TipoToken.IDENTIFICADOR){
            match(TipoToken.IDENTIFICADOR);
            match(TipoToken.PARENTESIS_ABRE);
            PARAMETERS_OPC();
            match(TipoToken.PARENTESIS_CIERRA);
            BLOCK();
        }else{
            hayErrores = true;
            System.out.println("Se esperaba 'IDENTIFICADOR'");
        }
    }

    // VAR_INIT -> = EXPRESSION | E
    private void VAR_INIT(){
        if(hayErrores)
            return;
        if(preanalisis.tipo == TipoToken.IGUAL){
            match(TipoToken.IGUAL);
            EXPRESSION();
        }
        //else vacio
         }
    
    //  EXPRESSION -> ASSIGNMENT
    private void EXPRESSION(){
        if(hayErrores)
            return;
        
        ASSIGNMENT();  
    }

    //  EXPR_STMT -> EXPRESSION
    private void EXPR_STMT(){
        if(hayErrores)
            return;
        
        EXPRESSION();
        match(TipoToken.PUNTO_Y_COMA);
        
    }
    
  
}

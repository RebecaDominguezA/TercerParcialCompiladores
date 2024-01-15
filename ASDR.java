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
    //  FOR_STMT -> for ( FOR_STMT_1 FOR_STMT_2 FOR_STMT_3 ) STATEMENT
    private void FOR_STMT(){
        if(hayErrores)
            return;
        
        match(TipoToken.FOR);
        match(TipoToken.PARENTESIS_ABRE);
        FOR_STMT_1();
        FOR_STMT_2();
        FOR_STMT_3();
        match(TipoToken.PARENTESIS_CIERRA);
        STATEMENT();
    }

    //   if (EXPRESSION) STATEMENT ELSE_STATEMENT
    private void IF_STMT(){
        if(hayErrores)
            return;
        
        match(TipoToken.IF);
        match(TipoToken.PARENTESIS_ABRE);
        EXPRESSION();
        match(TipoToken.PARENTESIS_CIERRA);
        STATEMENT();
        ELSE_STATEMENT();
    }

    //   PRINT_STMT -> print EXPRESSION;
    private void PRINT_STMT(){
        if(hayErrores)
            return;
        
        match(TipoToken.PRINT);
        EXPRESSION();
        match(TipoToken.PUNTO_Y_COMA);
    }

    //   RETURN_STMT -> return RETURN_EXP_OPC ;
    private void RETURN_STMT(){
        if(hayErrores)
            return;
        
        match(TipoToken.RETURN);
        RETURN_EXP_OPC();
        match(TipoToken.PUNTO_Y_COMA);
    }
    
    //   WHILE_STMT -> while ( EXPRESSION ) STATEMENT
    private void WHILE_STMT(){
        if(hayErrores)
            return;
        
        match(TipoToken.WHILE);
        match(TipoToken.PARENTESIS_ABRE);
        EXPRESSION();
        match(TipoToken.PARENTESIS_CIERRA);
        STATEMENT();
    }

    //   BLOCK -> { DECLARATION }
    private void BLOCK(){
        if(hayErrores)
            return;
        
        match(TipoToken.LLAVE_ABRE);
        DECLARATION();
        match(TipoToken.LLAVE_CIERRA);
    }

    //   FOR_STMT_1 -> VAR_DECL | EXPR_STMT | ;
    private void FOR_STMT_1(){
        if(hayErrores)
            return;
        
        if(preanalisis.tipo == TipoToken.VAR){
            VAR_DECL();
        }
        else if (preanalisis.tipo == TipoToken.BANG
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
        else if (preanalisis.tipo == TipoToken.PUNTO_Y_COMA){
            match(TipoToken.PUNTO_Y_COMA);
        }
        else{
            hayErrores = true;
            System.out.println("Se esperaba un 'VAR' or 'BANG' or 'RESTA' or 'TRUE' or 'FALSE'"+ 
            "or 'NULL' or 'ENTERO' or 'DECIMAL' or 'STRING'  or 'IDENTIFICADOR' or 'PARENTESIS_ABRE' or ';'");
        }
    }
    //   FOR_STMT_2 -> EXPRESSION ; | ;
    private void FOR_STMT_2(){
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
            EXPRESSION();
            match(TipoToken.PUNTO_Y_COMA);
        }
        else if (preanalisis.tipo == TipoToken.PUNTO_Y_COMA){
            match(TipoToken.PUNTO_Y_COMA);
        }
        else{
            hayErrores = true;
            System.out.println("Se esperaba un 'BANG' or 'RESTA' or 'TRUE' or 'FALSE'"+ 
            "or 'NULL' or 'ENTERO' or 'DECIMAL' or 'STRING'  or 'IDENTIFICADOR' or 'PARENTESIS_ABRE' or ';'");
        }
    }

    //   FOR_STMT_3 -> EXPRESSION | E
    private void FOR_STMT_3(){
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
            EXPRESSION();
        }
        //else vacio
    }

    //   ELSE_STATEMENT -> else STATEMENT | E
    private void ELSE_STATEMENT(){
        if(hayErrores)
            return;
        
        if(preanalisis.tipo == TipoToken.ELSE){
            match(TipoToken.ELSE);
            STATEMENT();
        }
        //else caso vacio
    }

    //   RETURN_EXP_OPC -> EXPRESSION | E
    private void RETURN_EXP_OPC(){
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
            EXPRESSION();
        }
        //else vacio
    }

    //   ASSIGNMENT -> LOGIC_OR ASSIGNMENT_OPC
    private void ASSIGNMENT(){
        if(hayErrores)
            return;

        LOGIC_OR();
        ASSIGNMENT_OPC();
    }

//   ASSIGNMENT_OPC -> = EXPRESSION | E
    private void ASSIGNMENT_OPC(){
        if(hayErrores)
            return;

        if(preanalisis.tipo == TipoToken.IGUAL){
            match(TipoToken.IGUAL);
            EXPRESSION();
        }
        //ELSE vacio    
    }

    //   LOGIC_OR -> LOGIC_AND LOGIC_OR_2
    private void LOGIC_OR(){
        if(hayErrores)
            return;
            
        LOGIC_AND();
        LOGIC_OR_2();
    }

    //   LOGIC_OR_2 -> or LOGIC_AND LOGIC_OR_2 | E
    private void LOGIC_OR_2(){
        if(hayErrores)
            return;
            
        if(preanalisis.tipo == TipoToken.OR){
            match(TipoToken.OR);
            LOGIC_AND();
            LOGIC_OR_2();
        }
        //ELSE vacio  
    }

    //   LOGIC_AND -> EQUALITY LOGIC_AND_2
    private void LOGIC_AND(){
        if(hayErrores)
            return;
            
        EQUALITY();
        LOGIC_AND_2();
    }

    //   LOGIC_AND_2 -> and EQUALITY LOGIC_AND_2 | E
    private void LOGIC_AND_2(){
        if(hayErrores)
            return;
            
        if(preanalisis.tipo == TipoToken.AND){
            match(TipoToken.AND);
            EQUALITY();
            LOGIC_AND_2();
        }
        //ELSE vacio 
    }

    //   EQUALITY -> COMPARISON EQUALITY_2
    private void EQUALITY(){
        if(hayErrores)
            return;
            
        COMPARISON();
        EQUALITY_2();
    }

    //   EQUALITY_2 -> != COMPARISON EQUALITY_2 | == COMPARISON EQUALITY_2 | E
    private void EQUALITY_2(){
        if(hayErrores)
            return;
            
        if(preanalisis.tipo == TipoToken.DIFERENTE_QUE){
            match(TipoToken.DIFERENTE_QUE);
            COMPARISON();
            EQUALITY_2();
        }
        else if(preanalisis.tipo == TipoToken.IGUAL_IGUAL){
            match(TipoToken.IGUAL_IGUAL);
            COMPARISON();
            EQUALITY_2();
        }
        //ELSE vacio 
    }


    //   COMPARISON -> TERM COMPARISON_2
    private void COMPARISON(){
        if(hayErrores)
            return;
        
        TERM();
        COMPARISON_2();
    }

    //   COMPARISON_2 -> > TERM COMPARISON_2 | >= TERM COMPARISON_2 |
    //                   < TERM COMPARISON_2 | <= TERM COMPARISON_2 | E
    private void COMPARISON_2(){
        if(hayErrores)
            return;
            
        if(preanalisis.tipo == TipoToken.MAYOR_QUE){
            match(TipoToken.MAYOR_QUE);
            TERM();
            COMPARISON_2();

        }
        else if(preanalisis.tipo == TipoToken.MAYOR_IGUAL_QUE){
            match(TipoToken.MAYOR_IGUAL_QUE);
            TERM();
            COMPARISON_2();
            
        }
        else if(preanalisis.tipo == TipoToken.MENOR_QUE){
            match(TipoToken.MENOR_QUE);
            TERM();
            COMPARISON_2();
        }
        else if(preanalisis.tipo == TipoToken.MENOR_IGUAL_QUE){
            match(TipoToken.MENOR_IGUAL_QUE);
            TERM();
            COMPARISON_2();
            
        }
        //Else vacio
    }

    //   TERM -> FACTOR TERM_2
    private void TERM(){
        if(hayErrores)
            return;
        
        FACTOR();
        TERM_2();
    }

    // TERM_2 -> - FACTOR TERM_2 | + FACTOR TERM_2 | E
    private void TERM_2(){
        if(hayErrores)
            return;
            
        if(preanalisis.tipo == TipoToken.RESTA){
            match(TipoToken.RESTA);
            FACTOR();
            TERM_2();

        }
        else if(preanalisis.tipo == TipoToken.SUMA){
            match(TipoToken.SUMA);
            FACTOR();
            TERM_2();
        }
        //ELSE VACIO
    }

    // FACTOR -> UNARY FACTOR_2
    private void FACTOR(){
        if(hayErrores)
            return;
        
        UNARY();
        FACTOR_2();
    }

    // FACTOR_2 -> / UNARY FACTOR_2 | * UNARY FACTOR_2 | E
    private void FACTOR_2(){
        if(hayErrores)
            return;
            
        if(preanalisis.tipo == TipoToken.SLASH){
            match(TipoToken.SLASH);
            UNARY();
            FACTOR_2();

        }
        else if(preanalisis.tipo == TipoToken.ESTRELLA){
            match(TipoToken.ESTRELLA);
            UNARY();
            FACTOR_2();
        }
        //ELSE VACIO
    }

    // UNARY -> ! UNARY | - UNARY | CALL
    private void UNARY(){
        if(hayErrores)
            return;
            
        if(preanalisis.tipo == TipoToken.BANG){
            match(TipoToken.BANG);
            UNARY();
        }
        else if(preanalisis.tipo == TipoToken.RESTA){
            match(TipoToken.RESTA);
            UNARY();
        }
        else if (preanalisis.tipo == TipoToken.TRUE
            || preanalisis.tipo == TipoToken.FALSE
            || preanalisis.tipo == TipoToken.NULL
            || preanalisis.tipo == TipoToken.ENTERO
            || preanalisis.tipo == TipoToken.DECIMAL
            || preanalisis.tipo == TipoToken.STRING
            || preanalisis.tipo == TipoToken.IDENTIFICADOR
            || preanalisis.tipo == TipoToken.PARENTESIS_ABRE){
            CALL();
        }else{
            hayErrores = true;
            System.out.println("Se esperaba 'BANG' or 'RESTA' or 'TRUE' or 'FALSE'"+
            "or 'NULL' or 'ENTERO' or 'DECIMAL' or 'STRING'  or 'IDENTIFICADOR' or 'PARENTESIS_ABRE'.");
        }
    }

    // CALL -> PRIMARY CALL_2
    private void CALL(){
        if(hayErrores)
            return;
        
        PRIMARY();
        CALL_2();
    }

    //   CALL_2 -> ( ARGUMENTS_OPC ) CALL_2 | E
    private void CALL_2(){
        if(hayErrores)
            return;
            
        if(preanalisis.tipo == TipoToken.PARENTESIS_ABRE){
            match(TipoToken.PARENTESIS_ABRE);
            ARGUMENTS_OPC();
            match(TipoToken.PARENTESIS_CIERRA);
            CALL_2();
        }
        //ELSE vacio 
    }

    //   PRIMARY -> true | false | null | number | string | id | ( EXPRESSION )
    private void PRIMARY(){
        if(hayErrores)
            return;
            
        if(preanalisis.tipo == TipoToken.TRUE){
            match(TipoToken.TRUE);
        }
        else if(preanalisis.tipo == TipoToken.FALSE){
            match(TipoToken.FALSE);
        }
        else if(preanalisis.tipo == TipoToken.NULL){
            match(TipoToken.NULL);
        }
        else if(preanalisis.tipo == TipoToken.DECIMAL){
            match(TipoToken.DECIMAL);
        }
        else if(preanalisis.tipo == TipoToken.ENTERO){
            match(TipoToken.ENTERO);
        }
        else if(preanalisis.tipo == TipoToken.STRING){
            match(TipoToken.STRING);
        }
        else if(preanalisis.tipo == TipoToken.IDENTIFICADOR){
            match(TipoToken.IDENTIFICADOR);
        }
        else if(preanalisis.tipo == TipoToken.PARENTESIS_ABRE){
            match(TipoToken.PARENTESIS_ABRE);
            EXPRESSION();
            match(TipoToken.PARENTESIS_CIERRA);
        }else{
            hayErrores = true;
            System.out.println("Se esperaba 'TRUE' or 'FALSE'"+
            "or 'NULL' or 'ENTERO' or 'DECIMAL' or 'STRING'  or 'IDENTIFICADOR' or 'PARENTESIS_ABRE'.");
        }
    }


//   FUNCTIONS -> FUN_DECL FUNCTIONS | E
    private void FUNCTIONS(){
        if(preanalisis.tipo == TipoToken.FUN){
            FUN_DECL();
            FUNCTIONS();
        }
        //ELSE vacio 
    }

    //   PARAMETERS_OPC -> PARAMETERS | E
    private void PARAMETERS_OPC(){
        if(preanalisis.tipo == TipoToken.IDENTIFICADOR){
            PARAMETERS();
        }
        //ELSE vacio 
    }

    //   PARAMETERS -> id PARAMETERS_2
    private void PARAMETERS(){
        if(preanalisis.tipo == TipoToken.IDENTIFICADOR){
            match(TipoToken.IDENTIFICADOR);
            PARAMETERS_2();
        }else{
            hayErrores = true;
            System.out.println("Se esperaba un 'identificador'");
        }
    }

    //   PARAMETERS_2 -> , id PARAMETERS_2 | E
    private void PARAMETERS_2(){
        if(preanalisis.tipo == TipoToken.COMA){
            match(TipoToken.COMA);
            match(TipoToken.IDENTIFICADOR);
            PARAMETERS_2();
        }
        //ELSE vacio 
    }
    //ELSE_STATEMENT();
    //   ARGUMENTS_OPC -> EXPRESSION ARGUMENTS | E
    private void ARGUMENTS_OPC(){
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
            EXPRESSION();
            ARGUMENTS();
        }
        //ELSE vacio 
    }

    //   ARGUMENTS -> , EXPRESSION ARGUMENTS | E
    private void ARGUMENTS(){
        if(preanalisis.tipo == TipoToken.COMA){
            match(TipoToken.COMA);
            EXPRESSION();
            ARGUMENTS();
        }
        //ELSE vacio 
    }
    private void match(TipoToken tt){
        if(preanalisis.tipo == tt){
            i++;
            preanalisis = tokens.get(i);
        }
        else{
            hayErrores = true;
            System.out.println("Error encontrado");
        }

    }
    /* 
    public void match(TipoToken token) {
        if (!tokens.isEmpty()) {
            tokens.remove(i); // Eliminar el elemento en el índice 0 si la lista no está vacía
            preanalisis = this.tokens.get(i);
            //System.out.println("Nuevo preanalisis."+preanalisis);
        } else {
            // Manejo para el caso en que la lista está vacía
            System.out.println("La lista está vacía. No se puede eliminar ningún elemento.");
        }
        
    }
    */


}

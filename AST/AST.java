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



// DECLARATION -> FUN_DECL DECLARATION | VAR_DECL DECLARATION 
    //                                      | STATEMENT DECLARATION | E
    public void DECLARATION(List <Statement> StateMts){
        if(preanalisis.tipo == TipoToken.FUN){//FUN_DECL DECLARATION
            Statement StmtFUN_DECL = FUN_DECL();
            StateMts.add(StmtFUN_DECL);
            DECLARATION(StateMts);
        }//VAR_DECL DECLARATION
        else if (preanalisis.tipo == TipoToken.VAR) {//VAR_DECL DECLARATION 
            Statement StmtVAR_DECL = VAR_DECL();
            StateMts.add(StmtVAR_DECL);
            DECLARATION(StateMts);
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
            || preanalisis.tipo == TipoToken.LLAVE_ABRE) 
            {
                Statement Stmt = STATEMENT();
                StateMts.add(Stmt);
                DECLARATION(StateMts);
        }
        //ELSE VACIO
    }

    // FUN_DECL -> fun FUNCTION
    public Statement FUN_DECL(){
        if(hayErrores)
            return null;
        if(preanalisis.tipo == TipoToken.FUN){
            match(TipoToken.FUN);
            Statement StmtFUNCTION= FUNCTION();
            return StmtFUNCTION;
        }
        else{
            hayErrores = true;
            System.out.println("Se esperaba un 'FUN'");
            return null;
        }

    }

    // VAR_DECL -> var id VAR_INIT
    public Statement VAR_DECL(){
        if(hayErrores)
            return null;

        Expression exprVAR_DECL=null;
        if(preanalisis.tipo == TipoToken.VAR){
            match(TipoToken.VAR);
            match(TipoToken.IDENTIFICADOR);
            //System.out.println("checkpoint");
            //for(Token token : tokens){
                //System.out.println(token);
            //}
            Token TokenAnterior = previous();
            if (preanalisis.tipo == TipoToken.IGUAL)
                exprVAR_DECL=VAR_INIT(exprVAR_DECL);
            
            match(TipoToken.PUNTO_Y_COMA);
            return new StmtVar(TokenAnterior, exprVAR_DECL);
        }
        else{
            hayErrores = true;
            System.out.println("Se esperaba un 'VAR'");
            return null;
        }
    }
    
    // STATEMENT -> EXPR_STMT | FOR_STMT | IF_STMT
    //              | PRINT_STMT | RETURN_STMT | WHILE_STMT | BLOCK
    public Statement STATEMENT(){
        if(hayErrores)
            return null;
        
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
            
            Statement exprEXPR_STMT=EXPR_STMT();
            return exprEXPR_STMT;
        }
        else if(preanalisis.tipo == TipoToken.FOR){
            Statement exprFOR_STMT= FOR_STMT();
            return exprFOR_STMT;
           
        }
        else if(preanalisis.tipo == TipoToken.IF){
            Statement exprIF_STMT=IF_STMT();
            return exprIF_STMT;
            
        }
        else if(preanalisis.tipo == TipoToken.PRINT){
            Statement exprPRINT_STMT=PRINT_STMT();
            return exprPRINT_STMT;
            
        }
        else if(preanalisis.tipo == TipoToken.RETURN){
            Statement exprRETURN_STMT=RETURN_STMT();
            return exprRETURN_STMT;
            
        }
        else if(preanalisis.tipo == TipoToken.WHILE){
            Statement exprWHILE_STMT=WHILE_STMT();
            return exprWHILE_STMT;
            
        }
        else if(preanalisis.tipo == TipoToken.LLAVE_ABRE){
            Statement exprBLOCK=BLOCK();
            return exprBLOCK;
            
        }else{
            hayErrores = true;
            System.out.println("Se esperaba 'BANG' or 'RESTA' or 'TRUE' or 'FALSE'"+
            "or 'NULL' or 'ENTERO' or 'DECIMAL' or 'STRING'  or 'IDENTIFICADOR' or 'PARENTESIS_ABRE' "+
            "or 'FOR' or 'IF' or 'PRINT' or 'RETURN' or 'WHILE' or '{'");
            return null;
        }
    }
    //DEN

    //BECA

    //BECA
}

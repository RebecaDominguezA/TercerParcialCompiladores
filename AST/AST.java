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
    // FUNCTION -> id ( PARAMETERS_OPC ) BLOCK
    public Statement FUNCTION(){
        if(hayErrores)
            return null;
        if(preanalisis.tipo == TipoToken.IDENTIFICADOR){
            match(TipoToken.IDENTIFICADOR);
            Token name= previous();
            match(TipoToken.PARENTESIS_ABRE);
            List <Token> parametroslList = PARAMETERS_OPC();
            match(TipoToken.PARENTESIS_CIERRA);
            Statement StmtBlock = BLOCK();
            return new StmtFunction(name, parametroslList, (StmtBlock) StmtBlock);
        }else{
            hayErrores = true;
            System.out.println("Se esperaba 'IDENTIFICADOR'");
            return null;
        }
    }

    // VAR_INIT -> = EXPRESSION | E
    public Expression VAR_INIT(Expression expr){
        if(hayErrores)
            return null;
        if(preanalisis.tipo == TipoToken.IGUAL){
            match(TipoToken.IGUAL);
            expr = EXPRESSION();
        }
        //else vacio
        return expr;
    }
    
    //  EXPRESSION -> ASSIGNMENT
    public Expression EXPRESSION(){
        if(hayErrores)
            return null;
        
        return ASSIGNMENT();  
    }

    //  EXPR_STMT -> EXPRESSION
    public Statement EXPR_STMT(){
        if(hayErrores)
            return null;
        
        Expression exprEXPRESSION=EXPRESSION();
        match(TipoToken.PUNTO_Y_COMA);
        return new StmtExpression(exprEXPRESSION);
        
    }

    //  FOR_STMT -> for ( FOR_STMT_1 FOR_STMT_2 FOR_STMT_3 ) STATEMENT
    public Statement FOR_STMT(){
        if(hayErrores)
            return null;
        
        if (preanalisis.tipo== TipoToken.FOR) {
            match(TipoToken.FOR);
            match(TipoToken.PARENTESIS_ABRE);
            Statement StmtFOR_STMT_1 = FOR_STMT_1();//Segun codigo del profe este es un inicializador
            Expression exprFOR_STMT_2 = FOR_STMT_2();//este una condicion
            Expression exprFOR_STMT_3 =FOR_STMT_3();//este un incremento
    
            match(TipoToken.PARENTESIS_CIERRA);

            List<Statement> StateMts = new ArrayList<>();
            //aplicamos add
            StateMts.add(StmtFOR_STMT_1);
            Statement StmtSTATEMENT =STATEMENT();//Es para bucles/ciclos
            if (exprFOR_STMT_3==null){
                StateMts.add(new StmtLoop(exprFOR_STMT_2, StmtSTATEMENT));
            }else{
                StateMts.add(new StmtLoop(exprFOR_STMT_2, new StmtBlock(Arrays.asList(StmtSTATEMENT,new StmtExpression(exprFOR_STMT_3)))   ));
                //Aqui el incremento se mete dentro del bucle mencionado StmtSTATEMENT.
            }
            return new StmtBlock(StateMts);
        }else{
            hayErrores = true;
            System.out.println("Se esperaba 'FOR'");
            return null;
        }
        
    }

    //   if (EXPRESSION) STATEMENT ELSE_STATEMENT
    public Statement IF_STMT(){
        if(hayErrores)
            return null;

        Statement elseBranch = null;
        if (preanalisis.tipo==TipoToken.IF) {
            match(TipoToken.IF);
            match(TipoToken.PARENTESIS_ABRE);
            Expression condition =EXPRESSION();
            match(TipoToken.PARENTESIS_CIERRA);
            Statement thenBranch = STATEMENT();
            if (preanalisis.tipo==TipoToken.ELSE)
                elseBranch= ELSE_STATEMENT(elseBranch);
            
            return new StmtIf(condition, thenBranch, elseBranch);
            
        }else{
            hayErrores=true;
            System.out.println("Se esperaba un 'IF'");
            return null;
        }
    }

    //   PRINT_STMT -> print EXPRESSION;
    public Statement PRINT_STMT(){
        if(hayErrores)
            return null;
        
        if (preanalisis.tipo==TipoToken.PRINT) {
            match(TipoToken.PRINT);
            Expression exprEXPRESSION=EXPRESSION();  
            match(TipoToken.PUNTO_Y_COMA);  
            return new StmtPrint(exprEXPRESSION);
        }else{
            hayErrores=true;
            System.out.println("Se esperaba un 'PRINT'");
            return null;
        }
    }

    //   RETURN_STMT -> return RETURN_EXP_OPC ;
    public Statement RETURN_STMT(){
        if(hayErrores)
            return null;
        
        Expression value=null;
        if (preanalisis.tipo==TipoToken.RETURN) {
            match(TipoToken.RETURN);
            if (preanalisis.tipo == TipoToken.BANG
            || preanalisis.tipo == TipoToken.RESTA
            || preanalisis.tipo == TipoToken.TRUE
            || preanalisis.tipo == TipoToken.FALSE
            || preanalisis.tipo == TipoToken.NULL
            || preanalisis.tipo == TipoToken.ENTERO
            || preanalisis.tipo == TipoToken.DECIMAL
            || preanalisis.tipo == TipoToken.STRING
            || preanalisis.tipo == TipoToken.IDENTIFICADOR
            || preanalisis.tipo == TipoToken.PARENTESIS_ABRE
            ) {
                value = RETURN_EXP_OPC(value);
            }
            match(TipoToken.PUNTO_Y_COMA);
            return new StmtReturn(value);
        }else{
            hayErrores=true;
            System.out.println("Se esperaba un 'RETURN'");
            return null;
        }
        
    }
    
    //   WHILE_STMT -> while ( EXPRESSION ) STATEMENT
    public Statement WHILE_STMT(){
        if(hayErrores)
            return null;
        
        if (preanalisis.tipo==TipoToken.WHILE) {
            match(TipoToken.WHILE);
            match(TipoToken.PARENTESIS_ABRE);
            Expression condition =EXPRESSION();
            match(TipoToken.PARENTESIS_CIERRA);
            Statement body=STATEMENT();
            return new StmtLoop(condition, body);
        }else{
            hayErrores=true;
            System.out.println("Se esperaba un 'WHILE'");
            return null;
        }
    }

    //   BLOCK -> { DECLARATION }
    public Statement BLOCK(){
        if(hayErrores)
            return null;
        
        List <Statement> StateMts =new ArrayList<>();
        if (preanalisis.tipo==TipoToken.LLAVE_ABRE) {
            match(TipoToken.LLAVE_ABRE);
            DECLARATION(StateMts);
            match(TipoToken.LLAVE_CIERRA);
            return new StmtBlock(StateMts);
        }else{
            hayErrores=true;
            System.out.println("Se esperaba un 'LLAVE_ABRE'");
            return null;
        }
        
    }

    //DEN


//   FOR_STMT_1 -> VAR_DECL | EXPR_STMT | ;
    public Statement FOR_STMT_1(){
        if(hayErrores)
            return null;
        
        if(preanalisis.tipo == TipoToken.VAR){
            return VAR_DECL();
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
            return EXPR_STMT();
        }
        else if (preanalisis.tipo == TipoToken.PUNTO_Y_COMA){
            match(TipoToken.PUNTO_Y_COMA);
            return null;
        }
        else{
            hayErrores = true;
            System.out.println("Se esperaba un 'VAR' or 'BANG' or 'RESTA' or 'TRUE' or 'FALSE'"+ 
            "or 'NULL' or 'ENTERO' or 'DECIMAL' or 'STRING'  or 'IDENTIFICADOR' or 'PARENTESIS_ABRE' or ';'");
            return null;
        }
    }

    //   FOR_STMT_2 -> EXPRESSION ; | ;
    public Expression FOR_STMT_2(){
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
            Expression exprEXPRESSION = EXPRESSION();
            match(TipoToken.PUNTO_Y_COMA);
            return exprEXPRESSION;
        }
        else if (preanalisis.tipo == TipoToken.PUNTO_Y_COMA){
            match(TipoToken.PUNTO_Y_COMA);
            return new ExprLiteral(true);
        }
        else{
            hayErrores = true;
            System.out.println("Se esperaba un 'BANG' or 'RESTA' or 'TRUE' or 'FALSE'"+ 
            "or 'NULL' or 'ENTERO' or 'DECIMAL' or 'STRING'  or 'IDENTIFICADOR' or 'PARENTESIS_ABRE' or ';'");
            return null;
        }
    }

    //   FOR_STMT_3 -> EXPRESSION | E
    public Expression FOR_STMT_3(){
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
            return EXPRESSION();
        }
        //else vacio
        return null;
    }

    //   ELSE_STATEMENT -> else STATEMENT | E
    public Statement ELSE_STATEMENT(Statement elseBranch){
        if(hayErrores)
            return null;
        
        if(preanalisis.tipo == TipoToken.ELSE){
            match(TipoToken.ELSE);
            elseBranch=STATEMENT();
            return elseBranch;
        }
        //else caso vacio
        return elseBranch;
    }

    //   RETURN_EXP_OPC -> EXPRESSION | E
    public Expression RETURN_EXP_OPC(Expression value){
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
            value = EXPRESSION();
            return value;
        }
        //else vacio
        return value;
    }

    //   ASSIGNMENT -> LOGIC_OR ASSIGNMENT_OPC
    public Expression ASSIGNMENT(){
        if(hayErrores)
            return null;
        Expression exprLOGIC_OR = LOGIC_OR();
        if (preanalisis.tipo==TipoToken.IGUAL) 
            exprLOGIC_OR=ASSIGNMENT_OPC(exprLOGIC_OR);
        
        return exprLOGIC_OR;
        
    }

    //   ASSIGNMENT_OPC -> = EXPRESSION | E
    public Expression ASSIGNMENT_OPC(Expression expr){
        if(hayErrores)
            return null;

        if(preanalisis.tipo == TipoToken.IGUAL){
            //la lógica de asignación se aplica específicamente 
            //cuando se trata de asignar valores a variables 
            //en el código fuente durante el análisis sintáctico.
            if (expr instanceof ExprVariable) {
                Token name = ((ExprVariable) expr).name;
                match(TipoToken.IGUAL);
                Expression value = EXPRESSION();
                return new ExprAssi(name, value);
            }
        }
        //ELSE vacio 
        return expr;
    }

    //   LOGIC_OR -> LOGIC_AND LOGIC_OR_2
    public Expression LOGIC_OR(){
        if(hayErrores)
            return null;
        
        Expression exprLOGIC_AND =LOGIC_AND();
        if (preanalisis.tipo == TipoToken.OR) {
            exprLOGIC_AND = LOGIC_OR_2(exprLOGIC_AND);
        }
        return exprLOGIC_AND;
    }

    //   LOGIC_OR_2 -> or LOGIC_AND LOGIC_OR_2 | E
    public Expression LOGIC_OR_2(Expression left){
        if(hayErrores)
            return null;
            
        if(preanalisis.tipo == TipoToken.OR){
            match(TipoToken.OR);
            Token operator = previous();
            Expression right = LOGIC_AND();
            ExprLogical exprJunta = new ExprLogical(left, operator, right);
            return LOGIC_OR_2(exprJunta);
        }
        //ELSE vacio  
        return left;
    }

    //   LOGIC_AND -> EQUALITY LOGIC_AND_2
    public Expression LOGIC_AND(){
        if(hayErrores)
            return null;
        
        Expression exprEQUALITY = EQUALITY();
        if (preanalisis.tipo==TipoToken.AND) {
            exprEQUALITY = LOGIC_AND_2(exprEQUALITY);
        }
        return exprEQUALITY;
    }

    //   LOGIC_AND_2 -> and EQUALITY LOGIC_AND_2 | E
    public Expression LOGIC_AND_2(Expression left){
        if(hayErrores)
            return null;
            
        if(preanalisis.tipo == TipoToken.AND){
            match(TipoToken.AND);
            Token operator = previous();
            Expression right = EQUALITY();
            ExprLogical exprJunta = new ExprLogical(left, operator, right);
            
            return LOGIC_AND_2(exprJunta);
        }
        //ELSE vacio 
        return left;
    }

    //   EQUALITY -> COMPARISON EQUALITY_2
    public Expression EQUALITY(){
        if(hayErrores)
            return null;
            
        Expression exprCOMPARISON = COMPARISON();
        if (preanalisis.tipo == TipoToken.DIFERENTE_QUE
            ||preanalisis.tipo == TipoToken.IGUAL_IGUAL) {
            exprCOMPARISON= EQUALITY_2(exprCOMPARISON);
        }
        return exprCOMPARISON;
    }

    //   EQUALITY_2 -> != COMPARISON EQUALITY_2 | == COMPARISON EQUALITY_2 | E
    public Expression EQUALITY_2(Expression left){
        if(hayErrores)
            return null;
            
        if(preanalisis.tipo == TipoToken.DIFERENTE_QUE){
            match(TipoToken.DIFERENTE_QUE);
            Token operator = previous();
            Expression right=COMPARISON();
            ExprBinary exprJunta = new ExprBinary(left, operator, right);
            
            return EQUALITY_2(exprJunta);
        }
        else if(preanalisis.tipo == TipoToken.IGUAL_IGUAL){
            match(TipoToken.IGUAL_IGUAL);
            Token operator = previous();
            Expression right=COMPARISON();
            ExprBinary exprJunta = new ExprBinary(left, operator, right);
            
            return EQUALITY_2(exprJunta);
        }
        //ELSE vacio 
        return left;
    }


    //   COMPARISON -> TERM COMPARISON_2
    public Expression COMPARISON(){
        if(hayErrores)
            return null;
        
        Expression exprTERM=TERM();
        if (preanalisis.tipo == TipoToken.MAYOR_QUE 
        ||preanalisis.tipo == TipoToken.MAYOR_IGUAL_QUE 
        || preanalisis.tipo == TipoToken.MENOR_QUE 
        || preanalisis.tipo == TipoToken.MENOR_IGUAL_QUE) {
            exprTERM= COMPARISON_2(exprTERM);
        }
        return exprTERM;
    }

    //   COMPARISON_2 -> > TERM COMPARISON_2 | >= TERM COMPARISON_2 |
    //                   < TERM COMPARISON_2 | <= TERM COMPARISON_2 | E
    public Expression COMPARISON_2(Expression left){
        if(hayErrores)
            return null;
            
        if(preanalisis.tipo == TipoToken.MAYOR_QUE){
            match(TipoToken.MAYOR_QUE);
            Token operator = previous();
            Expression right= TERM();
            ExprBinary exprJunta= new ExprBinary(left, operator, right);
            return COMPARISON_2(exprJunta);
        }
        else if(preanalisis.tipo == TipoToken.MAYOR_IGUAL_QUE){
            match(TipoToken.MAYOR_IGUAL_QUE);
            Token operator = previous();
            Expression right= TERM();
            ExprBinary exprJunta= new ExprBinary(left, operator, right);
            return COMPARISON_2(exprJunta);
            
        }
        else if(preanalisis.tipo == TipoToken.MENOR_QUE){
            match(TipoToken.MENOR_QUE);
            Token operator = previous();
            Expression right= TERM();
            ExprBinary exprJunta= new ExprBinary(left, operator, right);
            return COMPARISON_2(exprJunta);
        }
        else if(preanalisis.tipo == TipoToken.MENOR_IGUAL_QUE){
            match(TipoToken.MENOR_IGUAL_QUE);
            Token operator = previous();
            Expression right= TERM();
            ExprBinary exprJunta= new ExprBinary(left, operator, right);
            return COMPARISON_2(exprJunta);
        }
        //Else vacio
        return left;
    }

    //   TERM -> FACTOR TERM_2
    public Expression TERM(){
        Expression exprFACTOR=FACTOR();
        if (preanalisis.tipo == TipoToken.RESTA
        || preanalisis.tipo == TipoToken.SUMA) {
            exprFACTOR =TERM_2(exprFACTOR);
        }
        return exprFACTOR;
    }

    // TERM_2 -> - FACTOR TERM_2 | + FACTOR TERM_2 | E
    public Expression TERM_2(Expression left){
        if(hayErrores)
            return null;
            
        if(preanalisis.tipo == TipoToken.RESTA){
            match(TipoToken.RESTA);
            Token operator = previous();
            Expression right= FACTOR();
            ExprBinary exprJunta= new ExprBinary(left, operator, right);
            return TERM_2(exprJunta);
        }
        else if(preanalisis.tipo == TipoToken.SUMA){
            match(TipoToken.SUMA);
            Token operator = previous();
            Expression right= FACTOR();
            ExprBinary exprJunta= new ExprBinary(left, operator, right);
            return TERM_2(exprJunta);
        }
        //ELSE VACIO
        return left;
    }

    // FACTOR -> UNARY FACTOR_2
    public Expression FACTOR(){
        Expression exprUNARY = UNARY();
        if (preanalisis.tipo == TipoToken.SLASH
        || preanalisis.tipo == TipoToken.ESTRELLA) {
            exprUNARY=FACTOR_2(exprUNARY);
        }
        return exprUNARY;
    }

    // FACTOR_2 -> / UNARY FACTOR_2 | * UNARY FACTOR_2 | E
    public Expression FACTOR_2(Expression expr){
        
        if(preanalisis.tipo == TipoToken.SLASH){
            match(TipoToken.SLASH);
            Token operador = previous();
            Expression expr2 = UNARY();
            ExprBinary expb = new ExprBinary(expr, operador, expr2);
            return FACTOR_2(expb);
        }
        else if(preanalisis.tipo == TipoToken.ESTRELLA){
            
            match(TipoToken.ESTRELLA);
            Token operador = previous();
            Expression expr2 = UNARY();
            ExprBinary expb = new ExprBinary(expr, operador, expr2);
            return FACTOR_2(expb);
        }
        //ELSE VACIO
        return expr;
    }

    // UNARY -> ! UNARY | - UNARY | CALL
    public Expression UNARY(){
        if(hayErrores)
            return null;

        if(preanalisis.tipo == TipoToken.BANG){
            match(TipoToken.BANG);
            Token operador = previous();
            Expression expr = UNARY();
            return new ExprUnary(operador, expr);
        }
        else if(preanalisis.tipo == TipoToken.RESTA){
            match(TipoToken.RESTA);
            Token operador = previous();
            Expression expr = UNARY();
            return new ExprUnary(operador, expr);
        }else if(preanalisis.tipo == TipoToken.TRUE 
        || preanalisis.tipo == TipoToken.FALSE 
        || preanalisis.tipo == TipoToken.NULL 
        || preanalisis.tipo == TipoToken.DECIMAL 
        || preanalisis.tipo == TipoToken.ENTERO
        || preanalisis.tipo == TipoToken.STRING 
        || preanalisis.tipo == TipoToken.IDENTIFICADOR 
        || preanalisis.tipo == TipoToken.PARENTESIS_ABRE){
            return CALL();
        }else{
            hayErrores=true;
            System.out.println("Se esperaba BANG or Resta or TRUE or FALSE or NULL or DECIMAL or ENTERO or String or IDDENTIFICADOR o Parentesis_abre");
            return null;
        }
    }

    //DEN

// CALL -> PRIMARY CALL_2
    public Expression CALL(){
        Expression exprPRIMARY = PRIMARY();
        exprPRIMARY = CALL_2(exprPRIMARY);
        return exprPRIMARY;
    }

    //   CALL_2 -> ( ARGUMENTS_OPC ) CALL_2 | E
    public Expression CALL_2(Expression callee){
        if(hayErrores)
            return null;

        if(preanalisis.tipo == TipoToken.PARENTESIS_ABRE){
            match(TipoToken.PARENTESIS_ABRE);
            List<Expression> arguments = new ArrayList<>();
            arguments = ARGUMENTS_OPC();
            //se retorna un alista de argumentos
            ExprCallFunction ecf = new ExprCallFunction(callee, arguments);
            return CALL_2(ecf);
        }
        //ELSE vacio 
        return callee;
    }

    //   PRIMARY -> true | false | null | number | string | id | ( EXPRESSION )
    private Expression PRIMARY(){
        if(preanalisis.tipo == TipoToken.TRUE){
            match(TipoToken.TRUE);
            return (new ExprLiteral(true));
        }
        else if(preanalisis.tipo == TipoToken.FALSE){
            match(TipoToken.FALSE);
            return new ExprLiteral(false);
        }
        else if(preanalisis.tipo == TipoToken.NULL){
            match(TipoToken.NULL);
            return new ExprLiteral(null);
        }
        else if(preanalisis.tipo == TipoToken.DECIMAL){
            match(TipoToken.DECIMAL);
            Token numero = previous();
            return new ExprLiteral(numero.getLiteral());
        }
        else if(preanalisis.tipo == TipoToken.ENTERO){
            match(TipoToken.ENTERO);
            Token numero = previous();
            return new ExprLiteral(numero.getLiteral());
        }
        else if(preanalisis.tipo == TipoToken.STRING){
            match(TipoToken.STRING);
            Token cadena = previous();
            return new ExprLiteral(cadena.getLiteral());
        }
        else if(preanalisis.tipo == TipoToken.IDENTIFICADOR){
            match(TipoToken.IDENTIFICADOR);
            Token id = previous();
            return new ExprVariable(id);
        }
        else if(preanalisis.tipo == TipoToken.PARENTESIS_ABRE){
            match(TipoToken.PARENTESIS_ABRE);
            Expression exprEXPRESSION = EXPRESSION();
            // Tiene que ser cachado aquello que retorna
            match(TipoToken.PARENTESIS_CIERRA);
            return exprEXPRESSION; //new ExprGrouping(exprEXPRESSION);
        }else{
            hayErrores=true;
            System.out.println("Se esperaba 'TRUE' or 'FALSE'"+
            "or 'NULL' or 'ENTERO' or 'DECIMAL' or 'STRING'  or 'IDENTIFICADOR' or 'PARENTESIS_ABRE'.");
            return null;
        }
    }
    //DEN

    //BECA

    //BECA
}


public class StmtVar extends Statement {
    final Token name;
    final Expression initializer;

    StmtVar(Token TokenAnterior, Expression exprVAR_DECL) {
        this.name = TokenAnterior;
        this.initializer = exprVAR_DECL;
    }
}

public class StmtFor extends Statement{
    final Statement initializer;
    final Expression condition;
    final Expression increase;
    final Statement body;

    StmtFor(Statement initializer, Expression condition, Expression increase, Statement body){
        this.initializer=initializer;
        this.condition=condition;
        this.increase=increase;
        this.body=body;
    }
}

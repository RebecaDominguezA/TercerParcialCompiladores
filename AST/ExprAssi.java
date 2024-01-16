public class ExprAssi extends Expression{
    final Token name;
    final Expression value;

    ExprAssi(Token name, Expression value) {
        this.name = name;
        this.value = value;
    }
}

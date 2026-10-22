/// Plain assertions on purpose: this snippet stays dependency free.
public class ShapesTest {

    public static void main(String[] args) {
        check(Shapes.area(new Shapes.Square(3)) == 9, "square area");
        check(Shapes.area(new Shapes.Rectangle(2, 5)) == 10, "rectangle area");
        check(Math.abs(Shapes.area(new Shapes.Circle(1)) - Math.PI) < 1e-9, "circle area");
        check(Shapes.describe(new Shapes.Circle(0)).equals("a point"), "guarded case wins over the general one");
        check(Shapes.describe(new Shapes.Rectangle(2, 2)).contains("disguise"), "record deconstruction in a guard");
        check(new Shapes.Square(2).equals(new Shapes.Square(2)), "records get value equality for free");
        System.out.println("ok");
    }

    private static void check(boolean condition, String what) {
        if (!condition) {
            throw new AssertionError(what);
        }
    }
}

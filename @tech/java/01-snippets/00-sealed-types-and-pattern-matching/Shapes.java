import java.util.List;

/// Sealed interface + records + pattern matching for switch (Java 21+).
public class Shapes {

    sealed interface Shape permits Circle, Rectangle, Square {}

    record Circle(double radius) implements Shape {}

    record Rectangle(double width, double height) implements Shape {}

    record Square(double side) implements Shape {}

    static double area(Shape shape) {
        // No default branch: the compiler knows every permitted subtype,
        // so adding a new Shape breaks the build here instead of at runtime.
        return switch (shape) {
            case Circle(double radius) -> Math.PI * radius * radius;
            case Rectangle(double width, double height) -> width * height;
            case Square(double side) -> side * side;
        };
    }

    static String describe(Shape shape) {
        return switch (shape) {
            case Circle c when c.radius() == 0 -> "a point";
            case Circle c -> "a circle of radius " + c.radius();
            case Rectangle(double w, double h) when w == h -> "a square in disguise";
            case Rectangle r -> "a rectangle";
            case Square s -> "a square";
        };
    }

    public static void main(String[] args) {
        List<Shape> shapes = List.of(new Circle(1), new Rectangle(2, 3), new Rectangle(2, 2), new Square(4), new Circle(0));
        for (Shape shape : shapes) {
            System.out.printf("%-60s area=%.2f%n", shape + " is " + describe(shape), area(shape));
        }
    }
}

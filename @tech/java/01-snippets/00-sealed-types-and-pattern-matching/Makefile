.PHONY: run test clean

out: Shapes.java ShapesTest.java
	javac -d out $^

run: out
	java -cp out Shapes

test: out
	java -cp out ShapesTest

clean:
	rm -rf out

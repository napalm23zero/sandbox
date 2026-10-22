package main

import (
	"fmt"
	"runtime"
)

func main() {
	fmt.Printf("hello from a %s/%s binary in an empty image\n", runtime.GOOS, runtime.GOARCH)
}

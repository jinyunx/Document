```go
package main

import "fmt"

type SortInterface interface {
	Len() int
	Less(i, j int) bool
	Swap(i, j int)
}

// Array 实现 SortInterface
type Array []int

func (arr Array) Len() int {
	return len(arr)
}

func (arr Array) Less(i, j int) bool {
	return arr[i] < arr[j]
}

func (arr Array) Swap(i, j int) {
	arr[i], arr[j] = arr[j], arr[i]
}

// 使用匿名SortInterface，reverse相当于是个container
// 其主要作用是特例化SortInterface的性质
type reverse struct {
	SortInterface
}

// 特例化Less
func (r reverse) Less(i, j int) bool {
	return r.SortInterface.Less(j, i)
}

// reverse作为container，往往从SortInterface的其他实例初始化，因为其需要初始化SortInterface
// SortInterface的实例放进container之后，container的性质将会覆盖实例的性质
func Reverse(data SortInterface) SortInterface {
	return &reverse{data}
}

func main() {
	test := reverse{} // 直接实例化reverse，SortInterface为空指针
	fmt.Println(test) // {<nil>}
	fmt.Println(test.Less(0, 1)) // panic: runtime error: invalid memory address or nil pointer dereference

	arr := Array{1, 2, 3}
	rarr := Reverse(arr) // 正确用法
	fmt.Println(arr.Less(0, 1))
	fmt.Println(rarr.Less(0, 1))
}

```
# Go的interface的实现
 在Go语言中interface是一个非常重要的概念，也是与其它语言相比存在很大特色的地方。interface也是一个Go语言中的一种类型，是一种比较特殊的类型，存在两种interface，一种是带有方法的interface，一种是不带方法的interface。Go语言中的所有变量都可以赋值给空interface变量，实现了interface中定义方法的变量可以赋值给带方法的interface变量，并且可以通过interface直接调用对应的方法，实现了其它面向对象语言的多态的概念。

# 内部定义

两种不同的interface在Go语言内部被定义成如下的两种结构体
```go
// 没有方法的interface
type eface struct {
    _type *_type
    data  unsafe.Pointer
}

// 记录着Go语言中某个数据类型的基本特征
type _type struct {
    size       uintptr
    ptrdata    uintptr
    hash       uint32
    tflag      tflag
    align      uint8
    fieldalign uint8
    kind       uint8
    alg        *typeAlg
    gcdata    *byte
    str       nameOff
    ptrToThis typeOff
}

// 有方法的interface
type iface struct {
    tab  *itab
    data unsafe.Pointer
}

type itab struct {
    inter  *interfacetype
    _type  *_type
    link   *itab
    hash   uint32
    bad    bool
    inhash bool
    unused [2]byte
    fun    [1]uintptr
}

// interface数据类型对应的type
type interfacetype struct {
    typ     _type
    pkgpath name
    mhdr    []imethod
}
```
可以看到两种类型的interface在内部实现时都是定义成了一个2个字段的结构体，所以任何一个interface变量都是占用16个byte的内存空间。
 在Go语言中_type这个结构体非常重要，记录着某种数据类型的一些基本特征，比如这个数据类型占用的内存大小（size字段），数据类型的名称（nameOff字段）等等。每种数据类型都存在一个与之对应的_type结构体（Go语言原生的各种数据类型，用户自定义的结构体，用户自定义的interface等等）。如果是一些比较特殊的数据类型，可能还会对_type结构体进行扩展，记录更多的信息，比如interface类型，就会存在一个interfacetype结构体，除了通用的_type外，还包含了另外两个字段pkgpath和mhdr，后文在对这两个字段的作用进行解析。除此之外还有其它类型的数据结构对应的结构体，比如structtype，chantype，slicetype，有兴趣的可以在$GOROOT/src/runtime/type.go文件中查看。
# 赋值
上面的例子都是将一个指针赋值给interface变量，如果是将一个值赋值给interface变量。会先对分配一块空间保存该值的副本，然后将该interface变量的data字段指向这个新分配的空间。将一个值赋值给interface变量时，操作的都是该值的一个副本。

# receiver的理解
go中将定义struct的方法中的func() 中的参数称为receiver。例如func(s St) Get() int { }中的s就是Get的receiver。要理解他可以联想C++中的this指针。
我们在上面的例子中调用test函数是test(&s)，也就是St的指针类型，可以是test(s)吗？
调用test(s)的执行结果如下：

这是一个错误的实现，关键在于St中Set()方法的receiver是一个pointer *St。

interface定义时并没有规定是闲着的方法receiver是value receiver 还是pointer receiver，如上述例子，当我们使用test(s)的形式调用，传递给test的是s的一份拷贝，在进行s的拷贝到Inter的转换时，s的拷贝不满速Set()方法的receiver是个pointer，也就是没有实现。

而如果反过来receiver是value，函数用pointer的形式调用.
如果是传入pointer，go可以根据pointer找到对应指向的值，但如果是value，传入的只能是value的拷贝temp，没办法根据value的拷贝temp去找到value原始的地址，这就是为什么pointer可以对应pointer receiver以及value receiver，但value却无法满足pointer receiver。

其实这里很关键的一点就是，实参到形参只是一个拷贝。

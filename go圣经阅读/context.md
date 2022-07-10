### Context
#### Context核心能力
ctx用于同步取消、超时、k-v信息到子routine
### Context使用
#### 父routine
1. 可往ctx添加超时或者添加cancel的能力
2. 可以主动调用cancel函数结束所有子routine
3. 把ctx传给子routine
#### 子routine
1. 使用select 读取Context的done chan来感知当前任务是否要结束
2. 读取Err看done的原因，要么超时，要么被主动cancel
### 理解Context
1. Context是一棵树
2. 每个父routine为了实现cancel和超时能力，可以往树中添加一个节点，其子routine将读取该节点的done chan
3. 节点新增的信息是不可以变更的，子routine只能继续增加节点
4. cancel和超时将会传递到当前ctx和子树，意味着子节点继承父节点的属性
5. 父节点被调用cancel，父节点的cancel函数会调用其子树的所有子节点的cancel函数，超时同理
6. valueCtx是一个链表，子节点指向父节点，找某个值的时候会从下往上找，找到相同key的值进行返回，效率很低，而且根据寻找的规则，相当于子节点的值会覆盖父节点的值，不推荐使用。
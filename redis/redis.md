# redis 命令
```bash
# 安装redis
apt-get install redis

# 登录redis数据库
redis-cli     # 打开redis命令行工具
auth passward # 输入密码

# 配置，配置文件/etc/redis/redis.conf
config get bind  # bind配置无法动态set，只能修改配置文件
config get port

# 启动
redis-server
redis-server /xxx/redis.conf
systemctl start redis
systemctl stop redis
systemctl restart redis

# 查看客户端
client list

```

# redis事务
- 定义：redis事务是将多个命令请求打包，然后一次性、按顺序地执行多个命令的机制，在事务执行期间，服务器不会中断事务而改去执行其他客户端的命令请求
- 命令：
  - `MULTI` 事务开始
  - `EXEC` 事务执行
    ```bash
    redis->MULTI
    OK

    redis->SET "name" "hellp"
    QUEUED

    redis->GET "name"
    QUEUED

    redis->EXEC
    1)OK
    2)"hellp"
    ```
  - `WATCH` 监视数据库键（可以多个），EXEC命令执行时，如果被监视的键至少有一个被修改过，服务器将拒绝执行事务，并向客户端返回执行失败的空回复
    ```bash
    redis-> WATCH "name"
    OK

    # 另一个客户端修改name
    # set name "haha"

    redis-> MULTI
    OK

    redis-> SET "name" "peter"
    QUEUED

    redis-> EXEC
    (nil)
    ```


# redis数据类型

### Strings
- 字符串，能够存储文本、序列化对象、二进制数组
- redis的键是字符串
- 最大512MB

- SET
  - SET key value 默认覆盖存在的值
  - SET key value nx 仅当key不在存在时才设置新的值
  - SET key vlaue xx 仅当key已经存在时才设置新的值
  - EX PX可以设置过期时间

- GET
  - GET mykey
  - 根据key获取值，key不存在则返回nil
  - key不是字符串，则会返回错误
  
- GETDEL
  - 功能类似GET，但是成功获取值会删除该键
  
- MGET
  - `MGET key [key ...]`
  - 返回多个key的值
  - key不存在 或 key对应值不是字符串，返回nil

- GETEX
  - 功能类似GET
  - 带有附加选项
    - EX 秒, 设置指定过期时间
    - PX 毫秒, 设置指定的过期时间
    - EXAT 设置密钥过期的指定Unix时间，秒秒
    - PXAT 设置密钥过期的指定Unix时间，毫秒
    - PERSIST 删除与过期时间

- APPEND
  - APPEND mykey "Hello" mykey不存在则创建空字符串，存在则在后面添加Hello

- SUBSTR
  - `SUBSTR key start stop`
  - 返回子字符串

- DECR
- DECRBY
  - SET mykey "10"
  - DECR mykey mykey变为"9"
  - DECRBY mykey 3 mykey变为"7"
  - 如果键不存在，则先初始化为"0"
  - 如果键不是整数，则会返回错误
    
### List
- 字符串值的链表，实现堆栈和队列
- 最大长度2^32-1个元素
- 访问头部和尾部操作复杂度为O(1)


- LPUSH
  - `LPUSH key element [element ...]`
  - 插入元素到列表头部，支持一次插入多个元素
  - 返回插入后列表长度
  - 列表不存在，则创建空列表
  - key不是列表，返回错误

- LPUSHX
  - 基本同LPUSH
  - key不存在或key不为列表，则不执行任何操作
  - 返回插入后列表长度

- LPOP
  - `LPOP key [count]`
  - 从列表头部弹出count个元素，默认为1
  - 返回弹出元素后列表长度

- BLPOP
  - `BLPOP key [key ...] timeout`
  - 第一个不为空的列表头部弹出一个元素
  - 所有列表都为空则阻塞
  - timeout=0，不会超时

- RPUSH
  - `RPUSH key element [element ...]`
  - 将元素插入到列表尾部
  - 返回插入后列表长度
  - 列表不存在，则创建空列表
  - key不是列表，返回错误

- RPUSHX
  - 基本同RPUSH
  - key不存在或key不为列表，则不执行任何操作
  - 返回插入后列表长度

- RPOP
  - `RPOP key [count]`
  - 从列表尾部弹出count个元素，默认为1
  - 返回弹出元素后列表长度

- BRPOP
  - `BRPOP key [key ...] timeout`
  - 第一个不为空的列表尾部弹出一个元素
  - 所有列表都为空则阻塞
  - timeout=0，不会超时

- LMPOP
  - `LMPOP numkeys key [key ...] <LEFT|RIGHT> [COUNT count]`
  - 从第一个不为空的列表中弹出count个元素，count不传入，默认为1
  - 弹出位置通过LEFT和RIGHT指定

- BLMPOP
  - `BLMPOP timeout numkeys key [key ...] <LEFT|RIGHT> [COUNT count]`
  - 行为同LMPOP
  - 当所有列表都为空时阻塞
  - timeout = 0时，不限时间，指到有列表不为空

- LSET
  - `LSET key index element`
  - 设置element到列表index位置（覆盖原有值）
  - index超出范围则报错

- LINSERT
  - `LINSERT key <BEFORE|AFTER> pivot element`
  - 把element插入列表key，位置是pivot元素前面|后面
  - key不存在，认为是空列表，不执行任何操作
  - key存在，但不存在pivot元素，将返回错误

- LLEN
  - `LLEN key`
  - 返回列表的元素个数
  - key不存在返回0
  - key存在但存储的值不是列表，返回错误

- LINDEX
  - `LINDEX key index`
  - 返回key对应列表索引index位置的元素

- LPOS
  - `LPOS key element [RANK rank] [COUNT num-matches] [MAXLEN len]`
  - 默认从头到尾查找element，返回找到的第一个element的index
  - rank表示存在多个匹配项时，返回第几个匹配项的index，默认为1（第一个）
  - count表示返回前几个匹配项的下表，默认1，填0时表示返回所有匹配项的index
  - 使用count但未找到，返回空数组
  - 未使用count但未找到，返回nil
  - len表示最大比较次数

- LMOVE
  - `LMOVE source dest <LEFT|RIGHT> <LEFT|RIGHT>
  - 原子删除source的一个元素，并存储在dest
  - 删除和存储位置（头或尾）通过LEFT和RIGHT参数指定
  - source不存在，返回nil
  
- BLMOVE
  - `BLMOVE source dest <LEFT|RIGHT> <LEFT|RIGHT> timeout`
  - 移动source列表元素到dest列表，source不存在或为空则阻塞，直到source有元素或timeout到达
  - LEFT和RIGHT控制移除和插入的地方（头还是尾）

- LRANGE
  - `LRANGE key start stop`
  - 返回下表start到下表stop的所有元素
  - start大于列表最后一个元素索引，返回空列表
  - stop大于列表最后一个元素索引，stop自动赋值为最后一个元素索引
  - 正向索引0开始，逆向索引-1开始

- LREM
  - `LREM key count element`
  - 删除列表中element元素
  - count = 0，全部删除
  - count > 0, 删除前count个
  - count < 0, 删除后|count|个

- LTRIM
  - `LTRIM key start stop`
  - 裁剪列表，下表start-stop的元素
  - start > end后start > 最大索引，返回空列表（key列表被删除）
  - end > 最大索引，则end = 最大索引

### Hash
 - HSET
 - HMSET
 - HDEL
 - HGET
 - HMGET
 - HGETALL
 - HKEYS


### List
 - LSET
 - LPUSH
 - RPUSH
 - LRANGE
 - BLPOP
 - BRPOP
 - LPOP
 - LREM
 - LINDEX
 - LRANGE

### Set
 - SADD
 - SPOP
 - SREM
 - SISMEMBER
### ZSet
 - ZADD
 - ZREM
 - ZREMRANGEBYLEX
 - ZREMRANGEBYRANK
 - ZREMRANGEBYSCORE

### JSON命令
- JSON.SET key path value
- JSON.GET key path
- JSON.DEL key path
- JSON.TYPE key path 获取数据类型
- JSON.NUMINCREBY 加法
- JSON.NUMMULTBY 乘法
- JSON.ARRAPPEND key path value [value ...]
- JSON.ARRINSERT 
- JSON.ARRTRIM 
- JSON.ARRPOP
- JSONPath语法
  | 符号 | 说明 |
  | - | - |
  | $ | 开始符号，单独一个$表示根路径 |
  | .或者[] | 选择子元素 |
  | [] | 下表运算符，访问数组元素，下表从0开始 |
  | [,] | 联合，选择多个元素
  | .. | 递归遍历json文档 |
  | * | 通配符 |
  | start:end:step | 数组切片，[*]或[:]选择所有元素 |
  | ?() | 过滤json对象或数组 |
  | () | 脚本 |
  | @ | 当前元素，用于过滤器或脚本表达式 |

# redis持久化
## RDB
- 经过压缩的二进制文件（RDB文件）
- `SAVE`命令 会阻塞Redis服务进程
- `BGSAVE`命令 BackGround SAVE，增加一个子进程负责创建RDB文件
  - 可以设置条件，让服务器每隔一段时间自动保存
    ```shell
    save 900 1          # 900秒内对数据库至少进行了1次修改
    save 300 10         # 300秒内对数据库至少进行了10次修改
    save 60 10000       # 60秒内对数据库至少进行了10000次修改
    ```
- 服务器启动时检测到RDB文件存在，自动加载
- RDB持久化记录的是数据库本身的数据

## AOF
- 记录Redis服务器所执行的写命令
- AOF：Append Only File
- 配置项`appendfsync`，默认`everysec`
  - `always`: 每次写操作都立即写入并同步到AOF文件
  - `everysec`：每次写操作都立即写入AOF文件，如果上次同步AOF文件的时间举例现在超过一秒，那么在此对AOF文件进行同步
  - `no`：每次写操作都立即写入AOF文件，但并不对AOF文件进行同步，何时同步由操作系统来决定
- AOF重写：多次写入，只保留最后一次命令


# 常见面试题
## 缓存雪崩
- 是什么：1. 大量redis缓存数据同时失效，导致大量数据库请求 2.redis服务器挂了
- 怎么办：1. 缓存是过期时间随机                          2.哨兵，集群

## 缓存穿透
- 是什么：查询不存在的数据，由于缓存不命中，从数据库查询也查不到，未写入缓存，导致这个不存在的数据每次请求都要查询数据库
- 怎么办：布隆过滤器；数据库查不到也把空数据写入缓存（设置较短的过期时间）

## 缓存击穿
- 是什么：大量请求同时查询一个key时，此时这个key正好失效了，会导致大量请求查询数据库
- 怎么办：热点数据不设置过期时间，双检枷锁策略

## 缓存和数据库双写不一致
- 是什么
  - 先更新数据库，再删除缓存：原子性被破坏时导致数据不一致（更新了库，没删缓存）；并发场景出问题概率较低
  - 先删除缓存，在更新数据库：原子性被破坏时不影响一致性；并发时问题很大

- 怎么办
  - 将多个线程中的删除缓存，修改数据库，读取缓存等的操作挤压到队列里，实现串行化

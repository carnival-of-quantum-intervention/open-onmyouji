# 总述

本工具库集成了在游戏过程中可能用到的部分识别及操作方法。

## 配置

工具库自带的配置文件将支持大部分副本，同时您也可以通过修改配置文件支持其它副本的识别操作。

### 格式

JSON 配置文件的根对象需要有字符串标题，即 title 属性，这个属性用于根据窗口名称找到工具需要作用的窗口。除此之外，根对象需要有 config 属性，这是一个数组，由关于不同副本的配置组成。

每个副本配置需要有name属性，指示其展示在配置列表中时的名称。
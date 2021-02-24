# 总述

本工具库集成了在游戏过程中可能用到的部分识别及操作方法。

## 配置格式

工具库自带的配置文件将支持阴阳师的大部分副本，同时您也可以通过修改配置文件支持其它副本甚至其他游戏的识别操作。

### 配置对象

JSON 配置文件的根对象需要有字符串标题，即 title 属性，这个属性用于根据窗口名称找到该配置文件作用的窗口。除此之外，根对象需要有 config 属性，这是一个数组，由不同副本流程的配置组成。

### 配置名称

副本流程配置需要有name属性，指示该副本流程展示在列表中时的名称。

### 配置任务

副本流程配置需要有task属性，指示该副本流程需要执行的任务操作。

### 任务种类

任务配置需要有type属性，指示该配置节点的种类。

#### 定位任务

定位任务指定位一个几何图形，返回值为定位得到的最匹配的图形的坐标或None。

#### 查找任务

查找任务指查找一个几何图形，返回值为定位得到的匹配的图形的数目。

#### 点击任务

点击任务

# xpip-mirror

如果您位于长城防火墙或其他受到限制的网络之内，官方源 [PyPI](https://pypi.org/) 可能无法访问，或者安装包的依赖较多时由于访问不稳定而安装失败。

`xpip-mirror` 镜像源管理提供了一个内置的镜像源列表，并且探测镜像源是否可达以及延迟，您随时可以切换镜像源至当前的最佳路径。

## 查看列表所有的镜像源

```text
root@zou:~# xpip-mirror list
name      URL                                       HOST                                       PING(ms)
--------  ----------------------------------------  -----------------------------------------  ----------
ustc      https://pypi.mirrors.ustc.edu.cn/simple   pypi.mirrors.ustc.edu.cn (218.104.71.170)  8.3
baidu     https://mirror.baidu.com/pypi/simple      mirror.baidu.com (58.243.203.35)           15.7
aliyun    https://mirrors.aliyun.com/pypi/simple    mirrors.aliyun.com (119.167.250.248)       17.7
tsinghua  https://pypi.tuna.tsinghua.edu.cn/simple  pypi.tuna.tsinghua.edu.cn (101.6.15.130)   23.7
douban    https://pypi.douban.com/simple            pypi.douban.com (49.233.242.15)            32.0
pypi      https://pypi.org/simple                   pypi.org (151.101.128.223)                 timeout

Suggest using the installation command:
pip install -i https://pypi.mirrors.ustc.edu.cn/simple <package-name>
```

## 镜像源配置

## 查看当前镜像源配置

```text
root@zou:~# xpip-mirror now
https://mirrors.aliyun.com/pypi/simple
```

### 自动选择镜像源

探测镜像源的延迟，自动选择最佳的镜像源，以获得更快的安装速度：

```text
root@zou:~# xpip-mirror choice
Writing to /root/.config/pip/pip.conf
choice ustc: https://pypi.mirrors.ustc.edu.cn/simple
```

### 切换指定镜像源

如果需要使用特定的镜像源安装包，也可指定切换的镜像源名称：

```text
root@zou:~# xpip-mirror choice tsinghua
Writing to /root/.config/pip/pip.conf
choice tsinghua: https://pypi.tuna.tsinghua.edu.cn/simple
```

# xpip-mirror

If you live within the Great Wall Firewall, the access to the official source of [PyPI](https://pypi.org/) is extremely unstable.

The `xpip-mirror` mirror management can probe the delay of mirrors in the list and select the current optimal path.

## list all available mirrors

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

## config mirror

### show config

```text
root@zou:~# xpip-mirror now
https://mirrors.aliyun.com/pypi/simple
```

### choice the best

```text
root@zou:~# xpip-mirror choice
Writing to /root/.config/pip/pip.conf
choice ustc: https://pypi.mirrors.ustc.edu.cn/simple
```

### choice by name

```text
root@zou:~# xpip-mirror choice tsinghua
Writing to /root/.config/pip/pip.conf
choice tsinghua: https://pypi.tuna.tsinghua.edu.cn/simple
```

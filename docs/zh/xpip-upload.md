# xpip-upload

`xpip-upload` 可方便的将构建的包上传至 [PyPI](https://pypi.org/) 仓库。

## 使用密码

```shell
root@zou:~# xpip-upload dist/*
```

## 使用 token

由于 PyPI 开始要求使用双因子认证（2FA），所以上传时推荐使用 [API tokens](https://pypi.org/help/#apitoken) 认证。

```shell
root@zou:~# xpip-upload dist/* --token <TOKEN>
```

## 使用配置文件

将密码或者 token 存储在本地的配置文件中，指定配置文件以避免每次输入用户名和密码。

**警告：密码或者 token 为敏感信息，请务必本地存储，妥善保管，谨防泄露，切勿上传至公共环境。**

可以通过 `--config-file` 选项来指定配置文件，未指定时 `~/.pypirc` （如果存在）作为默认配置文件。

```shell
root@zou:~# xpip-upload dist/* --config-file .pypirc
```

配置文件的示例：

```text
[distutils]
index-servers =
    repository1
    repository2

[repository1]
repository = https://upload.pypi.org/legacy/
token = <token>

[repository2]
repository = https://upload.pypi.org/legacy/
username = __token__
password = <token>
```

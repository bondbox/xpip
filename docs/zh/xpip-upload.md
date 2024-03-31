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

您还可以将密码或者 token 存储在配置文件中，以避免每次输入。

**警告：密码或者 token 为敏感信息，请本地存储，切勿保存于公共环境中。**

```shell
root@zou:~# xpip-upload dist/* --config-file .pypirc
```

默认配置文件为 `~/.pypirc`，您还可以用过 `--config-file` 选项来指定配置文件，示例如下：

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

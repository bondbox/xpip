# xpip

构建和安装 Python 包。

## 特性

- **通过 [xpip-build](xpip-build.md) 简单、快速的构建和安装 Python 包**
- **通过 [xpip-upload](xpip-upload.md) 上传至 PyPI 仓库**
- **通过 [xpip-mirror](xpip-mirror.md) 管理镜像源**

## Makefile

为您的项目创建以下 `makefile`，即可简单、快速的构建和上传 Python 包。

```Makefile
MAKEFLAGS += --always-make

all: build install


upgrade-xpip.build:
	pip3 install -i https://pypi.org/simple --upgrade xpip.build

upgrade-xpip.upload:
	pip3 install -i https://pypi.org/simple --upgrade xpip.upload

upgrade-xpip: upgrade-xpip.build upgrade-xpip.upload
	pip3 install -i https://pypi.org/simple --upgrade xpip.mirror


upload:
	xpip-upload --config-file .pypirc dist/*


build:
	xpip-build setup --clean --all


install:
	pip3 install --force-reinstall --no-deps dist/*.whl


uninstall:
	pip3 uninstall -y <package>
```

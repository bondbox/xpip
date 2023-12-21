依以下步骤发布到PyPI（https://pypi.org）：
1.修改元数据
    1a.修改源代码
    1b.文件“../xpip/__init__.py”（如有新增import对象）
    1c.文件“../setup.py”中的版本号
2.检查是否安装setuptools、wheel、twine等模块（python -m pip list）
    如果未安装或者需要升级，请依次执行以下命令：
        >>>python -m pip install --upgrade pip
        >>>python -m pip install --upgrade setuptools
        >>>python -m pip install --upgrade wheel
        >>>python -m pip install --upgrade twine
3.打包及上传，依次执行以下脚本文件：
    windows:
        ./windows/step1.pack.bat
        ./windows/step2.upload.bat
    linux:
        ./linux/step1.pack.sh
        ./linux/step2.upload.sh
4.安装、升级、卸载xpip模块
    可使用dist目录下的whl包进行本地测试
    安装xpip模块：
        >>>python -m pip install xpip
        >>>python -m pip list
    升级xpip模块
        >>>python -m pip install --upgrade xpip
        >>>python -m pip list
    卸载xpip模块
        >>>python -m pip uninstall xpip
        >>>python -m pip list
5.以下目录为打包时自动生成：
    ../build
    ../dist
    ../xpip.egg-info

# pip-qt
![PyPI - Version](https://img.shields.io/pypi/v/pip-qt)

pip qt widget to install new python modules from within your python environment.  

![image](https://github.com/hannesdelbeke/pip-qt/assets/3758308/272b56de-ada0-45f3-a813-75db8a749688)

Show the window:
```python
import pip_qt
widget = pip_qt.show()
```

## Gotchas
⚠️ WARNING, since this runs in Qt, you might get bugs when trying to (un)install or update the active Qt bindings.  
or any package that has a Qt binding as (indirect) dependency

## Dcc plugins
- <img src="https://raw.githubusercontent.com/tandpfun/skill-icons/59059d9d1a2c092696dc66e00931cc1181a4ce1f/icons/Blender-Dark.svg" width="20" style="max-width: 100%;"> Blender [pip qt addon](https://github.com/hannesdelbeke/pip-qt-addon)
- <img src="https://raw.githubusercontent.com/hannesdelbeke/gamedev-emojis/main/tools/emoji-maya.png" width="20" style="max-width: 100%;"> Maya [pip-qt-maya-plugin](https://github.com/hannesdelbeke/pip-qt-maya)  
- Unreal [pip-qt-unreal](https://github.com/hannesdelbeke/pip-qt-unreal) 

## Commands
- For advanced users, you can add options in the package name field, e.g. `--index-url http://my.package.repo/simple/ SomePackage` instead of `SomePackage`
- install auto adds `--target C:/target-path`, so don't add that, instead fill in the target field
- upgrade, type `--upgrade package-name` in the text field & click install
- editable install, type `-e C:/local-package-path` in the text field & click install

### 🔍 search packages on PyPI
- type `PackageName` in package field.
- click search

### ▶️ install a package
- type package name in package field
- click install

### ▶️ install a local package 
A local editable install speeds up your development.
Changes to your scripts in your IDE are automatically loaded in your app (after app restart or `importlib.reload`).
- type `-e path/to/packaged/repo` (ensure your local repo has a `pyproject.toml` or `setup.py`)
- click install

### 📃 list installed packages
See all installed packages, their versions, and location
- click the list button

# TODO
- [ ] ❌ uninstall
- [ ] 📃 list dependencies


### Dependencies
developed on Windows, Mac support in progress
- [py-pip](https://github.com/hannesdelbeke/py-pip)
- `pip-search` (optional, used for search, type `pip-search` and click install)
- qtpy



### Similar
let me know [here](https://github.com/hannesdelbeke/pip-qt/issues/new) if you find a similar project, and I'll link it below:
- DEAD https://github.com/open-cogsci/python-qtpip 3y old, outdated: uses pip search which is not supported anymore , unclear docs
- DEAD https://github.com/techbliss/Pip_QT_Gui 8 year old, PyQt4
- ARCHIVED https://github.com/NathanVaughn/PipQt 4year old, - PySide2, nice UI

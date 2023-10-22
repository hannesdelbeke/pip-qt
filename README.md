# pip-qt
pip qt widget to install new python modules from within your python environment.  

> ⚠️ WARNING, since this runs in Qt, you might get bugs when trying to (un)install or update the active Qt bindings.
> or any package that has a Qt binding as (indirect) dependency

![image](https://github.com/hannesdelbeke/pip-qt/assets/3758308/272b56de-ada0-45f3-a813-75db8a749688)


### Command reference
install auto adds `--target C:/target-path`, so don't add that, instead fill in the target field
- upgrade, type `--upgrade package-name` in the text field & click install
- editable install, type `-e C:/local-package-path` in the text field & click install

### dependencies
- [py-pip](https://github.com/hannesdelbeke/py-pip)
- `pip-search` (optional, used for search, type `pip-search` and click install)
- qtpy

<img src="https://raw.githubusercontent.com/tandpfun/skill-icons/59059d9d1a2c092696dc66e00931cc1181a4ce1f/icons/Blender-Dark.svg" width="32" style="max-width: 100%;"> if using Blender, check out the [pip qt addon](https://github.com/hannesdelbeke/pip-qt-addon)

### Similar
- https://github.com/open-cogsci/python-qtpip 3y old, uses pip search, outdated, unclear docs
- https://github.com/techbliss/Pip_QT_Gui 8 year old, PyQt4
- https://github.com/NathanVaughn/PipQt 4year old, - PySide2, nice UI

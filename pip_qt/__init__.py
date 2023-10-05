import sys
import subprocess
import pip_search
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from qtpy.QtWidgets import QTableWidget, QTableWidgetItem
from qtpy import QtGui
from qtpy.QtWidgets import QHeaderView
import importlib
import pkgutil
import os
import pkg_resources  # todo replace deprecated module


def run_command(command):
    # pass custom python paths, in case they were dynamically added
    my_env = os.environ.copy()
    joined_paths = os.pathsep.join(sys.path)
    env_var = my_env.get("PYTHONPATH")
    if env_var:
        joined_paths = f"{env_var}{os.pathsep}{joined_paths}"
    my_env["PYTHONPATH"] = joined_paths

    # Run the command and capture the output
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=my_env)
    output, error = process.communicate()
    return output, error


def list_packages():
    """return tuple of (name, version) for each installed package"""
    output, error = run_command([sys.executable, "-m", "pip", "list"])

    # Parse the output of the pip list command
    packages = []
    raw = output.decode()
    # [print(x) for x in raw.split("\n")]

    for line in raw.split("\n")[2:-1]:
        name, version = line.split()
        packages.append((name, version))
    return packages


def get_version(package_name) -> str:
    """Return installed package version or empty string"""
    packages = list_packages()
    for name, version in packages:
        if name == package_name:
            return version
    return ""


def get_location(package_name) -> str:
    output, error = run_command([sys.executable, "-m", "pip", "show", package_name])
    raw = output.decode()
    for line in raw.split("\n"):
        if line.startswith("Location:"):
            return line.split(" ")[1]
    return ""


def find_package_location(package_name):
    try:
        distribution = pkg_resources.get_distribution(package_name)
        return distribution.location
    except pkg_resources.DistributionNotFound:
        return f"Package '{package_name}' not found."


def get_location2(package_name) -> str:
    try:
        loader = pkgutil.get_loader(package_name)
        if loader is not None:
            package_location = os.path.dirname(loader.get_filename())
            return package_location
        else:
            loc = find_package_location(package_name)
            if loc:
                return loc
            else:
                return f"Package '{package_name}' not found."
    except ImportError:
        return f"Error while trying to locate package '{package_name}'."


class PipInstaller(QWidget):
    def __init__(self):
        super().__init__()

        # Create the UI elements
        self.package_label = QLabel("Package name:")
        self.package_input = QLineEdit()
        self.install_button = QPushButton("Install")
        self.list_button = QPushButton("List")
        self.search_button = QPushButton("Search")
        self.run_button = QPushButton("Custom cmd")

        # Create the output text box
        self.output_box = QTextEdit()
        self.output_box.setReadOnly(True)
        self.output_table = QTableWidget()
        self.output_table.setVisible(False)
        self.output_table.verticalHeader().setVisible(False)
        # self.output_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)  # auto resize
        self.output_table.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)  # reduce spacing
        self.output_table.horizontalHeader().setStretchLastSection(True)

        # Connect the buttons to their functions
        self.install_button.clicked.connect(self.install_package)
        self.list_button.clicked.connect(self.ui_list_packages)
        self.search_button.clicked.connect(self.search_packages)
        self.run_button.clicked.connect(self.run_command)

        # Create the layout
        package_layout = QHBoxLayout()
        package_layout.addWidget(self.package_label)
        package_layout.addWidget(self.package_input)
        package_layout.addWidget(self.install_button)
        package_layout.addWidget(self.list_button)
        package_layout.addWidget(self.search_button)
        package_layout.addWidget(self.run_button)

        main_layout = QVBoxLayout()
        main_layout.addLayout(package_layout)
        main_layout.addWidget(self.output_box)
        main_layout.addWidget(self.output_table)

        self.setLayout(main_layout)

    def install_package(self):
        package_name = self.package_input.text()
        command = [sys.executable, "-m", "pip", "install", package_name]
        self.run_command(command)
        importlib.invalidate_caches()  # todo add control


    def ui_list_packages(self):
        self.output_table.setVisible(True)
        self.output_box.setVisible(False)

        packages = list_packages()

        table = self.output_table
        table.setColumnCount(3)
        table.setHorizontalHeaderLabels(["Name", "Version", "Location"])
        table.setRowCount(len(packages))

        # Populate the table with the installed packages
        for i, (name, version) in enumerate(packages):
            name_item = QTableWidgetItem(name)
            version_item = QTableWidgetItem(version)
            table.setItem(i, 0, name_item)
            table.setItem(i, 1, version_item)
        table.repaint()

        self.repaint()
        QApplication.processEvents()

        # slow
        for i, (name, version) in enumerate(packages):
            location = get_location2(name)  # slo
            location_item = QTableWidgetItem(location)
            table.setItem(i, 2, location_item)
            self.repaint()

    def search_packages(self):
        self.output_table.setVisible(True)
        self.output_box.setVisible(False)

        # Get the search query from the user
        query = self.package_input.text()
        if not query:
            self.output_box.insertPlainText("Please enter a search query")

        # Search for packages on PyPI
        packages = list(pip_search.search(query))

        # Create the table w idget
        table = self.output_table
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Name", "Latest", "Installed",   "Released", "Description"])
        table.setRowCount(len(packages))
        # set scale last olumn to max
        # table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        table.setColumnWidth(0, 200)
        table.setColumnWidth(1, 70)
        table.setColumnWidth(2, 70)
        table.setColumnWidth(3, 100)

        # Populate the table with the search results
        for i, package in enumerate(packages):
            name_item = QTableWidgetItem(package.name)
            version_item = QTableWidgetItem(package.version)
            installed_version = get_version(package.name)
            installed_version_item = QTableWidgetItem(installed_version)
            released_item = QTableWidgetItem(package.released[:10])
            description_item = QTableWidgetItem(package.description)
            table.setItem(i, 0, name_item)
            table.setItem(i, 1, version_item)
            table.setItem(i, 2, installed_version_item)
            table.setItem(i, 3, released_item)
            table.setItem(i, 4, description_item)

            # make text green if installed version matches
            # todo, match with dark and light style
            if package.version == installed_version:
                installed_version_item.setBackground(QtGui.QColor(80, 200, 80))
            elif(installed_version):
                installed_version_item.setBackground(QtGui.QColor(200, 80, 80))

    def run_command(self, custom_command=None):
        # Get the command to run
        command = custom_command or self.package_input.text().split()

        output, error = run_command(command)

        self.output_table.setVisible(False)
        self.output_box.setVisible(True)

        # Display the output in the text box
        self.output_box.insertPlainText(output.decode())
        self.output_box.insertPlainText("\nERRORS =====================\n")
        self.output_box.insertPlainText(error.decode())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PipInstaller()
    window.show()
    sys.exit(app.exec_())

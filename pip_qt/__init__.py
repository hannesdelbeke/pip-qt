import sys
import pip_search
from qtpy.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QTextEdit
from qtpy.QtWidgets import QTableWidget, QTableWidgetItem
from qtpy import QtGui
from qtpy.QtWidgets import QHeaderView
import py_pip
from pathlib import Path


class PipInstaller(QWidget):
    # TODO option to set target path
    # provide preset for path in dcc like Blender, Unreal, ...
    # not all dcc have set path, e.g. Substance has no user path.

    def __init__(self):
        super().__init__()

        # create row at top with browse button and text edit field
        self.path_label = QLabel("Path:")
        self.path_input = QLineEdit(str(py_pip.default_target_path))
        self.path_button = QPushButton("Browse")
        self.path_button.clicked.connect(self.browse_path)
        self.path_layout = QHBoxLayout()
        self.path_layout.addWidget(self.path_label)
        self.path_layout.addWidget(self.path_input)
        self.path_layout.addWidget(self.path_button)

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
        self.install_button.clicked.connect(self.ui_install_package)
        # TODO uninstall
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
        main_layout.addLayout(self.path_layout)
        main_layout.addLayout(package_layout)
        main_layout.addWidget(self.output_box)
        main_layout.addWidget(self.output_table)

        self.setLayout(main_layout)

    def browse_path(self):
        path = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
        self.path_input.setText(path)

    def ui_install_package(self):
        package_name = self.package_input.text()
        py_pip.install(package_name, target_path=self.path_input.text())


    def ui_list_packages(self):
        self.output_table.setVisible(True)
        self.output_box.setVisible(False)

        packages = py_pip.list()

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
            location = str(Path(py_pip.get_location(name)))  # slo
            location_item = QTableWidgetItem(location)
            table.setItem(i, 2, location_item)
            self.repaint()

    def sort_by_column(self, column):
        self.output_table.sortItems(column)

    def search_packages(self):
        self.output_table.setVisible(True)
        self.output_box.setVisible(False)

        # Get the search query from the user
        query = self.package_input.text()
        if not query:
            self.output_box.insertPlainText("Please enter a search query")

        # Search for packages on PyPI
        packages = list(pip_search.search(query))

        # Create the table widget
        table = self.output_table
        table.setColumnCount(5)
        table.setHorizontalHeaderLabels(["Name", "Latest", "Installed",   "Released", "Description"])
        table.setRowCount(len(packages))

        table.horizontalHeader().sectionClicked.connect(self.sort_by_column)  # TODO sort by column

        # set scale last olumn to max
        # table.horizontalHeader().setSectionResizeMode(4, QHeaderView.Stretch)
        table.setColumnWidth(0, 200)
        table.setColumnWidth(1, 70)
        table.setColumnWidth(2, 70)
        table.setColumnWidth(3, 100)

        py_pip.list()  # create cache

        # Populate the table with the search results
        for i, package in enumerate(packages):
            name_item = QTableWidgetItem(package.name)
            version_item = QTableWidgetItem(package.version)
            installed_version = py_pip.get_version(package.name, cached=True)
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

        output, error = py_pip.run_command(command)

        self.output_table.setVisible(False)
        self.output_box.setVisible(True)

        # Display the output in the text box
        self.output_box.insertPlainText(output.decode())
        self.output_box.insertPlainText("\nERRORS =====================\n")
        self.output_box.insertPlainText(error.decode())


def show(dark=False):
    app = QApplication.instance()
    new_app = False
    if not app:
        new_app = True
        app = QApplication(sys.argv)

    if dark:
        import blender_stylesheet
        blender_stylesheet.setup()
    window = PipInstaller()
    window.show()

    if new_app:
        app.exec_()


if __name__ == "__main__":
    show()

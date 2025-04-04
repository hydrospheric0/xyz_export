import os
from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction
from .xyz_export_gui import XYZExportDialog

class XYZExport:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = os.path.dirname(__file__)
        self.action = None

    def initGui(self):
        icon_path = os.path.join(self.plugin_dir, 'icon.png')
        self.action = QAction(QIcon(icon_path), 'Export XYZ Tiles', self.iface.mainWindow())
        self.action.triggered.connect(self.run)
        self.iface.addPluginToMenu('&XYZ Export', self.action)
        self.iface.addToolBarIcon(self.action)

    def unload(self):
        if self.action:
            self.iface.removePluginMenu('&XYZ Export', self.action)
            self.iface.removeToolBarIcon(self.action)

    def run(self):
        dialog = XYZExportDialog(self.iface)
        dialog.exec_()

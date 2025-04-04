
import os
import re
from qgis.PyQt.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QPushButton, QLineEdit, QFileDialog,
    QComboBox, QListWidget, QListWidgetItem, QDialogButtonBox,
    QCheckBox, QMessageBox
)
from qgis.PyQt.QtCore import QSize, Qt
from qgis.core import (
    QgsProject, QgsRasterLayer, QgsRectangle, QgsMapSettings,
    QgsMapRendererCustomPainterJob, QgsApplication, QgsTask
)
from qgis.PyQt.QtGui import QImage, QPainter

class XYZExportDialog(QDialog):
    def __init__(self, iface):
        super().__init__()
        self.iface = iface
        self.setWindowTitle("Export XYZ Tiles")
        self.resize(500, 400)
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Output folder:"))
        self.folder_input = QLineEdit(os.path.expanduser('~/outputs'))
        browse_btn = QPushButton("Browse")
        browse_btn.clicked.connect(self.select_folder)
        layout.addWidget(self.folder_input)
        layout.addWidget(browse_btn)

        layout.addWidget(QLabel("Export resolution:"))
        self.res_combo = QComboBox()
        self.res_combo.addItems(["1920x1080 (2K)", "3840x2160 (4K)", "7680x4320 (8K)"])
        layout.addWidget(self.res_combo)

        layout.addWidget(QLabel("Select visible raster layers:"))
        self.layer_list = QListWidget()
        self.layer_map = {}

        root = QgsProject.instance().layerTreeRoot()
        for layer in QgsProject.instance().mapLayers().values():
            if isinstance(layer, QgsRasterLayer):
                node = root.findLayer(layer.id())
                if node and node.isVisible():
                    item = QListWidgetItem(layer.name())
                    item.setFlags(item.flags() | Qt.ItemIsUserCheckable)
                    item.setCheckState(Qt.Checked)
                    self.layer_list.addItem(item)
                    self.layer_map[layer.name()] = layer

        layout.addWidget(self.layer_list)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.folder_input.setText(folder)

    def accept(self):
        print("✅ [XYZExportDialog] OK clicked.")
        res_text = self.res_combo.currentText()
        config = {
            'folder': self.folder_input.text(),
            'resolution': res_text,
            'width': int(res_text.split('x')[0]),
            'height': int(res_text.split('x')[1].split()[0]),
            'layers': [self.layer_map[item.text()] for item in self.layer_list.findItems("*", Qt.MatchWildcard) if item.checkState() == Qt.Checked]
        }
        config['res_label'] = res_text.split('(')[-1].strip(')')

        print("🧮 Config:", config)
        print("🗂 Layers selected:", [l.name() for l in config['layers']])
        if not config['layers']:
            QMessageBox.warning(self, "No layers selected", "Please select at least one raster layer to export.")
            return

        task = RasterExportTask("Export Raster", self.iface, config)
        QgsApplication.taskManager().addTask(task)
        print("🚀 Task submitted to QGIS Task Manager.")
        self.close()

class RasterExportTask(QgsTask):
    def __init__(self, desc, iface, config):
        super().__init__(desc)
        self.iface = iface
        self.config = config

    def run(self):
        try:
            print("🔧 [RasterExportTask] Starting render...")
            c = self.config
            map_canvas = self.iface.mapCanvas()
            extent = map_canvas.extent()
            size = QSize(c['width'], c['height'])

            settings = QgsMapSettings()
            settings.setOutputSize(size)
            settings.setExtent(extent)
            settings.setLayers(c['layers'])

            for layer in c['layers']:
                img = QImage(c['width'], c['height'], QImage.Format_ARGB32_Premultiplied)
                dpi = int(300 * 39.37)  # 300 DPI
                img.setDotsPerMeterX(dpi)
                img.setDotsPerMeterY(dpi)
                painter = QPainter(img)

                job = QgsMapRendererCustomPainterJob(settings, painter)
                job.start()
                job.waitForFinished()
                painter.end()

                safe_name = re.sub(r'[^a-zA-Z0-9_]+', '_', layer.name())
                fname = os.path.join(c['folder'], f"{safe_name}_{c['res_label']}.png")

                base, ext = os.path.splitext(fname)
                counter = 1
                while os.path.exists(fname):
                    fname = f"{base}_{counter}{ext}"
                    counter += 1

                img.save(fname, "PNG")
                print(f"✅ Exported: {fname}")

            return True
        except Exception as e:
            print(f"❌ Export failed: {e}")
            return False

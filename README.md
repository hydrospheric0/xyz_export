# Screenshot Export Plugin for QGIS

**Screenshot Export** is a QGIS plugin developed by **Metolius Research** for exporting high-resolution screenshots of raster layers, including XYZ tiles and WMS sources. It's ideal for generating clean visuals for print, presentations, videos, or further analysis.

---

## Features

### Export Raster Layers to PNG
- Select visible **raster layers** (including XYZ tiles or WMS)
- Automatically uses current map canvas extent
- Supports standard output resolutions:
  - `1920×1080 (2K)`
  - `3840×2160 (4K)`
  - `7680×4320 (8K)`
- PNGs are saved at **300 DPI**

### 📁 Output Management
- Choose your own export folder
- Auto-generated filenames like:LayerName_2K.png LayerName_4K_1.png ← (auto-incremented if file exists)
- Safe overwrite handling

### 🗂 Layer Selection
- Only visible raster layers are listed
- Checkbox-based selection before export

### 🔧 Debugging and Transparency
- Prints export progress and file paths to the QGIS Python Console
- Logs:
- Active layer names
- Selected resolution
- Export folder
- Any rendering or save errors

---

## 🔧 Installation

1. [📦 Download the latest ZIP](https://github.com/hydrospheric0/xyz_export/blob/main/xyz_export_plugin.zip)
2. In QGIS, go to `Plugins → Manage and Install Plugins → Install from ZIP`.
3. Select the ZIP and install.
4. Access the plugin under `Plugins → Screenshot Export → Export XYZ Tiles`.

---

## 🧰 Requirements

- QGIS 3.x (Windows, macOS, or Linux)
- No external dependencies

---

## 📌 Roadmap

Planned features for future versions:

- [ ] MP4 animation generation (from time-series or stacked layers)
- [ ] Overlay options for date and credits
- [ ] AOI-based clipping and zoom control
- [ ] Custom DPI and resolution options

---

## ✉️ Contact

**Metolius Research**  
📧 metoliusresearch@gmail.com

---

## 📝 License

MIT License – free for personal and commercial use.

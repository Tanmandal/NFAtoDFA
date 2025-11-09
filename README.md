# NFA → DFA Converter & Visualizer

Convert any **NFA (or λ-NFA)** to a **DFA** and visualize it interactively using Python and PyWebView.

---

## 🚀 Features

* NFA → DFA conversion (with λ-support)
* Rich CLI interface
* Interactive DFA visualization in browser window
* Download DFA diagram as JPEG
* Built with **PyWebView**, **Rich**, and **Nuitka**

---

## ⚙️ Installation

```bash
git clone https://github.com/tanmandal/NFAtoDFA.git
cd NFAtoDFA
pip install -r requirements.txt
```

For **Windows**, you can also download the `.zip` from [Releases](https://github.com/Tanmandal/NFAtoDFA/releases) and extract it and run the .exe directly.

---

## 🧠 Usage

```bash
python NFAtoDFA.py
```

Follow the CLI prompts to enter:

* States and transitions
* Initial and final states
* (Optional) λ-transitions

Choose to visualize → opens DFA diagram window with download option.

---

## 🖼️ Screenshots

<table>
<tr>
<td><img src="https://github.com/Tanmandal/ScreenShots/blob/main/NFADFA2.png" width="300"></td>
<td><img src="https://github.com/Tanmandal/ScreenShots/blob/main/NFADFA1.png" width="300"></td>
</tr>
<tr>
<td colspan="2" align="center"><img src="https://github.com/Tanmandal/ScreenShots/blob/main/NFADFA3.png" width="500"></td>
</tr>
</table>

---

## 🆕 Updates

* Migrated from **Electron → PyWebView**
* Switched **PyInstaller → Nuitka**
* Improved CLI with **Rich**

---

## 📜 License

MIT License © 2024

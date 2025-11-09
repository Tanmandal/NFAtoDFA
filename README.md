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

## 🆕 Updates

* Migrated from **Electron → PyWebView**
* Switched **PyInstaller → Nuitka**
* Improved CLI with **Rich**

---

## 📜 License

MIT License © 2024

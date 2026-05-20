# UtilityHub: Modular System for Utility Tool Management
## Full Technical Report

> [!CAUTION]
> **Warning:** This project was conducted strictly for pedagogical purposes to study video streaming protocols, data extraction, and automation techniques. No copyrighted content was distributed or used beyond legal limits. All experiments were limited to publicly accessible data.

---

**Presented by:** Salimi Achraf  
**Academic Year:** 2025/2026  
**Institution:** University Ibn Tofaïl - Faculty of Sciences, Kenitra  
**Master:** Big Data, Artificial Intelligence, and Advanced Applications

---

## Acknowledgements
We wish to express our deep gratitude to everyone who contributed to the realization of the **UtilityHub** project. Our thanks go first to our module professor for proposing this stimulating project and for the valuable advice that guided our work throughout the development of this modular application.

We also thank the entire UIT faculty for the quality of their instruction and pedagogical support. Finally, we thank our colleagues and loved ones for their encouragement and moral support during the various phases of design and implementation.

---

## 1. Introduction
The **UtilityHub** project was born from a personal initiative to design a versatile "Multi-Utils" application capable of efficiently assisting with daily digital tasks. The project had a dual ambition: to explore the internal workings of common digital tools (such as conversion algorithms and media download protocols) and to intensively practice the simultaneous use of **PyQt5 (Desktop)** and **Flask (Web)** frameworks.

This report details the design approach, the technological solutions implemented, and the final assessment of this software engineering experience.

> [!TIP]
> **Desktop vs. Web Development Focus**
> Although the project features a hybrid architecture, the **Desktop (PyQt5)** application received the majority of development time. It is aesthetically superior and includes advanced features such as real-time task cancellation and sophisticated multithreading ergonomics that are not yet fully available in the Web version.

---

## 2. Project Objectives
The primary goal was to centralize four essential utilities into a single platform:
- **File Converter:** Transforming documents, images, and audio/video files.
- **Media Downloader:** Extracting media from multiple web sources (YouTube, etc.).
- **Notes Manager:** Quick text archiving and search system.
- **Todo List:** Task management with status tracking.

The project is built on several technological pillars:
1. **PyQt5:** For the powerful desktop software interface.
2. **Flask:** For the web-accessible interface.
3. **Pandas & CSV:** For lightweight and simple data management.
4. **Specialized Tools:** Integration of `yt-dlp`, `FFmpeg`, and `FileLock`.

---

## 3. General Architecture
UtilityHub follows a strict **layered architecture** to ensure separation of concerns between data, logic, and interfaces.

### 3.1. Architectural Layers
1. **Persistence Layer (Data):** Management of CSV files (`notes.csv`, `todos.csv`, `history.csv`) and configuration JSON.
2. **Core Layer:** Centralized managers (`CsvManager`, `SettingsManager`, `HistoryManager`) using **FileLock** as a safety bridge to guarantee data integrity between the Desktop and Web versions during concurrent writes.
3. **Navigation & Dashboard:** Centered around a main dashboard that manages all menus. Users can switch between tools seamlessly without closing or reloading the app, preserving current work states across tabs.
4. **Service Layer:** The core logic organized into independent service classes, shared between environments.
5. **Presentation Layer:** Divided into two distinct environments (Desktop PyQt5 and Web Flask).

### 3.2. Project Technical Tree
```text
utilityhub/
├── app.py                  # Web launcher (Flask)
├── desktop_app.py          # Desktop launcher (PyQt5)
├── assets/                 # UI Resources (Icons, etc.)
├── tools/                  
│   ├── ffmpeg.exe          # FFmpeg binary
│   └── node.exe            # Node binary
├── data/                   
│   ├── notes.csv
│   ├── todos.csv
│   ├── history.csv
│   ├── settings.json
│   ├── uploads/            # Temp storage
│   └── outputs/            # Generated files
├── core/                   # Application core managers
│   ├── csv_manager.py      
│   ├── history_manager.py  
│   └── settings_manager.py 
├── modules/                # Business logic modules
│   ├── converter/
│   ├── downloader/
│   ├── notes/
│   └── todo/
├── web/                    # Flask Interface (templates & static)
└── desktop/                # PyQt5 Interface (windows & main window)
```

---

## 4. Deep Dive into Implementation

### 4.1. Core Layer (Managers)
- **CsvManager:** Centralizes core I/O. Key methods: `load_csv()`, `save_csv()`, `lock()`, and `generate_id()`.
- **HistoryManager:** Tracks all user interactions. Key methods: `add_record()`, `get_history()`, `delete_record()`, and `clear_history()`.
- **SettingsManager:** Single entry point for application configuration via structured JSON. Key methods: `get_setting()`, `update_setting()`, and `get_all_settings()`.

### 4.2. Functional Modules & Services

#### 4.2.1. Media Converter (ConverterService)
Advanced transformations utilizing specialized libraries:
- **xhtml2pdf & Markdown:** `convert_md_to_pdf()` and `convert_txt_to_pdf()` with custom CSS styling.
- **Pillow (PIL):** `convert_to_jpg()` and `convert_to_png()` for image format and transparency management.
- **vtracer:** `convert_to_svg()` for high-performance bitmap vectorization.
- **FFmpeg:** `convert_mp4_to_mp3()` for high-quality audio extraction.

#### 4.2.2. Media Downloader (MediaDownloaderService)
Orchestrates `yt-dlp` for complex extraction:
- **`get_media_info()`:** Fetches metadata and available format IDs.
- **`download_media()`:** Execution via progress hooks for real-time tracking (speed, ETA, percentage).
- **`get_available_formats()`:** Filters raw formats for user selection.

#### 4.2.3. Productivity Tools (Notes & Todo)
- **Notes Service:** `save_note()`, `list_notes()`, `get_note_by_id()`, `search_notes()`, and `search_by_tag()`.
- **Todo Service:** `add_task()`, `delete_task()`, `change_status()`, `change_task()`, `get_tasks()`, and `search_tasks()`.

---

## 5. Technical Challenges & Engineering

### 5.1. Synchronization (FileLock)
Crucial for management between Desktop and Web. It creates a temporary `.lock` file to prevent data corruption during simultaneous writes to common CSV files.

### 5.2. Desktop (PyQt5) & Threading Model
Uses `QThread` and `pyqtSignal` to offload heavy tasks from the main UI thread, ensuring a non-blocking and fluid experience. The tools communicate progress (percentage, speed, ETA) via signals to update the UI in real-time.

### 5.3. Web (Flask) & Server-Sent Events (SSE)
- **Blueprints:** The web interface is structured into independent "Blueprints," functioning as modular applications working together for cleaner code maintenance.
- **SSE Tracking:** To overcome the limitation where websites wait for a task to finish before showing results, UtilityHub uses **Server-Sent Events**.
    - **Technical Details:** The server keeps a persistent HTTP connection open, streaming raw text data (`data: ...\n\n`) using the `text/event-stream` content type.
    - **Advantages:** Simpler than WebSockets, supports automatic reconnection, and is firewall-friendly as it uses standard HTTP ports. The client connects via the `EventSource` API for live DOM updates.

### 5.4. The GIL Challenge
The Python **Global Interpreter Lock (GIL)** presented a technical hurdle:
- **Downloader:** Primarily I/O-bound (internet wait), leaving the UI highly responsive.
- **Converter:** Being CPU-intensive, it can cause the UI to freeze even when using FFmpeg as an external process. While `asyncio` would have been the optimal solution for total fluidity, it was not integrated in this version due to time constraints.

---

## 6. Graphical Presentation
The application features a consistent **Dark Mode** design:
- **Desktop:** Custom tab navigation system and integrated terminal logging.
- **Web:** Responsive grid-based layout built with **Bootstrap**.

---

## 7. Conclusion
**UtilityHub** is a solid software engineering demonstration, proving that a modular architecture and shared services can create a powerful hybrid ecosystem. It represents a robust base, ready for future enhancements and additional modules.

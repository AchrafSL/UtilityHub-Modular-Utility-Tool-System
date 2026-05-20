# UtilityHub - Modular Utility Tool System

> [!CAUTION]
> **Warning:** This project was conducted strictly for pedagogical purposes to study video streaming protocols, data extraction, and automation techniques. No copyrighted content was distributed or used beyond legal limits. All experiments were limited to publicly accessible data.

---


UtilityHub is a comprehensive desktop and web-based application designed to centralize various utility tools into a single, modular ecosystem. Built with Python, it offers advanced features for media conversion, downloading, and productivity management through both a powerful PyQt5 desktop interface and a convenient Flask web dashboard.

---

## 🛠️ Key Features

- **Media Converter:** Convert documents (MD/TXT to PDF), images (JPG/PNG/SVG), and extract audio from video (MP4 to MP3). Optimized to delegate CPU-intensive tasks to external binaries (FFmpeg) to mitigate GIL limitations.
- **Media Downloader:** YouTube and streaming media extraction featuring **non-blocking background threads** and real-time progress tracking (percentage, speed, ETA).
- **Productivity Suite:** Integrated Notes and Todo list managers with advanced search, categorization, and cross-platform synchronization.
- **Hybrid Architecture:** A shared service layer using **FileLock** as a safety bridge to ensure data integrity between Desktop and Web interfaces accessing common CSV storage.

## 🚀 Getting Started

### Prerequisites

Ensure you have Python 3.10+ installed. Some modules require external binaries (FFmpeg) which are included in the `tools/` directory.

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd UtilityHub
   ```

2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

#### 1. Desktop Version (Recommended ⭐)
Launch the advanced PyQt5 interface. This version is the most complete, featuring superior aesthetics, real-time task cancellation, and a robust multithreading engine:
```bash
python desktop_app.py
```

#### 2. Web Version
Launch the Flask-based web dashboard. It utilizes **Blueprints** for modularity and **Server-Sent Events (SSE)** for live progress streaming:
```bash
python app.py
```

---

## 📄 Technical Documentation

For in-depth details on the architecture, technical logic, and implementation, please refer to our documentation:
- 🇺🇸 **[Full Project Technical Report (English - Markdown)](./eng%20version%20technical%20report/Project_Full_Report_EN.md)**
- 🇫🇷 [Technical Overview - 5-page Report (French)](./rapport%20technique%205pages/rapport%20technique%20utilityhub%20Achraf%20Salimi.md)
- 🇫🇷 [Detailed Full Project Report - 44-page PDF (French)](./full%20report%2044page/rapport%20python%20s1%20mini%20projet.pdf)

## 🧠 Technical Highlights

- **The GIL Challenge:** The project manages the Python Global Interpreter Lock by offloading heavy lifting (FFmpeg, yt-dlp) to external processes. While Downloader tasks (I/O) remain fluid, Converter tasks (CPU) hit the GIL; future updates aim for `asyncio` integration for total UI non-blocking behavior.
- **Real-time Synchronization:** Data integrity is maintained via a physical locking mechanism (`FileLock`), preventing race conditions when both Desktop and Web interfaces write to shared CSV files.
- **Web Streaming (SSE):** Unlike traditional polling, the Web interface uses `EventSource` (SSE) to maintain a persistent connection, allowing the server to "push" download progress data instantly.

## 🏗️ Project Structure
- `core/`: Data managers (CSV, History, Settings) with **FileLock** logic.
- `modules/`: Shared business logic services (Converter, Downloader) and modular Flask **Blueprints**.
- `desktop/`: Advanced PyQt5 windows with custom signal/slot threading.
- `web/`: Responsive Flask templates and SSE integration logic.
- `data/`: Centralized CSV persistence layer shared across platforms.
- `tools/`: Portable external binaries (FFmpeg, Node, vtracer).

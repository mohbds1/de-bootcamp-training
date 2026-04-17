# GitHub Trending Scraper API & Debian Package 🚀

This project is a complete "from script to system" solution. It demonstrates the full lifecycle of a software project: scraping web data, exposing it via a REST API, wrapping it as a background Linux service, and packaging it into an easily distributable Debian package (`.deb`).

## 🌟 Features
- **Web Scraping:** Extracts real-time trending repositories from GitHub using `BeautifulSoup4`.
- **REST API:** Serves the cleaned data over a network endpoint using `FastAPI` and `Uvicorn`.
- **System Service:** Runs continuously in the background on Ubuntu using `systemd` (automatic restart enabled).
- **Security:** Automatically configures the `ufw` firewall to open the required port (8000) during installation.
- **Automated Deployment:** Wrapped entirely in a `.deb` package with `postinst` and `prerm` scripts for a professional, zero-touch installation experience.

## 📁 Project Structure
The repository mimics the structure of an Ubuntu file system required for building the Debian package:
- `DEBIAN/`: Contains package metadata (`control`) and automation scripts (`postinst`, `prerm`).
- `opt/trending-api/`: The application's home, containing the core Python source code and virtual environment setup.
- `etc/systemd/system/`: Contains the unit file to manage the application as a system service.

## 🛠️ Installation
To deploy this system on any Ubuntu/Debian machine, simply download the `.deb` package and run:

```bash
sudo dpkg -i trending-app-package.deb
sudo apt-get install -f  # This ensures all dependencies (python3-venv, ufw) are installed
```

## 🌐 Usage
Once installed, the service starts automatically. You can verify the status and fetch data using the following commands:

### Check Service Status:
```bash
sudo systemctl status trending-api.service
```

### Fetch Trending Repos:
```bash
curl http://localhost:8000/trending
```

### Interactive Documentation:
Visit `http://localhost:8000/docs` in your browser to interact with the **Swagger UI** and explore the API endpoints.

## 📝 Development & Analysis
This project was designed with a focus on **separation of concerns**:
1. **Scraper Layer:** Handles raw HTML processing and data extraction.
2. **API Layer:** Handles network communication and JSON serialization.
3. **OS Layer:** Handles process management, security, and distribution.

---
*Created as part of a System Programming & Deployment assignment.*

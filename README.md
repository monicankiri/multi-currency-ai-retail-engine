# multi-currency-ai-retail-engine

# Multi-Currency AI Retail Engine (Project MCARE)

Project MCARE is an enterprise-grade backend ecosystem designed to eliminate operational bottlenecks for global e-commerce companies. The architecture autonomously tracks competitor inventories, neutralizes foreign exchange volatility at checkout, and uses artificial intelligence to accelerate catalog deployment.

## 🚀 Current Architecture Status

### Phase 1: Automated Data Intake Pipeline (Completed - Week 1 Milestone)
*   **Data Scraper Engine:** Built an object-oriented Python scraping engine using `Requests` and `BeautifulSoup` to autonomously fetch product structures from web targets without browser overhead.
*   **Sanitization Layer:** Integrated regex string-filtration to strip currency anomalies and parse pure mathematical values.
*   **Relational Data Model:** Created an automated database initialization engine using `SQLAlchemy` mapping distinct relational structures for Core Products and Historical Price Tracking.

---

## 🛠️ Tech Stack & Dependencies
*   **Language:** Python 3.10+
*   **Database ORM:** SQLAlchemy
*   **Database Engine:** SQLite (Local Development Baseline) / Ready for PostgreSQL migration
*   **Network & Parsing:** Requests, BeautifulSoup4

---

## 📂 Project Structure
```text
├── mcare_core.py       # Core application layer (Database configuration, Scraper Engine, and Pipeline Execution)
└── README.md           # Engineering documentation and architectural roadmap
```

## ⚙️ How to Run the Baseline Pipeline Local Setup

1. **Install Dependencies:**
   ```bash
   pip install sqlalchemy requests beautifulsoup4
   ```

2. **Execute Core Script:**
   ```bash
   python mcare_core.py
   ```

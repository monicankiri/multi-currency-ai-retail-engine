import os
import requests
from datetime import datetime
from bs4 import BeautifulSoup
from sqlalchemy import create_engine, Column, Integer, String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# ==========================================
# SECTION 1: THE DIGITAL NOTEBOOK (DATABASE STRUCTURE)
# ==========================================
# We tell Python to create a local database file named 'mcare_local.db' right here.
DATABASE_URL = "sqlite:///mcare_local.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    """Stores the items our business wants to sell."""
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    ai_optimized_title = Column(String, nullable=True) # Blank until Week 2 AI runs
    ai_marketing_description = Column(Text, nullable=True) # Blank until Week 2 AI runs
    base_price_usd = Column(Numeric(10, 2), nullable=False)
    competitor_url = Column(String, nullable=True)
    stock_count = Column(Integer, default=5)

    price_history = relationship("PriceHistory", back_populates="product", cascade="all, delete-orphan")

class PriceHistory(Base):
    """Tracks how competitor prices change over time."""
    __tablename__ = "price_history"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    observed_price_usd = Column(Numeric(10, 2), nullable=False)
    scraped_at = Column(DateTime, default=datetime.utcnow)

    product = relationship("Product", back_populates="price_history")


# ==========================================
# SECTION 2: THE INVISIBLE EMPLOYEE (THE BOT ENGINE)
# ==========================================
class RetailBot:
    """Simulates a browser, connects to web pages, and extracts data."""
    def __init__(self):
        # We wear a mask (User-Agent) so the server thinks we are Google Chrome, not a script
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    def scrape_product(self, url: str) -> dict:
        """Downloads the page HTML and pulls out the title and price containers."""
        try:
            print(f"📡 Step 1: Sending request across the internet to sandbox...")
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            # Turn the raw HTML text string into a structured, searchable object
            soup = BeautifulSoup(response.text, "html.parser")
            
            # Look for the specific HTML elements on the book testing site
            title_element = soup.find("h1")
            price_element = soup.find("p", {"class": "price_color"})
            
            # If found, grab the inside text; if missing, use placeholders
            raw_title = title_element.text.strip() if title_element else "Unknown Item"
            raw_price = price_element.text.strip() if price_element else "£0.00"
            
            print("📥 Step 2: HTML data downloaded and parsed cleanly!")
            return {"title": raw_title, "price_string": raw_price}
            
        except Exception as e:
            print(f"❌ Network/Parsing failure occurred: {e}")
            return None


# ==========================================
# SECTION 3: THE PIPELINE EXECUTION (RUNNING THE ENGINE)
# ==========================================
def main():
    print("🚀 --- STARTING MCARE CORE PIPELINE --- 🚀")
    
    # 1. Initialize the physical database tables on your computer hard drive
    print("🗄️ Initializing database tables...")
    Base.metadata.create_all(bind=engine)
    
    # 2. Boot up our worker bot
    bot = RetailBot()
    target_link = "http://toscrape.com"
    
    # 3. Tell the bot to go scrape the target page
    scraped_info = bot.scrape_product(target_link)
    
    if scraped_info:
        # CLEANING DATA: The price text looks like '£51.77'. 
        # A database cannot save currency symbols, so we filter out only numbers and decimals.
        price_str = scraped_info["price_string"]
        clean_numeric_str = "".join(char for char in price_str if char.isdigit() or char == '.')
        final_price = float(clean_numeric_str) if clean_numeric_str else 0.0
        
        print(f"🎯 Cleaned Scraped Data -> Title: '{scraped_info['title']}' | Price: ${final_price}")
        
        # 4. Save the records into our database using a data session
        print("💾 Committing records to local database file...")
        db_session = SessionLocal()
        try:
            # Create a row instance for the products table
            db_product = Product(
                title=scraped_info["title"],
                base_price_usd=final_price,
                competitor_url=target_link
            )
            db_session.add(db_product)
            db_session.flush() # Forces database to generate an ID for this product
            
            # Create a linked row instance for the historical tracking price table
            db_history = PriceHistory(
                product_id=db_product.id,
                observed_price_usd=final_price
            )
            db_session.add(db_history)
            
            db_session.commit()
            print("🏆 SUCCESS! Data perfectly captured and written to disk.")
            
        except Exception as database_error:
            db_session.rollback()
            print(f"❌ Transaction aborted due to database issue: {database_error}")
        finally:
            db_session.close() # Clean up memory allocations
            
    print("🏁 --- PIPELINE EXECUTION FINISHED --- 🏁")

if __name__ == "__main__":
    main()

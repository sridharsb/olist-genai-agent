#!/usr/bin/env python
"""Setup verification script for Olist GenAI Agent"""

import os
import sys
import duckdb

def check_database():
    """Check if database exists and has required views"""
    db_path = "db/olist.db"
    
    if not os.path.exists(db_path):
        print("[ERROR] Database not found. Run: python db/setup_db.py")
        return False
    
    try:
        con = duckdb.connect(db_path)
        
        # Check for required views
        required_views = [
            "v_order_facts",
            "v_category_revenue",
            "v_category_units_sold",
            "v_category_aov",
            "v_monthly_revenue",
            "v_yearly_revenue"
        ]
        
        existing_views = con.execute(
            "SELECT table_name FROM information_schema.tables WHERE table_type = 'VIEW'"
        ).fetchall()
        
        existing_view_names = [v[0] for v in existing_views]
        
        missing_views = [v for v in required_views if v not in existing_view_names]
        
        if missing_views:
            print(f"[WARNING] Missing views: {missing_views}")
            print("   Run: python db/setup_db.py")
            con.close()
            return False
        
        print(f"[OK] Database setup complete ({len(existing_view_names)} views found)")
        con.close()
        return True
        
    except Exception as e:
        print(f"[ERROR] Database error: {e}")
        return False

def check_dependencies():
    """Check if required packages are installed"""
    # Map package names to import names
    required = {
        "streamlit": "streamlit",
        "duckdb": "duckdb",
        "pandas": "pandas",
        "matplotlib": "matplotlib",
        "python-dateutil": "dateutil",
        "openai": "openai"
    }
    missing = []
    
    for pkg_name, import_name in required.items():
        try:
            __import__(import_name)
        except ImportError:
            missing.append(pkg_name)
    
    if missing:
        print(f"[ERROR] Missing packages: {missing}")
        print("   Run: pip install -r requirements.txt")
        return False
    
    print("[OK] All dependencies installed")
    return True

def check_data_files():
    """Check if data files exist"""
    data_dir = "data"
    required_files = [
        "olist_orders_dataset.csv",
        "olist_order_items_dataset.csv",
        "olist_products_dataset.csv",
        "olist_order_payments_dataset.csv"
    ]
    
    missing = []
    for f in required_files:
        if not os.path.exists(os.path.join(data_dir, f)):
            missing.append(f)
    
    if missing:
        print(f"[WARNING] Missing data files: {missing}")
        return False
    
    print("[OK] Data files found")
    return True

def main():
    print("Checking Olist GenAI Agent setup...\n")
    
    deps_ok = check_dependencies()
    data_ok = check_data_files()
    db_ok = check_database()
    
    print("\n" + "="*50)
    if deps_ok and data_ok and db_ok:
        print("[OK] Setup complete! Run: streamlit run streamlit_app.py")
        return 0
    else:
        print("[ERROR] Setup incomplete. Please fix the issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())


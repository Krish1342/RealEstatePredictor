"""
Simple launcher script for the Real Estate Predictor Streamlit app
"""

import streamlit as st
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    # Import the main app
    from app import main
    
    if __name__ == "__main__":
        main()
        
except ImportError as e:
    st.error(f"Error importing main application: {e}")
    st.info("Please ensure all required packages are installed. Run: pip install -r requirements.txt")
except Exception as e:
    st.error(f"Error running application: {e}")
    st.info("Please check the error message above and ensure all data files are in place.")
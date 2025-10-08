"""
Professional Real Estate Price Predictor - Launch Script
Run this script to start the Streamlit application
"""

import subprocess
import sys
import os


def check_requirements():
    """Check if required packages are installed"""
    required_packages = [
        "streamlit",
        "pandas",
        "numpy",
        "plotly",
        "scikit-learn",
        "joblib",
        "requests",
    ]

    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ Missing packages: {', '.join(missing_packages)}")
        print("Please install them using: pip install -r enhanced_requirements.txt")
        return False

    print("✅ All required packages are installed!")
    return True


def main():
    """Main launcher function"""
    print("🏠 Real Estate AI Predictor - Professional Edition")
    print("=" * 50)

    # Check requirements
    if not check_requirements():
        return

    # Check if model files exist
    model_dir = "ensemble_learning/saved_models"
    if not os.path.exists(model_dir):
        print(f"⚠️ Model directory not found: {model_dir}")
        print("Please ensure the models are in the correct location.")

    # Launch Streamlit app
    print("🚀 Launching Professional Real Estate Predictor...")
    print("📱 The app will open in your default web browser")
    print("🔗 URL: http://localhost:8501")
    print("-" * 50)
    print("💡 To get weather data, sign up for a free API key at:")
    print("   https://openweathermap.org/api")
    print("-" * 50)

    try:
        subprocess.run(
            [
                sys.executable,
                "-m",
                "streamlit",
                "run",
                "professional_app.py",
                "--server.port",
                "8501",
                "--server.address",
                "localhost",
                "--theme.base",
                "light",
            ]
        )
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except Exception as e:
        print(f"❌ Error launching application: {e}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
Real Estate Predictor FastAPI Backend Launcher
"""

import sys
import os
import subprocess
import uvicorn


def check_dependencies():
    """Check if required dependencies are installed"""
    # Map package names to their import names
    required_packages = {
        "fastapi": "fastapi",
        "uvicorn": "uvicorn",
        "pandas": "pandas",
        "numpy": "numpy",
        "scikit-learn": "sklearn",  # scikit-learn imports as sklearn
        "joblib": "joblib",
        "pydantic": "pydantic",
    }

    # Optional packages (don't fail if missing)
    optional_packages = {
        "xgboost": "xgboost",
        "lightgbm": "lightgbm",
    }

    missing_packages = []
    for package_name, import_name in required_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_packages.append(package_name)

    # Check optional packages and warn if missing
    missing_optional = []
    for package_name, import_name in optional_packages.items():
        try:
            __import__(import_name)
        except ImportError:
            missing_optional.append(package_name)

    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("📦 Please install them with: pip install -r requirements.txt")
        return False

    if missing_optional:
        print(f"⚠️ Optional packages missing: {', '.join(missing_optional)}")
        print("💡 Some ML models may not work without these packages")

    print("✅ All required dependencies are installed")
    return True


def check_models():
    """Check if model files exist"""
    model_dir = "../ensemble_learning/saved_models"
    required_files = [
        "best_model_extra_trees.pkl",
        "model_3_random_forest.pkl",
        "model_4_decision_tree.pkl",
        "model_5_lightgbm.pkl",
        "model_1_extra_trees.pkl",
        "feature_scaler.pkl",
        "ensemble_learning_results.csv",
        "feature_importance.csv",
    ]

    missing_files = []
    for file in required_files:
        if not os.path.exists(os.path.join(model_dir, file)):
            missing_files.append(file)

    if missing_files:
        print(f"⚠️ Missing model files: {', '.join(missing_files)}")
        print(f"📁 Please ensure all model files are in: {model_dir}")
        return False

    print("✅ All model files found")
    return True


def main():
    """Main function to start the FastAPI server"""
    print("🚀 Real Estate Predictor FastAPI Backend")
    print("=" * 50)

    # Check dependencies
    if not check_dependencies():
        sys.exit(1)

    # Check model files
    if not check_models():
        print("⚠️ Some model files are missing, but starting server anyway...")

    print("\n🔧 Starting FastAPI server...")
    print("📡 Server will be available at: http://localhost:8000")
    print("📊 API documentation at: http://localhost:8000/docs")
    print("🔍 Health check at: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server\n")

    try:
        # Start the FastAPI server
        uvicorn.run(
            "simple_fastapi_app:app",
            host="0.0.0.0",
            port=8000,
            reload=True,
            log_level="info",
        )
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

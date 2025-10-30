#!/usr/bin/env python3
"""Test the /predict endpoint with various scenarios"""

import requests
import json

BASE_URL = "http://localhost:8000"

# Test data - complete property
test_property = {
    "BHK": 3,
    "Size_in_SqFt": 1500,
    "Year_Built": 2018,
    "Floor_No": 5,
    "Total_Floors": 12,
    "Nearby_Schools": 3,
    "Nearby_Hospitals": 2,
    "Furnished_Status": "Semi-Furnished",
    "Public_Transport_Accessibility": "Good",
    "Parking_Space": "Yes",
    "Security": "Yes",
    "Availability_Status": "Ready to Move",
    "Baths": 2,
    "balcony": "Yes",
    "location": "Koramangala",
    "Property_Type": "Apartment",
    "Facing": "East",
    "Owner_Type": "Primary"
}

def test_health():
    """Test health endpoint"""
    print("\n" + "="*60)
    print("Testing /health endpoint...")
    print("="*60)
    r = requests.get(f"{BASE_URL}/health")
    print(f"Status: {r.status_code}")
    print(json.dumps(r.json(), indent=2))
    return r.status_code == 200

def test_models():
    """Test models endpoint"""
    print("\n" + "="*60)
    print("Testing /models endpoint...")
    print("="*60)
    r = requests.get(f"{BASE_URL}/models")
    print(f"Status: {r.status_code}")
    data = r.json()
    print(f"Total models loaded: {data['total_models']}")
    for model in data['models']:
        print(f"  - {model['name']}: weight={model['weight']}, R2={model['metrics']['R2']}")
    return r.status_code == 200

def test_predict():
    """Test predict endpoint"""
    print("\n" + "="*60)
    print("Testing /predict endpoint...")
    print("="*60)
    print("Input:")
    print(json.dumps(test_property, indent=2))
    
    r = requests.post(f"{BASE_URL}/predict", json=test_property)
    print(f"\nStatus: {r.status_code}")
    
    if r.status_code == 200:
        data = r.json()
        print(f"\n✅ SUCCESS!")
        print(f"Predicted Price: {data['formatted_price']}")
        print(f"Confidence: {data['confidence']}")
        print(f"Models used: {len(data['individual_predictions'])}")
        
        print("\nIndividual Model Predictions:")
        for pred in data['individual_predictions']:
            print(f"  - {pred['name']}: {pred['formatted_price']} (weight: {pred['weight']}%)")
        
        print(f"\nPrediction Range:")
        print(f"  Min: {data['prediction_range']['formatted_min']}")
        print(f"  Max: {data['prediction_range']['formatted_max']}")
        
        print(f"\nTop 5 Important Features:")
        for feat in data['feature_importance'][:5]:
            print(f"  - {feat['feature']}: {feat['importance']:.4f}")
        
        return True
    else:
        print(f"\n❌ FAILED!")
        print(r.text)
        return False

if __name__ == "__main__":
    print("\n🏡 Real Estate Predictor API - Test Suite")
    print("="*60)
    
    # Run tests
    health_ok = test_health()
    models_ok = test_models()
    predict_ok = test_predict()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print(f"Health Check: {'✅ PASS' if health_ok else '❌ FAIL'}")
    print(f"Models Info:  {'✅ PASS' if models_ok else '❌ FAIL'}")
    print(f"Prediction:   {'✅ PASS' if predict_ok else '❌ FAIL'}")
    print("="*60)
    
    if health_ok and models_ok and predict_ok:
        print("\n🎉 All tests passed! API is working correctly.")
    else:
        print("\n⚠️  Some tests failed. Check the output above.")

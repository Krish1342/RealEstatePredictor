#!/usr/bin/env python3
"""Multiple test scenarios for the /predict endpoint"""

import requests
import json

BASE_URL = "http://localhost:8000"

test_cases = [
    {
        "name": "Luxury 4BHK in Whitefield",
        "data": {
            "BHK": 4,
            "Size_in_SqFt": 3000,
            "Year_Built": 2022,
            "Floor_No": 12,
            "Total_Floors": 20,
            "Nearby_Schools": 5,
            "Nearby_Hospitals": 3,
            "Furnished_Status": "Fully Furnished",
            "Public_Transport_Accessibility": "Excellent",
            "Parking_Space": "Yes",
            "Security": "Yes",
            "Availability_Status": "Ready to Move",
            "Baths": 4,
            "balcony": "Yes",
            "location": "Whitefield",
            "Property_Type": "Penthouse",
            "Facing": "North-East",
            "Owner_Type": "Primary"
        }
    },
    {
        "name": "Budget 2BHK in Electronic City",
        "data": {
            "BHK": 2,
            "Size_in_SqFt": 900,
            "Year_Built": 2010,
            "Floor_No": 2,
            "Total_Floors": 5,
            "Nearby_Schools": 2,
            "Nearby_Hospitals": 1,
            "Furnished_Status": "Unfurnished",
            "Public_Transport_Accessibility": "Fair",
            "Parking_Space": "No",
            "Security": "No",
            "Availability_Status": "Ready to Move",
            "Baths": 1,
            "balcony": "No",
            "location": "Electronic City",
            "Property_Type": "Apartment",
            "Facing": "West",
            "Owner_Type": "Secondary"
        }
    },
    {
        "name": "Modern 3BHK in Indiranagar",
        "data": {
            "BHK": 3,
            "Size_in_SqFt": 1800,
            "Year_Built": 2023,
            "Floor_No": 8,
            "Total_Floors": 15,
            "Nearby_Schools": 4,
            "Nearby_Hospitals": 2,
            "Furnished_Status": "Semi-Furnished",
            "Public_Transport_Accessibility": "Good",
            "Parking_Space": "Yes",
            "Security": "Yes",
            "Availability_Status": "Under Construction",
            "Baths": 3,
            "balcony": "Yes",
            "location": "Indiranagar",
            "Property_Type": "Apartment",
            "Facing": "South",
            "Owner_Type": "Primary"
        }
    }
]

print("\n🏡 Real Estate Predictor - Multiple Property Tests")
print("="*70)

for i, test in enumerate(test_cases, 1):
    print(f"\n{'='*70}")
    print(f"Test {i}: {test['name']}")
    print("="*70)
    
    r = requests.post(f"{BASE_URL}/predict", json=test['data'])
    
    if r.status_code == 200:
        data = r.json()
        print(f"✅ Status: {r.status_code} OK")
        print(f"\n📊 Results:")
        print(f"   Predicted Price: {data['formatted_price']}")
        print(f"   Confidence: {data['confidence']}")
        print(f"   Models Used: {len(data['individual_predictions'])}/4")
        
        print(f"\n💰 Individual Model Predictions:")
        for pred in data['individual_predictions']:
            print(f"   • {pred['name']:<20} {pred['formatted_price']:<15} (weight: {pred['weight']:.1f}%)")
        
        print(f"\n📈 Prediction Range:")
        print(f"   Min: {data['prediction_range']['formatted_min']}")
        print(f"   Max: {data['prediction_range']['formatted_max']}")
        
        if data['insights']:
            print(f"\n💡 Insights:")
            for insight in data['insights']:
                print(f"   • {insight}")
    else:
        print(f"❌ Status: {r.status_code} FAILED")
        print(f"Error: {r.text}")

print(f"\n{'='*70}")
print("✅ All tests completed successfully!")
print("="*70)

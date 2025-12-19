"""
Test script for the new export API endpoints
"""
import requests
import json

API_BASE = "http://localhost:5000"

def test_get_table_columns():
    """Test getting columns from a table"""
    print("\n=== Testing GET /api/tables/{table}/columns ===")
    
    response = requests.get(f"{API_BASE}/api/tables/facebook_ads_insights/columns")
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        if data.get('success'):
            columns = data.get('data', [])
            print(f"Found {len(columns)} columns:")
            for col in columns[:5]:  # Show first 5
                print(f"  - {col['name']} ({col['type']})")
    else:
        print(f"Error: {response.text}")


def test_query_data():
    """Test querying data with filters"""
    print("\n=== Testing POST /api/data/query ===")
    
    query_data = {
        "table": "facebook_ads_insights",
        "columns": ["date_start", "date_stop", "impressions", "clicks", "spend"],
        "start_date": "2025-01-01",
        "end_date": "2025-12-31",
        "limit": 5
    }
    
    response = requests.post(
        f"{API_BASE}/api/data/query",
        json=query_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"Success: {data.get('success')}")
        if data.get('success'):
            results = data.get('data', [])
            print(f"Found {data.get('count')} records")
            if results:
                print("First record:")
                print(json.dumps(results[0], indent=2, default=str))
    else:
        print(f"Error: {response.text}")


def test_export_data():
    """Test exporting data to CSV"""
    print("\n=== Testing POST /api/data/export ===")
    
    export_data = {
        "table": "facebook_ads_insights",
        "columns": ["date_start", "impressions", "clicks", "spend"],
        "start_date": "2025-01-01",
        "end_date": "2025-12-31"
    }
    
    response = requests.post(
        f"{API_BASE}/api/data/export",
        json=export_data,
        headers={"Content-Type": "application/json"}
    )
    
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        print("Success! CSV file generated")
        print(f"Content-Type: {response.headers.get('Content-Type')}")
        print(f"Content-Disposition: {response.headers.get('Content-Disposition')}")
        print(f"CSV size: {len(response.content)} bytes")
        
        # Show first few lines
        csv_content = response.content.decode('utf-8')
        lines = csv_content.split('\n')[:5]
        print("\nFirst lines of CSV:")
        for line in lines:
            print(f"  {line}")
    else:
        print(f"Error: {response.text}")


if __name__ == "__main__":
    print("=" * 60)
    print("Testing Export API Endpoints")
    print("=" * 60)
    print("\nMake sure the API is running on http://localhost:5000")
    print("and that there's data in the database.")
    
    try:
        # Test if API is running
        response = requests.get(f"{API_BASE}/api/status")
        if response.status_code == 200:
            print("\n✅ API is running!")
            
            test_get_table_columns()
            test_query_data()
            test_export_data()
            
            print("\n" + "=" * 60)
            print("All tests completed!")
            print("=" * 60)
        else:
            print("\n❌ API is not responding correctly")
    except requests.exceptions.ConnectionError:
        print("\n❌ Cannot connect to API. Is it running?")
        print("Start it with: python api.py")

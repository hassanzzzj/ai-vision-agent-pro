"""
Simple API Tests
Backend API ko test karne ke liye
"""
import requests
import time
import sys

API_BASE = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🏥 Testing health endpoint...")
    try:
        response = requests.get(f"{API_BASE}/api/v1/health")
        assert response.status_code == 200
        print("✅ Health check passed")
        return True
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False

def test_root():
    """Test root endpoint"""
    print("\n🏠 Testing root endpoint...")
    try:
        response = requests.get(f"{API_BASE}/")
        assert response.status_code == 200
        data = response.json()
        print(f"✅ Root endpoint: {data.get('name')}")
        return True
    except Exception as e:
        print(f"❌ Root endpoint failed: {e}")
        return False

def test_generate(prompt="A cute robot in a library"):
    """Test image generation endpoint"""
    print(f"\n🎨 Testing generation with prompt: '{prompt}'")
    try:
        response = requests.post(
            f"{API_BASE}/api/v1/generate",
            json={
                "prompt": prompt,
                "max_iterations": 1
            }
        )
        
        if response.status_code != 200:
            print(f"❌ Generate failed with status {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        data = response.json()
        task_id = data.get("task_id")
        print(f"✅ Generation started - Task ID: {task_id}")
        
        # Poll for completion
        print("⏳ Waiting for generation to complete...")
        max_wait = 120  # 2 minutes
        start_time = time.time()
        
        while time.time() - start_time < max_wait:
            status_response = requests.get(f"{API_BASE}/api/v1/status/{task_id}")
            status_data = status_response.json()
            
            status = status_data.get("status")
            progress = status_data.get("progress", 0)
            
            print(f"   Status: {status} - Progress: {progress}%", end='\r')
            
            if status == "completed":
                print("\n✅ Generation completed successfully!")
                if status_data.get("generated_image"):
                    print("✅ Image data received")
                return True
            elif status == "failed":
                error = status_data.get("error", "Unknown error")
                print(f"\n❌ Generation failed: {error}")
                return False
            
            time.sleep(2)
        
        print(f"\n⚠️ Generation timed out after {max_wait}s")
        return False
        
    except Exception as e:
        print(f"❌ Generation test failed: {e}")
        return False

def run_all_tests():
    """Run all tests"""
    print("="*50)
    print("🧪 Running API Tests")
    print("="*50)
    
    results = []
    
    # Basic tests
    results.append(("Health Check", test_health()))
    results.append(("Root Endpoint", test_root()))
    
    # Generation test (only if API key is configured)
    print("\n⚠️ Note: Generation test requires SILICONFLOW_API_KEY")
    run_gen = input("Run generation test? (y/n): ").lower() == 'y'
    
    if run_gen:
        results.append(("Image Generation", test_generate()))
    
    # Summary
    print("\n" + "="*50)
    print("📊 Test Summary")
    print("="*50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    
    return passed == total

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)

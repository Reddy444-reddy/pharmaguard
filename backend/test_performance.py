import requests
import json
import time
import concurrent.futures
from datetime import datetime

BASE_URL = "http://127.0.0.1:5000"
VCF_PATH = "test_sample.vcf"

class PerformanceTester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.results = {
            "timestamp": datetime.now().isoformat(),
            "tests": []
        }
    
    def test_health_endpoint(self):
        """Test health check endpoint"""
        print("\n[TEST 1] Health Check Endpoint")
        start = time.time()
        
        try:
            response = requests.get(f"{self.base_url}/health")
            elapsed = time.time() - start
            
            result = {
                "test": "Health Check",
                "status": "PASS" if response.status_code == 200 else "FAIL",
                "status_code": response.status_code,
                "response_time_ms": round(elapsed * 1000, 2),
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"  Status: {response.status_code}")
            print(f"  Response Time: {result['response_time_ms']}ms")
            print(f"  Payload: {response.json()}")
            
            self.results["tests"].append(result)
            return result
        
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            self.results["tests"].append({
                "test": "Health Check",
                "status": "ERROR",
                "error": str(e)
            })
            return None
    
    def test_valid_vcf_analysis(self):
        """Test successful VCF analysis"""
        print("\n[TEST 2] Valid VCF Analysis")
        start = time.time()
        
        try:
            with open(VCF_PATH, 'rb') as f:
                files = {'vcf_file': f}
                data = {
                    'patient_id': 'PATIENT_001',
                    'drug': 'CODEINE'
                }
                
                response = requests.post(
                    f"{self.base_url}/analyze",
                    files=files,
                    data=data
                )
            
            elapsed = time.time() - start
            
            result = {
                "test": "Valid VCF Analysis",
                "status": "PASS" if response.status_code == 200 else "FAIL",
                "status_code": response.status_code,
                "response_time_ms": round(elapsed * 1000, 2),
                "timestamp": datetime.now().isoformat()
            }
            
            if response.status_code == 200:
                resp_json = response.json()
                result["risk_label"] = resp_json.get("risk_assessment", {}).get("risk_label")
                result["phenotype"] = resp_json.get("pharmacogenomic_profile", {}).get("phenotype")
                print(f"  Status: {response.status_code}")
                print(f"  Response Time: {result['response_time_ms']}ms")
                print(f"  Risk Label: {result['risk_label']}")
                print(f"  Phenotype: {result['phenotype']}")
            
            self.results["tests"].append(result)
            return result
        
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            self.results["tests"].append({
                "test": "Valid VCF Analysis",
                "status": "ERROR",
                "error": str(e)
            })
            return None
    
    def test_missing_patient_id(self):
        """Test missing patient_id validation"""
        print("\n[TEST 3] Missing Patient ID (Validation)")
        start = time.time()
        
        try:
            with open(VCF_PATH, 'rb') as f:
                files = {'vcf_file': f}
                data = {'drug': 'CODEINE'}  # Missing patient_id
                
                response = requests.post(
                    f"{self.base_url}/analyze",
                    files=files,
                    data=data
                )
            
            elapsed = time.time() - start
            
            result = {
                "test": "Missing Patient ID",
                "status": "PASS" if response.status_code == 400 else "FAIL",
                "status_code": response.status_code,
                "response_time_ms": round(elapsed * 1000, 2),
                "expected": 400,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"  Status: {response.status_code} (Expected: 400)")
            print(f"  Response Time: {result['response_time_ms']}ms")
            print(f"  Error: {response.json().get('error')}")
            
            self.results["tests"].append(result)
            return result
        
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            return None
    
    def test_invalid_drug(self):
        """Test invalid drug validation"""
        print("\n[TEST 4] Invalid Drug (Validation)")
        start = time.time()
        
        try:
            with open(VCF_PATH, 'rb') as f:
                files = {'vcf_file': f}
                data = {
                    'patient_id': 'PATIENT_002',
                    'drug': 'INVALIDRUG'  # Not in whitelist
                }
                
                response = requests.post(
                    f"{self.base_url}/analyze",
                    files=files,
                    data=data
                )
            
            elapsed = time.time() - start
            
            result = {
                "test": "Invalid Drug",
                "status": "PASS" if response.status_code == 400 else "FAIL",
                "status_code": response.status_code,
                "response_time_ms": round(elapsed * 1000, 2),
                "expected": 400,
                "timestamp": datetime.now().isoformat()
            }
            
            print(f"  Status: {response.status_code} (Expected: 400)")
            print(f"  Response Time: {result['response_time_ms']}ms")
            
            self.results["tests"].append(result)
            return result
        
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            return None
    
    def test_concurrent_requests(self, num_requests=5):
        """Test concurrent request handling"""
        print(f"\n[TEST 5] Concurrent Requests ({num_requests} requests)")
        
        def make_request(req_num):
            start = time.time()
            try:
                with open(VCF_PATH, 'rb') as f:
                    files = {'vcf_file': f}
                    data = {
                        'patient_id': f'PATIENT_CONCURRENT_{req_num}',
                        'drug': 'CODEINE'
                    }
                    
                    response = requests.post(
                        f"{self.base_url}/analyze",
                        files=files,
                        data=data
                    )
                
                elapsed = time.time() - start
                return {
                    "request_num": req_num,
                    "status_code": response.status_code,
                    "response_time_ms": round(elapsed * 1000, 2),
                    "success": response.status_code == 200
                }
            
            except Exception as e:
                return {
                    "request_num": req_num,
                    "error": str(e),
                    "success": False
                }
        
        start_total = time.time()
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(make_request, i) for i in range(num_requests)]
            concurrent_results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        total_time = time.time() - start_total
        successful = sum(1 for r in concurrent_results if r.get("success"))
        
        result = {
            "test": "Concurrent Requests",
            "num_requests": num_requests,
            "successful": successful,
            "failed": num_requests - successful,
            "total_time_ms": round(total_time * 1000, 2),
            "avg_response_time_ms": round(sum(r.get("response_time_ms", 0) for r in concurrent_results) / num_requests, 2),
            "timestamp": datetime.now().isoformat()
        }
        
        print(f"  Total Requests: {num_requests}")
        print(f"  Successful: {successful}")
        print(f"  Failed: {num_requests - successful}")
        print(f"  Total Time: {result['total_time_ms']}ms")
        print(f"  Avg Response Time: {result['avg_response_time_ms']}ms")
        
        self.results["tests"].append(result)
        return result
    
    def generate_report(self):
        """Generate performance report"""
        print("\n" + "="*60)
        print("PERFORMANCE TEST REPORT")
        print("="*60)
        
        report = {
            "timestamp": self.results["timestamp"],
            "summary": {
                "total_tests": len(self.results["tests"]),
                "passed": sum(1 for t in self.results["tests"] if t.get("status") == "PASS"),
                "failed": sum(1 for t in self.results["tests"] if t.get("status") == "FAIL"),
                "errors": sum(1 for t in self.results["tests"] if t.get("status") == "ERROR")
            },
            "details": self.results["tests"]
        }
        
        print(f"\nTests Run: {report['summary']['total_tests']}")
        print(f"Passed: {report['summary']['passed']}")
        print(f"Failed: {report['summary']['failed']}")
        print(f"Errors: {report['summary']['errors']}")
        
        print("\n" + "="*60)
        print("PERFORMANCE METRICS")
        print("="*60)
        
        response_times = [t.get("response_time_ms") for t in self.results["tests"] if t.get("response_time_ms")]
        if response_times:
            print(f"\nAverage Response Time: {sum(response_times) / len(response_times):.2f}ms")
            print(f"Min Response Time: {min(response_times):.2f}ms")
            print(f"Max Response Time: {max(response_times):.2f}ms")
        
        print("\n" + "="*60)
        
        return report


if __name__ == "__main__":
    print("🧪 Starting PharmGuard Backend Performance Tests...\n")
    
    tester = PerformanceTester(BASE_URL)
    
    # Run all tests
    tester.test_health_endpoint()
    tester.test_valid_vcf_analysis()
    tester.test_missing_patient_id()
    tester.test_invalid_drug()
    tester.test_concurrent_requests(5)
    
    # Generate report
    report = tester.generate_report()
    
    # Save report to file
    with open("performance_report.json", "w") as f:
        json.dump(report, f, indent=2)
    
    print("\n✅ Performance report saved to: performance_report.json")

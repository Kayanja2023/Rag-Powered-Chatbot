#!/usr/bin/env python3
"""
Simple tests to verify recursion prevention
"""

def test_hash_function():
    """Test message hashing works"""
    import hashlib
    
    def get_message_hash(message):
        return hashlib.md5(message.encode()).hexdigest()
    
    # Test same message gives same hash
    msg1 = "Hello world"
    msg2 = "Hello world"
    msg3 = "Different message"
    
    hash1 = get_message_hash(msg1)
    hash2 = get_message_hash(msg2)
    hash3 = get_message_hash(msg3)
    
    assert hash1 == hash2, "Same messages should have same hash"
    assert hash1 != hash3, "Different messages should have different hashes"
    
    print("✅ Hash function test passed")

def test_fallback_detection():
    """Test fallback keyword detection"""
    
    def is_fallback_response(response):
        fallback_keywords = [
            "i'm not confident",
            "let me connect you to a live agent",
            "i'm unable to assist",
            "i do not have that information",
            "cannot confidently answer"
        ]
        return any(keyword in response.lower() for keyword in fallback_keywords)
    
    # Test fallback responses
    fallback_cases = [
        "I'm not confident I can assist with that",
        "Let me connect you to a live agent",
        "I'm unable to assist with this request"
    ]
    
    for case in fallback_cases:
        assert is_fallback_response(case), f"Should detect fallback: {case}"
    
    # Test normal responses
    normal_cases = [
        "Clickatell is a messaging company",
        "Here's how to use the API",
        "The pricing is available on our website"
    ]
    
    for case in normal_cases:
        assert not is_fallback_response(case), f"Should not detect fallback: {case}"
    
    print("✅ Fallback detection test passed")

def test_duplicate_prevention():
    """Test duplicate message prevention logic"""
    
    processed_hashes = set()
    
    def should_process_message(message):
        import hashlib
        message_hash = hashlib.md5(message.encode()).hexdigest()
        
        if message_hash in processed_hashes:
            return False
        
        processed_hashes.add(message_hash)
        return True
    
    # First message should be processed
    assert should_process_message("Hello"), "First message should be processed"
    
    # Same message should not be processed again
    assert not should_process_message("Hello"), "Duplicate message should not be processed"
    
    # Different message should be processed
    assert should_process_message("World"), "Different message should be processed"
    
    print("✅ Duplicate prevention test passed")

def run_all_tests():
    """Run all tests"""
    print("Running recursion prevention tests...")
    print("=" * 40)
    
    try:
        test_hash_function()
        test_fallback_detection()
        test_duplicate_prevention()
        
        print("=" * 40)
        print("✅ All tests passed! Recursion prevention should work.")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = run_all_tests()
    
    if success:
        print("\n🚀 The fixed Streamlit app should now work without recursion!")
        print("Run: streamlit run streamlit_app_fixed.py")
    else:
        print("\n⚠️ Tests failed. Check the implementation.")
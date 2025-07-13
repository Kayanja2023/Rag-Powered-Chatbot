#!/usr/bin/env python3
"""
Tests to ensure no recursion in the Streamlit app
"""

import unittest
from unittest.mock import Mock, patch
import sys
import os

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

class MockSessionState:
    """Mock Streamlit session state"""
    def __init__(self):
        self.messages = []
        self.processed_hashes = set()
        self.pending_handover = False
        self.processing = False
        self.session_id = "test-session"
        self.qa_chain = Mock()

class TestRecursionPrevention(unittest.TestCase):
    """Test cases to ensure no recursive behavior"""
    
    def setUp(self):
        """Set up test environment"""
        self.session_state = MockSessionState()
        
        # Mock the QA chain response
        self.session_state.qa_chain.invoke.return_value = "Test response"
    
    def test_duplicate_message_prevention(self):
        """Test that duplicate messages are not processed"""
        from streamlit_app_fixed import get_message_hash, process_message
        
        # Mock session state
        with patch('streamlit_app_fixed.st') as mock_st:
            mock_st.session_state = self.session_state
            
            # Process same message twice
            message = "Hello world"
            process_message(message)
            initial_count = len(self.session_state.messages)
            
            # Try to process same message again
            process_message(message)
            final_count = len(self.session_state.messages)
            
            # Should not increase message count
            self.assertEqual(initial_count, final_count, "Duplicate message was processed")
    
    def test_concurrent_processing_prevention(self):
        """Test that concurrent processing is prevented"""
        from streamlit_app_fixed import process_message
        
        with patch('streamlit_app_fixed.st') as mock_st:
            mock_st.session_state = self.session_state
            
            # Set processing flag
            self.session_state.processing = True
            
            # Try to process message while already processing
            initial_count = len(self.session_state.messages)
            process_message("Test message")
            final_count = len(self.session_state.messages)
            
            # Should not process message
            self.assertEqual(initial_count, final_count, "Message processed during concurrent processing")
    
    def test_fallback_state_management(self):
        """Test that fallback state is properly managed"""
        from streamlit_app_fixed import process_message, is_fallback_response
        
        with patch('streamlit_app_fixed.st') as mock_st:
            mock_st.session_state = self.session_state
            
            # Mock fallback response
            self.session_state.qa_chain.invoke.return_value = "I'm not confident I can assist with that"
            
            # Process message that triggers fallback
            process_message("Unknown question")
            
            # Should set pending_handover flag
            self.assertTrue(self.session_state.pending_handover, "Fallback did not set pending_handover")
            
            # Process "yes" response
            process_message("yes")
            
            # Should clear pending_handover flag
            self.assertFalse(self.session_state.pending_handover, "Handover flag not cleared after yes response")
    
    def test_fallback_detection(self):
        """Test fallback keyword detection"""
        from streamlit_app_fixed import is_fallback_response
        
        # Test fallback responses
        fallback_responses = [
            "I'm not confident I can assist with that",
            "Let me connect you to a live agent",
            "I'm unable to assist",
            "I do not have that information"
        ]
        
        for response in fallback_responses:
            self.assertTrue(is_fallback_response(response), f"Failed to detect fallback: {response}")
        
        # Test normal responses
        normal_responses = [
            "Clickatell is a messaging company",
            "Here's how to use the API",
            "The pricing is available on our website"
        ]
        
        for response in normal_responses:
            self.assertFalse(is_fallback_response(response), f"False positive fallback: {response}")
    
    def test_hash_uniqueness(self):
        """Test that message hashes are unique"""
        from streamlit_app_fixed import get_message_hash
        
        messages = [
            "Hello world",
            "Hello world!",
            "hello world",
            "Different message"
        ]
        
        hashes = [get_message_hash(msg) for msg in messages]
        
        # All hashes should be different (except exact duplicates)
        self.assertEqual(hashes[0], get_message_hash("Hello world"), "Same message should have same hash")
        self.assertNotEqual(hashes[0], hashes[1], "Different messages should have different hashes")
        self.assertNotEqual(hashes[0], hashes[2], "Case differences should create different hashes")
    
    def test_processing_flag_cleanup(self):
        """Test that processing flag is properly cleaned up"""
        from streamlit_app_fixed import process_message
        
        with patch('streamlit_app_fixed.st') as mock_st:
            mock_st.session_state = self.session_state
            
            # Process normal message
            process_message("Test message")
            
            # Processing flag should be cleared
            self.assertFalse(self.session_state.processing, "Processing flag not cleared after normal processing")
            
            # Test with exception
            self.session_state.qa_chain.invoke.side_effect = Exception("Test error")
            
            process_message("Error message")
            
            # Processing flag should still be cleared
            self.assertFalse(self.session_state.processing, "Processing flag not cleared after exception")

class TestIntegration(unittest.TestCase):
    """Integration tests for complete flow"""
    
    def test_complete_conversation_flow(self):
        """Test a complete conversation without recursion"""
        session_state = MockSessionState()
        
        with patch('streamlit_app_fixed.st') as mock_st:
            mock_st.session_state = session_state
            
            from streamlit_app_fixed import process_message
            
            # Normal conversation
            session_state.qa_chain.invoke.return_value = "Clickatell is a messaging company"
            process_message("What is Clickatell?")
            
            self.assertEqual(len(session_state.messages), 2)  # User + Bot
            self.assertFalse(session_state.pending_handover)
            
            # Fallback trigger
            session_state.qa_chain.invoke.return_value = "I'm not confident I can assist"
            process_message("Unknown question")
            
            self.assertEqual(len(session_state.messages), 4)  # Previous + User + Bot
            self.assertTrue(session_state.pending_handover)
            
            # User says no to live agent
            process_message("no")
            
            self.assertEqual(len(session_state.messages), 6)  # Previous + User + Bot
            self.assertFalse(session_state.pending_handover)

def run_tests():
    """Run all tests"""
    print("Running recursion prevention tests...")
    print("=" * 50)
    
    # Create test suite
    suite = unittest.TestSuite()
    
    # Add test cases
    suite.addTest(unittest.makeSuite(TestRecursionPrevention))
    suite.addTest(unittest.makeSuite(TestIntegration))
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "=" * 50)
    if result.wasSuccessful():
        print("✅ All tests passed! No recursion issues detected.")
    else:
        print("❌ Some tests failed. Recursion issues may exist.")
        print(f"Failures: {len(result.failures)}")
        print(f"Errors: {len(result.errors)}")
    
    return result.wasSuccessful()

if __name__ == "__main__":
    success = run_tests()
    sys.exit(0 if success else 1)
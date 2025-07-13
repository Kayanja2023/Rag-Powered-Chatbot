#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from legacy.retrieval_chain import build_retrieval_chain

def test_chain():
    print("Building retrieval chain...")
    try:
        chain = build_retrieval_chain()
        print("✅ Chain built successfully")
        
        print("\nTesting with a simple question...")
        response = chain.invoke(
            {"input": "What is Clickatell's mission?"},
            config={"configurable": {"session_id": "test-session"}}
        )
        
        print(f"✅ Response received: {response}")
        print(f"Response type: {type(response)}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_chain()
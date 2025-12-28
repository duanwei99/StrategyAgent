import sys
import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from backend.agent.nodes import perform_web_search, web_search_node


def test_direct_search():
    print("\n=== Testing Direct Search Function (perform_web_search) ===")
    query = "freqtrade rsi strategy best practices"
    print(f"Query: {query}")
    
    result = perform_web_search(query)
    print("\nResult:")
    print("-" * 30)
    print(result[:500] + "..." if len(result) > 500 else result)
    print("-" * 30)

def test_search_node():
    print("\n=== Testing Search Node (web_search_node) ===")
    
    # Mock state
    # web_search_node expects: user_requirement, iteration_count, has_strategy
    state = {
        "user_requirement": "RSI and MACD strategy",
        "iteration_count": 0,
        "has_strategy": False
    }
    
    print(f"Input State: {state}")
    
    try:
        result_dict = web_search_node(state)
        
        print("\nNode Output:")
        print("-" * 30)
        if "search_results" in result_dict:
            content = result_dict["search_results"]
            print(content[:500] + "..." if len(content) > 500 else content)
        else:
            print("No 'search_results' in output (might be skipped due to logic).")
            print(result_dict)
        print("-" * 30)
    except Exception as e:
        print(f"Error running node: {e}")

if __name__ == "__main__":
    test_direct_search()
    test_search_node()


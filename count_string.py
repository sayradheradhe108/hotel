import os
import requests
import sys

def count_occurrences(url, search_string, threshold):
    try:
        response = requests.get(url, timeout=15)
        response.raise_for_status()
        
        # Count occurrences
        count = response.text.count(search_string)
        
        print(f"URL: {url}")
        print(f"Searching for: '{search_string}'")
        print(f"Total Occurrences: {count}")
        print(f"Threshold: {threshold}")
        
        # Determine status
        is_below = count < threshold
        
        # Write to GitHub Step Summary
        summary_file = os.getenv('GITHUB_STEP_SUMMARY')
        if summary_file:
            with open(summary_file, 'a') as f:
                status_icon = "❌ ALERT" if is_below else "✅ OK"
                f.write(f"## {status_icon} Search Results\n")
                f.write(f"- **URL**: {url}\n")
                f.write(f"- **String**: `{search_string}`\n")
                f.write(f"- **Count Found**: `{count}`\n")
                f.write(f"- **Required Threshold**: `{threshold}`\n")
                if is_below:
                    f.write(f"\n> [!] Warning: Count is below threshold of {threshold}!\n")

        # Output the result for the shell script to pick up
        # We print a specific string that we can catch in the YAML
        if is_below:
            print("STATUS=FAIL")
            # Exit with 0 so the script finishes, but the YAML will handle the fail
        else:
            print("STATUS=SUCCESS")
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    target_url = os.getenv('TARGET_URL')
    search_str = os.getenv('SEARCH_STRING')
    limit = int(os.getenv('THRESHOLD', 1))
    
    if not target_url or not search_str:
        print("Missing environment variables.")
        sys.exit(1)
        
    count_occurrences(target_url, search_str, limit)

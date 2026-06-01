import os
import requests

def fetch_and_save_playlist():
    # GitHub Secret থেকে API URL নেওয়া হচ্ছে
    api_url = os.environ.get("TAPMAD_API_URL")
    
    if not api_url:
        print("Error: TAPMAD_API_URL secret is not set!")
        return

    try:
        print("Fetching data from API...")
        response = requests.get(api_url, timeout=30)
        
        # যদি রিকোয়েস্ট সফল হয় (Status Code 200)
        if response.status_code == 200:
            playlist_content = response.text
            
            # Tapmad.m3u নামে ফাইলটি সেভ করা হচ্ছে
            file_name = "Tapmad.m3u"
            with open(file_name, "w", encoding="utf-8") as file:
                file.write(playlist_content)
                
            print(f"Success: Playlist saved as {file_name}")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    fetch_and_save_playlist()

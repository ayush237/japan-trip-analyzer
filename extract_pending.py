import json
from bs4 import BeautifulSoup

def extract_pending():
    file_path = "travel_spots.html"
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    pending_spots = []
    
    # We iterate over details-row
    details_rows = soup.find_all('tr', class_='details-row')
    
    for details_row in details_rows:
        text_content = details_row.get_text()
        if "Deep research pending" in text_content:
            row_id = details_row.get('id')
            
            # Find the corresponding main row (it should be the row immediately preceding it, or we can find it by looking for onclick="toggleDetails('row_id')")
            # Wait, BeautifulSoup's find_previous_sibling is perfect.
            main_row = details_row.find_previous_sibling('tr', class_='main-row')
            if main_row:
                tds = main_row.find_all('td')
                if len(tds) >= 2:
                    spot_name = tds[0].get_text(strip=True)
                    location = tds[1].get_text(strip=True)
                    pending_spots.append({
                        "row_id": row_id,
                        "spot_name": spot_name,
                        "location": location
                    })

    print(f"Extracted {len(pending_spots)} pending spots.")
    with open("pending_spots.json", "w", encoding="utf-8") as f:
        json.dump(pending_spots, f, indent=2, ensure_ascii=False)

if __name__ == "__main__":
    extract_pending()

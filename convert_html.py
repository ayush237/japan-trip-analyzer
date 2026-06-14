import sys
from bs4 import BeautifulSoup

def convert_html(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    tbody = soup.find('tbody')
    if not tbody:
        print("No tbody found.")
        return

    # Find all direct child <tr> of tbody that are not already main-row or details-row
    rows = tbody.find_all('tr', recursive=False)
    
    new_rows = []
    
    for idx, row in enumerate(rows):
        if 'main-row' in row.get('class', []) or 'details-row' in row.get('class', []):
            new_rows.append(row)
            continue
            
        row_id = f"row-{idx}"
        
        # Add class and onclick to the main row
        row['class'] = row.get('class', []) + ['main-row']
        row['onclick'] = f"toggleDetails('{row_id}')"
        
        # Ensure all columns have correct classes or styling if needed.
        # But we don't need to change td contents.
        new_rows.append(row)
        
        # Create details row
        details_tr = soup.new_tag('tr')
        details_tr['id'] = row_id
        details_tr['class'] = 'details-row hidden'
        
        td = soup.new_tag('td')
        td['colspan'] = '8' # Wait, there are 8 columns: Spot Name, Location, Description, Booking, Distance, Timing, Highlights, Original Reel Link
        
        div = soup.new_tag('div')
        div['class'] = 'expanded-card'
        
        h4 = soup.new_tag('h4')
        h4.string = 'Deep Dive'
        div.append(h4)
        
        p_facts = soup.new_tag('p')
        p_facts_strong = soup.new_tag('strong')
        p_facts_strong.string = 'Facts: '
        p_facts.append(p_facts_strong)
        p_facts.append("Deep research pending. Run agent again to unlock fascinating facts.")
        div.append(p_facts)
        
        p_notes = soup.new_tag('p')
        p_notes_strong = soup.new_tag('strong')
        p_notes_strong.string = 'Special Notes: '
        p_notes.append(p_notes_strong)
        p_notes.append("Deep research pending. Run agent again to unlock special notes.")
        div.append(p_notes)
        
        p_links = soup.new_tag('p')
        p_links_strong = soup.new_tag('strong')
        p_links_strong.string = 'Reference Links: '
        p_links.append(p_links_strong)
        p_links.append("Deep research pending.")
        div.append(p_links)
        
        td.append(div)
        details_tr.append(td)
        
        new_rows.append(details_tr)
        
    # Replace contents of tbody
    tbody.clear()
    for row in new_rows:
        tbody.append(row)
        # Adding a newline for readability
        tbody.append("\n")

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print("HTML converted successfully.")

if __name__ == "__main__":
    convert_html("travel_spots.html")

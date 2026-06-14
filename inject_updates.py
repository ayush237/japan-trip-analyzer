import json
from bs4 import BeautifulSoup
import sys

def inject_updates():
    try:
        with open('backfill_results.json', 'r', encoding='utf-8') as f:
            updates = json.load(f)
    except FileNotFoundError:
        print("No backfill_results.json found.")
        sys.exit(1)

    html_file = 'travel_spots.html'
    with open(html_file, 'r', encoding='utf-8') as f:
        soup = BeautifulSoup(f, 'html.parser')

    for item in updates:
        row_id = item.get('row_id')
        details_row = soup.find('tr', id=row_id)
        if not details_row:
            print(f"Could not find row {row_id}")
            continue
            
        expanded_card = details_row.find('div', class_='expanded-card')
        if not expanded_card:
            continue
            
        ps = expanded_card.find_all('p')
        if len(ps) >= 3:
            # Facts
            ps[0].clear()
            s1 = soup.new_tag('strong')
            s1.string = "Facts: "
            ps[0].append(s1)
            f_facts = item.get('fascinating_facts', 'N/A')
            if isinstance(f_facts, list):
                f_facts = " ".join(f_facts)
            ps[0].append(f_facts)
            
            # Notes
            ps[1].clear()
            s2 = soup.new_tag('strong')
            s2.string = "Special Notes: "
            ps[1].append(s2)
            s_notes = item.get('special_notes', 'N/A')
            if isinstance(s_notes, list):
                s_notes = " ".join(s_notes)
            ps[1].append(s_notes)
            
            # Links
            ps[2].clear()
            s3 = soup.new_tag('strong')
            s3.string = "Reference Links: "
            ps[2].append(s3)
            r_links = item.get('reference_links', '#')
            if isinstance(r_links, list):
                if len(r_links) > 0:
                    r_links = r_links[0]
                else:
                    r_links = '#'
            a_tag = soup.new_tag('a', href=r_links, target='_blank')
            a_tag.string = "Official Link / More Info"
            ps[2].append(a_tag)

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(str(soup))
    print(f"Injected {len(updates)} updates into {html_file}.")

if __name__ == "__main__":
    inject_updates()

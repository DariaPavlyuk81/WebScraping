#1Web Scraping Program
#Uses Selenium - scraper launches browsers, navigates pages and collects data. The raw data is saved as CSV. And 
#Avoids duplication

import pandas as pd
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException

def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    return webdriver.Chrome(options=chrome_options)

def get_year_links(driver):
    print("Fetching year links...")
    driver.get("https://www.baseball-almanac.com/yearmenu.shtml")
    year_elements = driver.find_elements(By.CSS_SELECTOR, "a[href^='yearly/yr']")
    print(f"Found {len(year_elements)} year links")
    return [(el.text, el.get_attribute("href")) for el in year_elements if el.text.strip().isdigit()]

def extract_events(driver, year):
    events = {'year': year, 'season_highlights': '', 'world_series': '', 'all_star_game': ''}
    
    # Season highlights
    highlight_selectors = [
        "//h2[contains(., 'Season Highlights')]/following-sibling::p[1]",
        "//h2[contains(., 'Season Summary')]/following-sibling::p[1]",
        "//h2[contains(., 'Season')]/following-sibling::p[1]",
        "//p[contains(., 'The season')]",
        "//p[contains(., 'In') and contains(., 'the')]"
    ]
    
    for selector in highlight_selectors:
        try:
            events['season_highlights'] = driver.find_element(By.XPATH, selector).text.replace('\n', ' ').strip()
            break
        except NoSuchElementException:
            continue
    
    # World Series
    ws_selectors = [
        "//h2[contains(., 'World Series')]/following-sibling::p[1]",
        "//h2[contains(., 'Championship')]/following-sibling::p[1]",
        "//p[contains(., 'champions')]"
    ]
    for selector in ws_selectors:
        try:
            events['world_series'] = driver.find_element(By.XPATH, selector).text.replace('\n', ' ').strip()
            break
        except NoSuchElementException:
            continue
    
    # All-Star Game
    if int(year) >= 1933:
        asg_selectors = [
            "//h2[contains(., 'All Star Game')]/following-sibling::p[1]",
            "//p[contains(., 'All-Star Game')]"
        ]
        for selector in asg_selectors:
            try:
                events['all_star_game'] = driver.find_element(By.XPATH, selector).text
                break
            except NoSuchElementException:
                continue
    
    return events

def extract_stats(driver, year):
    stats = []
    # More comprehensive table selection
    tables = driver.find_elements(By.CSS_SELECTOR, "table[cellspacing='0'], table[border='1'], table[width='100%'], table")
    
    for table_idx, table in enumerate(tables):
        try:
            rows = table.find_elements(By.TAG_NAME, "tr")
            if len(rows) < 2:
                continue
                
            # Determine if this is a stats table
            is_stats_table = False
            header_text = ""
            
            # Check first few rows for stats headers
            for row in rows[:3]:
                try:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    if len(cells) >= 4:
                        header_text = ' '.join([cell.text.strip().lower() for cell in cells])
                        if ('player' in header_text or 'name' in header_text) and ('team' in header_text or 'value' in header_text):
                            is_stats_table = True
                            break
                except StaleElementReferenceException:
                    continue
            
            if not is_stats_table:
                continue
                
            # Determine category from surrounding elements
            category = ""
            try:
                # Look at preceding elements for category
                prev_elements = driver.find_elements(By.XPATH, f"//table[{table_idx+1}]/preceding-sibling::*[position() <= 3]")
                for elem in prev_elements:
                    text = elem.text.strip()
                    if text and any(x in text.lower() for x in ['batting', 'pitching', 'fielding', 'leaders']):
                        category = text
                        break
            except:
                pass
            
            # Process data rows
            for row in rows:
                try:
                    cols = row.find_elements(By.TAG_NAME, "td")
                    if len(cols) >= 4:
                        # Skip header rows
                        if any(x in cols[0].text.strip().lower() for x in ['rank', 'player', 'name']):
                            continue
                            
                        # Skip empty rows
                        if not cols[0].text.strip() and not cols[1].text.strip():
                            continue
                            
                        stats.append({
                            'year': year,
                            'category': category,
                            'rank': cols[0].text.strip(),
                            'player': cols[1].text.strip(),
                            'team': cols[2].text.strip(),
                            'value': cols[3].text.strip()
                        })
                except Exception as e:
                    continue
                    
        except Exception as e:
            continue
    
    print(f"Extracted {len(stats)} stats for {year}")
    return stats

def main():
    driver = setup_driver()
    year_links = get_year_links(driver)
    
    all_data = []
    all_events = []
    all_stats = []
    failed_years = []
    
    total_years = len(year_links)
    print(f"\nStarting to process {total_years} years...")
    
    for i, (year, url) in enumerate(year_links, 1):
        print(f"\n[{i}/{total_years}] Processing {year}...")
        try:
            start_time = time.time()
            driver.get(url)
            time.sleep(2)  # Allow page to load
            
            # Extract page content
            try:
                page_content = driver.find_element(By.CSS_SELECTOR, "body").text
                all_data.append({'year': year, 'content': page_content})
            except Exception as e:
                print(f"  Could not extract page content: {str(e)[:50]}...")
            
            # Extract events
            events = extract_events(driver, year)
            all_events.append(events)
            
            # Extract stats
            stats = extract_stats(driver, year)
            if not stats:
                print(f"  Warning: No stats found for {year}")
                failed_years.append(year)
                # Save HTML for debugging
                with open(f"debug_{year}.html", "w", encoding="utf-8") as f:
                    f.write(driver.page_source)
            else:
                all_stats.extend(stats)
            
            elapsed = time.time() - start_time
            print(f"  Completed in {elapsed:.1f} seconds")
            
        except Exception as e:
            print(f"  Error processing {year}: {str(e)}")
            failed_years.append(year)
            continue
    
    # Save data
    print("\nSaving data to CSV files...")
    pd.DataFrame(all_data).to_csv("mlb_yearly_pages.csv", index=False)
    pd.DataFrame(all_events).to_csv("mlb_events.csv", index=False)
    pd.DataFrame(all_stats).to_csv("mlb_stats.csv", index=False)
    
    # Save list of failed years
    if failed_years:
        pd.DataFrame({'year': failed_years}).to_csv("failed_years.csv", index=False)
        print(f"\nWarning: Failed to extract stats for {len(failed_years)} years")
        print("Saved debug HTML files for these years")
    
    driver.quit()
    print("\nScraping complete!")

if __name__ == "__main__":
    main()
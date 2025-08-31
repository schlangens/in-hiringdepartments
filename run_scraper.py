#!/usr/bin/env python3
"""
Simple launcher for the Indiana Police Jobs Scraper
"""

import os
import sys
import webbrowser
from indiana_police_jobs_scraper import IndianaPoliceJobsScraper

def main():
    print("=" * 60)
    print("Indiana Police Jobs Scraper and Mapper")
    print("=" * 60)
    print()
    
    # Check if required packages are installed
    try:
        import requests
        import folium
        from bs4 import BeautifulSoup
        print("✓ All required packages are installed")
    except ImportError as e:
        print(f"✗ Missing required package: {e}")
        print("Please run: pip install requests beautifulsoup4 folium lxml")
        return
    
    print()
    print("Starting the scraper...")
    print("This will:")
    print("1. Scrape job opportunities from the ILEA website")
    print("2. Create an interactive map showing job locations")
    print("3. Save data to CSV file")
    print()
    
    try:
        # Run the scraper
        scraper = IndianaPoliceJobsScraper()
        map_obj, county_jobs = scraper.run()
        
        print()
        print("=" * 60)
        print("SCRAPER COMPLETED SUCCESSFULLY!")
        print("=" * 60)
        
        # Check if files were created
        map_file = 'indiana_police_jobs_map.html'
        csv_file = 'indiana_police_jobs.csv'
        
        if os.path.exists(map_file):
            print(f"✓ Interactive map created: {map_file}")
            print(f"  File size: {os.path.getsize(map_file)} bytes")
        else:
            print(f"✗ Map file not found: {map_file}")
        
        if os.path.exists(csv_file):
            print(f"✓ Job data saved: {csv_file}")
            print(f"  File size: {os.path.getsize(csv_file)} bytes")
        else:
            print(f"✗ CSV file not found: {csv_file}")
        
        print()
        print("To view the interactive map:")
        print(f"1. Open {map_file} in your web browser")
        print("2. Or run this command to open it automatically:")
        print(f"   start {map_file}")
        
        # Ask if user wants to open the map
        try:
            response = input("\nWould you like to open the map in your browser now? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                print("Opening map in browser...")
                webbrowser.open(f'file://{os.path.abspath(map_file)}')
        except KeyboardInterrupt:
            print("\nMap opening cancelled.")
        
        print()
        print("Thank you for using the Indiana Police Jobs Scraper!")
        
    except Exception as e:
        print(f"Error running scraper: {e}")
        print("Please check your internet connection and try again.")

if __name__ == "__main__":
    main()

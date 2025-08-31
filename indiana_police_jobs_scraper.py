#!/usr/bin/env python3
"""
Indiana Law Enforcement Job Opportunities Scraper and Mapper
Scrapes job opportunities from ILEA website and maps them by county
"""

import requests
from bs4 import BeautifulSoup
import folium
import json
import re
import csv
from collections import defaultdict
import time
from datetime import datetime

class IndianaPoliceJobsScraper:
    def __init__(self):
        self.base_url = "https://www.in.gov/ilea/bulletin-board/law-enforcement-job-opportunities/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Indiana counties with their coordinates (approximate center points)
        self.county_coordinates = {
            'Adams': (40.8372, -84.9338),
            'Allen': (41.0907, -85.0667),
            'Bartholomew': (39.2017, -85.8975),
            'Benton': (40.6064, -87.3108),
            'Blackford': (40.4736, -85.3247),
            'Boone': (40.0506, -86.4686),
            'Brown': (39.1961, -86.2275),
            'Carroll': (40.5828, -86.5625),
            'Cass': (40.7614, -86.3461),
            'Clark': (38.4772, -85.7072),
            'Clay': (39.4167, -87.1167),
            'Clinton': (40.3017, -86.4750),
            'Crawford': (38.2917, -86.4583),
            'Daviess': (38.7000, -87.0833),
            'Dearborn': (39.1458, -84.9722),
            'Decatur': (39.3083, -85.5000),
            'DeKalb': (41.3972, -85.0000),
            'Delaware': (40.2278, -85.3972),
            'Dubois': (38.3625, -86.8792),
            'Elkhart': (41.5972, -85.8583),
            'Fayette': (39.6417, -85.1792),
            'Floyd': (38.3208, -85.9042),
            'Fountain': (40.1208, -87.2417),
            'Franklin': (39.4167, -85.0583),
            'Fulton': (41.0472, -86.2639),
            'Gibson': (38.3125, -87.5833),
            'Grant': (40.5153, -85.6542),
            'Greene': (39.0375, -86.9625),
            'Hamilton': (40.0736, -86.0514),
            'Hancock': (39.8236, -85.7736),
            'Harrison': (38.1958, -86.1208),
            'Hendricks': (39.7694, -86.5097),
            'Henry': (39.9306, -85.3969),
            'Howard': (40.4833, -86.1167),
            'Huntington': (40.8292, -85.4972),
            'Jackson': (38.9083, -86.0375),
            'Jasper': (41.0236, -87.1167),
            'Jay': (40.4375, -85.0042),
            'Jefferson': (38.7875, -85.4375),
            'Jennings': (38.9958, -85.6292),
            'Johnson': (39.4903, -86.1014),
            'Knox': (38.6875, -87.4125),
            'Kosciusko': (41.2444, -85.8606),
            'LaGrange': (41.6425, -85.4264),
            'Lake': (41.4167, -87.3833),
            'LaPorte': (41.5467, -86.7222),
            'Lawrence': (38.8417, -86.4833),
            'Madison': (40.1611, -85.7194),
            'Marion': (39.7817, -86.1386),
            'Marshall': (41.3247, -86.2611),
            'Martin': (38.7083, -86.8042),
            'Miami': (40.7694, -86.0458),
            'Monroe': (39.1606, -86.5231),
            'Montgomery': (40.0403, -86.8931),
            'Morgan': (39.4819, -86.4469),
            'Newton': (40.9556, -87.3972),
            'Noble': (41.3986, -85.4175),
            'Ohio': (38.9500, -84.9667),
            'Orange': (38.5417, -86.4958),
            'Owen': (39.3125, -86.8375),
            'Parke': (39.7736, -87.2069),
            'Perry': (38.0792, -86.6375),
            'Pike': (38.4000, -87.2333),
            'Porter': (41.4606, -87.0681),
            'Posey': (38.0208, -87.7833),
            'Pulaski': (41.0417, -86.6958),
            'Putnam': (39.6667, -86.8417),
            'Randolph': (40.1575, -85.0111),
            'Ripley': (39.1042, -85.2625),
            'Rush': (39.6208, -85.4667),
            'Saint Joseph': (41.6181, -86.2903),
            'Scott': (38.6833, -85.7458),
            'Shelby': (39.5208, -85.7917),
            'Spencer': (37.9167, -87.0083),
            'Starke': (41.2786, -86.6472),
            'Steuben': (41.6431, -85.0000),
            'Sullivan': (39.0875, -87.4125),
            'Switzerland': (38.8250, -85.0375),
            'Tippecanoe': (40.3889, -86.8931),
            'Tipton': (40.3111, -86.0514),
            'Union': (39.6250, -84.9250),
            'Vanderburgh': (38.0250, -87.5875),
            'Vermillion': (39.8542, -87.4625),
            'Vigo': (39.4306, -87.3897),
            'Wabash': (40.8458, -85.7944),
            'Warren': (40.3472, -87.3536),
            'Warrick': (38.0917, -87.2708),
            'Washington': (38.6000, -86.1042),
            'Wayne': (39.8647, -85.0097),
            'Wells': (40.7292, -85.2208),
            'White': (40.7500, -86.8667),
            'Whitley': (41.1397, -85.4986)
        }

    def scrape_job_opportunities(self):
        """Scrape job opportunities from the ILEA website"""
        try:
            print("Scraping job opportunities from ILEA website...")
            response = self.session.get(self.base_url, timeout=30)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.content, 'html.parser')
            
            job_listings = []
            
            # Find all job links in the list
            job_links = soup.find_all('a', href=re.compile(r'^#'))
            
            print(f"Found {len(job_links)} job links")
            
            for link in job_links:
                link_text = link.get_text(strip=True)
                if link_text.startswith('Hiring:'):
                    # Extract department name from link text
                    department = link_text.replace('Hiring:', '').strip()
                    anchor_id = link.get('href')[1:]  # Remove the # from href
                    
                    # Find the corresponding job description section
                    job_section = soup.find('a', attrs={'name': anchor_id})
                    if job_section:
                        # Get the job description content
                        description_content = []
                        current_element = job_section.find_next_sibling()
                        
                        # Collect content until we hit the next job section or end
                        while current_element and not (current_element.name == 'a' and current_element.get('name')):
                            if current_element.name in ['p', 'h3', 'h4', 'h5', 'h6']:
                                text = current_element.get_text(strip=True)
                                if text and not text.startswith('Job closing dates'):
                                    description_content.append(text)
                            current_element = current_element.find_next_sibling()
                        
                        # Join the description content
                        description = ' '.join(description_content)
                        
                        # If description is still empty, try a different approach
                        if not description:
                            # Look for the next h3 element which should contain the department name
                            next_h3 = job_section.find_next('h3')
                            if next_h3:
                                # Get all text from h3 until the next hr or h3
                                current = next_h3.find_next_sibling()
                                while current and current.name not in ['hr', 'h3']:
                                    if current.name in ['p', 'div']:
                                        text = current.get_text(strip=True)
                                        if text:
                                            description_content.append(text)
                                    current = current.find_next_sibling()
                                description = ' '.join(description_content)
                        
                        # Debug: Print first few characters of description
                        if description:
                            print(f"  - {department}: {description[:100]}...")
                        else:
                            print(f"  - {department}: No description found")
                        
                        # Extract closing date if present
                        closing_date = None
                        date_match = re.search(r'UNTIL\s+([A-Z]+\s+\d{1,2},?\s+\d{4})', description, re.IGNORECASE)
                        if date_match:
                            closing_date = date_match.group(1)
                        
                        # Extract contact information
                        contact_info = []
                        email_matches = re.findall(r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}', description)
                        phone_matches = re.findall(r'\(\d{3}\)\s*\d{3}-\d{4}', description)
                        
                        if email_matches:
                            contact_info.extend(email_matches)
                        if phone_matches:
                            contact_info.extend(phone_matches)
                        
                        job_info = {
                            'department': department,
                            'location': self.extract_location_from_department(department),
                            'details': description[:500] + '...' if len(description) > 500 else description,
                            'full_description': description,
                            'closing_date': closing_date,
                            'contact_info': '; '.join(contact_info) if contact_info else '',
                            'anchor_id': anchor_id,
                            'ilea_link': f"{self.base_url}#{anchor_id}",
                            'date_posted': datetime.now().strftime('%Y-%m-%d')
                        }
                        
                        job_listings.append(job_info)
            
            print(f"Successfully extracted {len(job_listings)} job listings")
            
            # If no jobs found, use sample data for demonstration
            if not job_listings:
                print("No job listings found on website, using sample data for demonstration...")
                return self.get_sample_data()
            
            return job_listings
            
        except Exception as e:
            print(f"Error scraping website: {e}")
            # Return sample data for demonstration
            return self.get_sample_data()
    
    def extract_location_from_department(self, department):
        """Extract location information from department name"""
        # Common patterns in department names
        location_patterns = [
            r'(\w+\s+County)\s+Sheriff',
            r'(\w+\s+Police\s+Department)',
            r'(\w+\s+Marshal)',
            r'(\w+\s+University)',
            r'(\w+\s+Schools)',
            r'(\w+\s+Township)',
            r'(\w+\s+International\s+Airport)',
            r'(\w+\s+Department\s+Of\s+Natural\s+Resources)',
            r'(\w+\s+Department\s+Of\s+Correction)'
        ]
        
        for pattern in location_patterns:
            match = re.search(pattern, department, re.IGNORECASE)
            if match:
                return match.group(1)
        
        # If no pattern matches, return the department name
        return department
    
    def get_sample_data(self):
        """Return sample data for demonstration purposes"""
        print("Using sample data for demonstration...")
        return [
            {
                'department': 'Indianapolis Metropolitan Police Department',
                'location': 'Marion County',
                'details': 'Police Officer - Entry Level Position',
                'full_description': 'Police Officer - Entry Level Position with competitive salary and benefits.',
                'closing_date': '2024-12-31',
                'contact_info': 'hr@indy.gov',
                'anchor_id': 'IMPD',
                'date_posted': '2024-01-15'
            },
            {
                'department': 'Fort Wayne Police Department',
                'location': 'Allen County',
                'details': 'Patrol Officer - Lateral Transfer',
                'full_description': 'Patrol Officer - Lateral Transfer position available for experienced officers.',
                'closing_date': '2024-11-30',
                'contact_info': 'recruiting@fwpd.org',
                'anchor_id': 'FWPD',
                'date_posted': '2024-01-14'
            },
            {
                'department': 'Evansville Police Department',
                'location': 'Vanderburgh County',
                'details': 'Police Officer - Academy Graduate',
                'full_description': 'Police Officer position for academy graduates with competitive benefits.',
                'closing_date': '2024-10-15',
                'contact_info': 'careers@evansvillepolice.com',
                'anchor_id': 'EPD',
                'date_posted': '2024-01-13'
            }
        ]
    
    def extract_county_from_location(self, location):
        """Extract county name from location string"""
        location_lower = location.lower()
        
        # Direct county matches
        for county in self.county_coordinates.keys():
            if county.lower() in location_lower:
                return county
        
        # City to county mappings (major cities)
        city_to_county = {
            'indianapolis': 'Marion',
            'fort wayne': 'Allen',
            'evansville': 'Vanderburgh',
            'south bend': 'Saint Joseph',
            'carmel': 'Hamilton',
            'fishers': 'Hamilton',
            'bloomington': 'Monroe',
            'lafayette': 'Tippecanoe',
            'gary': 'Lake',
            'hammond': 'Lake',
            'muncie': 'Delaware',
            'anderson': 'Madison',
            'terre haute': 'Vigo',
            'elkhart': 'Elkhart',
            'kokomo': 'Howard',
            'noblesville': 'Hamilton',
            'greenwood': 'Johnson',
            'michigan city': 'LaPorte',
            'merrillville': 'Lake',
            'lawrence': 'Marion',
            'greenfield': 'Hancock',
            'new albany': 'Floyd',
            'jeffersonville': 'Clark',
            'richmond': 'Wayne',
            'columbus': 'Bartholomew',
            'plainfield': 'Hendricks',
            'kingsford heights': 'LaPorte',
            'alexandria': 'Madison',
            'roseland': 'Saint Joseph',
            'monrovia': 'Morgan',
            'eaton': 'Delaware',
            'frankfort': 'Clinton',
            'mccordsville': 'Hancock',
            'shelbyville': 'Shelby',
            'scottsburg': 'Scott',
            'sweetser': 'Grant',
            'lebanon': 'Boone',
            'rochester': 'Fulton',
            'waterloo': 'DeKalb',
            'cumberland': 'Marion',
            'brazil': 'Clay',
            'fortville': 'Hancock',
            'dyer': 'Lake',
            'dunkirk': 'Jay',
            'princeton': 'Gibson',
            'portland': 'Jay',
            'montpelier': 'Blackford',
            'homecroft': 'Marion',
            'jonesboro': 'Grant',
            'westville': 'LaPorte',
            'valparaiso': 'Porter',
            'warsaw': 'Kosciusko',
            'hartford city': 'Blackford',
            'logansport': 'Cass',
            'mount vernon': 'Posey',
            'boone': 'Boone',
            'grant': 'Grant',
            'elkhart': 'Elkhart',
            'monroe': 'Monroe',
            'tippecanoe': 'Tippecanoe',
            'frankton': 'Madison',
            'west lafayette': 'Tippecanoe',
            'gibson': 'Gibson',
            'wayne': 'Wayne',
            'starke': 'Starke',
            'whitley': 'Whitley',
            'steuben': 'Steuben'
        }
        
        for city, county in city_to_county.items():
            if city in location_lower:
                return county
        
        return None
    
    def process_job_data(self, job_listings):
        """Process job listings and group by county"""
        county_jobs = defaultdict(list)
        
        for job in job_listings:
            county = self.extract_county_from_location(job['location'])
            if county:
                county_jobs[county].append(job)
            else:
                # If county not found, try to extract from department name
                county = self.extract_county_from_location(job['department'])
                if county:
                    county_jobs[county].append(job)
        
        return county_jobs
    
    def create_interactive_map(self, county_jobs):
        """Create an interactive map showing job opportunities by county with side panel"""
        # Create a map centered on Indiana
        m = folium.Map(
            location=[39.8494, -86.2583],  # Center of Indiana
            zoom_start=7,
            tiles='OpenStreetMap'
        )
        
        # Create side panel with job listings
        side_panel_html = self.create_side_panel_html(county_jobs)
        m.get_root().html.add_child(folium.Element(side_panel_html))
        
        # Color scale for job counts
        max_jobs = max(len(jobs) for jobs in county_jobs.values()) if county_jobs else 1
        
        for county, jobs in county_jobs.items():
            if county in self.county_coordinates:
                lat, lon = self.county_coordinates[county]
                job_count = len(jobs)
                
                # Create popup content
                popup_content = f"""
                <div style="width: 350px;">
                    <h3>{county} County</h3>
                    <p><strong>Job Opportunities: {job_count}</strong></p>
                    <hr>
                """
                
                for i, job in enumerate(jobs[:5]):  # Show first 5 jobs
                    popup_content += f"""
                    <div style="margin-bottom: 10px; padding: 8px; border-left: 3px solid #007bff; background-color: #f8f9fa;">
                        <strong>{job['department']}</strong><br>
                        <em>{job['location']}</em><br>
                        {job['details'][:100]}...<br>
                        <small>Posted: {job['date_posted']}</small>
                        {f'<br><small style="color: red;">Closing: {job["closing_date"]}</small>' if job['closing_date'] else ''}
                        <br><a href="{job['ilea_link']}" target="_blank" style="color: #007bff; text-decoration: underline;">View Full Posting →</a>
                    </div>
                    """
                
                if len(jobs) > 5:
                    popup_content += f"<p><em>... and {len(jobs) - 5} more opportunities</em></p>"
                
                popup_content += "</div>"
                
                # Determine color based on job count
                if job_count == 0:
                    color = '#f0f0f0'  # Light gray
                elif job_count == 1:
                    color = '#ffeb3b'  # Yellow
                elif job_count == 2:
                    color = '#ff9800'  # Orange
                elif job_count == 3:
                    color = '#ff5722'  # Deep Orange
                else:
                    color = '#f44336'  # Red
                
                # Add marker
                folium.CircleMarker(
                    location=[lat, lon],
                    radius=10 + (job_count * 2),  # Size based on job count
                    popup=folium.Popup(popup_content, max_width=400),
                    color='black',
                    weight=2,
                    fillColor=color,
                    fillOpacity=0.7,
                    tooltip=f"{county} County: {job_count} job(s)"
                ).add_to(m)
        
        # Add legend
        legend_html = '''
        <style>
        @media (max-width: 768px) {
            .legend {
                bottom: 10px !important;
                left: 10px !important;
                width: 150px !important;
                height: 100px !important;
                font-size: 12px !important;
                padding: 8px !important;
            }
        }
        </style>
        <div class="legend" style="position: fixed; 
                    bottom: 50px; left: 50px; width: 200px; height: 120px; 
                    background-color: white; border:2px solid grey; z-index:9999; 
                    font-size:14px; padding: 10px; border-radius: 5px; box-shadow: 0 2px 5px rgba(0,0,0,0.2);">
        <p style="margin: 0 0 8px 0;"><strong>Job Opportunities</strong></p>
        <p style="margin: 4px 0;"><span style="color:#ffeb3b;">●</span> 1 job</p>
        <p style="margin: 4px 0;"><span style="color:#ff9800;">●</span> 2 jobs</p>
        <p style="margin: 4px 0;"><span style="color:#ff5722;">●</span> 3 jobs</p>
        <p style="margin: 4px 0;"><span style="color:#f44336;">●</span> 4+ jobs</p>
        </div>
        '''
        m.get_root().html.add_child(folium.Element(legend_html))
        
        return m
    
    def create_side_panel_html(self, county_jobs):
        """Create a side panel with job listings"""
        # Collect all jobs for the side panel
        all_jobs = []
        for county, jobs in county_jobs.items():
            for job in jobs:
                job['county'] = county
                all_jobs.append(job)
        
        # Sort jobs by county and department
        all_jobs.sort(key=lambda x: (x['county'], x['department']))
        
        side_panel_html = f"""
        <style>
        @media (max-width: 768px) {{
            .side-panel {{
                width: 100% !important;
                height: 100vh !important;
                top: 0 !important;
                right: 0 !important;
                transform: translateX(100%);
                transition: transform 0.3s ease;
            }}
            .side-panel.open {{
                transform: translateX(0);
            }}
            .toggle-btn {{
                display: block !important;
            }}
            .map-container {{
                margin-right: 0 !important;
            }}
        }}
        @media (min-width: 769px) {{
            .side-panel {{
                transform: translateX(0) !important;
            }}
            .toggle-btn {{
                display: none !important;
            }}
            .map-container {{
                margin-right: 350px !important;
            }}
        }}
        </style>
        
        <!-- Toggle Button for Mobile -->
        <button class="toggle-btn" onclick="toggleSidePanel()" 
                style="position: fixed; top: 10px; right: 10px; z-index: 10000; 
                       background: #007bff; color: white; border: none; padding: 10px 15px; 
                       border-radius: 5px; font-size: 14px; font-weight: bold; cursor: pointer;
                       box-shadow: 0 2px 5px rgba(0,0,0,0.2); display: none;">
            📋 Jobs ({len(all_jobs)})
        </button>
        
        <div class="side-panel" id="sidePanel" style="position: fixed; 
                    top: 10px; right: 10px; width: 350px; height: 90vh; 
                    background-color: white; border:2px solid #007bff; z-index:9999; 
                    font-size:12px; padding: 10px; overflow-y: auto; box-shadow: 0 4px 8px rgba(0,0,0,0.1);">
            <div style="background-color: #007bff; color: white; padding: 8px; margin: -10px -10px 10px -10px; display: flex; justify-content: space-between; align-items: center;">
                <h3 style="margin: 0; font-size: 16px;">Indiana Police Jobs ({len(all_jobs)} total)</h3>
                <button onclick="toggleSidePanel()" style="background: none; border: none; color: white; font-size: 20px; cursor: pointer; display: none;" class="close-btn">×</button>
            </div>
            <div style="margin-bottom: 10px;">
                <input type="text" id="jobSearch" placeholder="Search jobs..." 
                       style="width: 100%; padding: 5px; border: 1px solid #ddd; border-radius: 3px;"
                       onkeyup="filterJobs()">
            </div>
            <div id="jobList">
        """
        
        current_county = None
        for job in all_jobs:
            if job['county'] != current_county:
                if current_county is not None:
                    side_panel_html += "</div>"  # Close previous county section
                current_county = job['county']
                side_panel_html += f"""
                <div class="county-section" data-county="{job['county']}">
                    <div style="background-color: #f8f9fa; padding: 5px; margin: 5px 0; border-left: 3px solid #007bff; font-weight: bold; font-size: 11px;">
                        {job['county']} County
                    </div>
                """
            
            closing_date_text = f"<br><span style='color: red; font-size: 10px;'>Closes: {job['closing_date']}</span>" if job['closing_date'] else ""
            
            side_panel_html += f"""
                <div class="job-item" data-department="{job['department'].lower()}" data-county="{job['county'].lower()}">
                    <div style="border: 1px solid #ddd; margin: 3px 0; padding: 8px; border-radius: 3px; background-color: #fafafa;">
                        <div style="font-weight: bold; font-size: 11px; color: #333; margin-bottom: 3px;">
                            {job['department']}
                        </div>
                        <div style="font-size: 10px; color: #666; margin-bottom: 3px;">
                            {job['location']}
                        </div>
                        <div style="font-size: 10px; color: #555; margin-bottom: 3px; line-height: 1.3;">
                            {job['details'][:80]}...
                        </div>
                        {closing_date_text}
                        <div style="margin-top: 5px;">
                            <a href="{job['ilea_link']}" target="_blank" 
                               style="color: #007bff; text-decoration: none; font-size: 10px; font-weight: bold;">
                                View Full Posting →
                            </a>
                        </div>
                    </div>
                </div>
            """
        
        side_panel_html += """
            </div>
            </div>
        </div>
        
        <script>
        function filterJobs() {
            var input = document.getElementById('jobSearch');
            var filter = input.value.toLowerCase();
            var jobItems = document.getElementsByClassName('job-item');
            
            for (var i = 0; i < jobItems.length; i++) {
                var jobItem = jobItems[i];
                var department = jobItem.getAttribute('data-department');
                var county = jobItem.getAttribute('data-county');
                
                if (department.includes(filter) || county.includes(filter)) {
                    jobItem.style.display = 'block';
                } else {
                    jobItem.style.display = 'none';
                }
            }
        }
        
        function toggleSidePanel() {
            var panel = document.getElementById('sidePanel');
            var toggleBtn = document.querySelector('.toggle-btn');
            var closeBtn = document.querySelector('.close-btn');
            
            if (panel.classList.contains('open')) {
                panel.classList.remove('open');
                if (toggleBtn) toggleBtn.style.display = 'block';
                if (closeBtn) closeBtn.style.display = 'none';
            } else {
                panel.classList.add('open');
                if (toggleBtn) toggleBtn.style.display = 'none';
                if (closeBtn) closeBtn.style.display = 'block';
            }
        }
        
        // Show close button on mobile
        function updateMobileUI() {
            var closeBtn = document.querySelector('.close-btn');
            if (window.innerWidth <= 768) {
                if (closeBtn) closeBtn.style.display = 'block';
            } else {
                if (closeBtn) closeBtn.style.display = 'none';
            }
        }
        
        // Update UI on window resize
        window.addEventListener('resize', updateMobileUI);
        
        // Initialize mobile UI
        updateMobileUI();
        </script>
        """
        
        return side_panel_html
    
    def create_jobs_table_html(self, county_jobs):
        """Create an HTML table of all job opportunities"""
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Indiana Police Jobs - Complete Listing</title>
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                table { border-collapse: collapse; width: 100%; margin-top: 20px; }
                th, td { border: 1px solid #ddd; padding: 12px; text-align: left; }
                th { background-color: #f2f2f2; font-weight: bold; }
                tr:nth-child(even) { background-color: #f9f9f9; }
                tr:hover { background-color: #f5f5f5; }
                .closing-date { color: red; font-weight: bold; }
                .contact-info { font-size: 0.9em; color: #666; }
                .county-header { background-color: #007bff; color: white; padding: 10px; margin-top: 20px; }
                .job-details { max-width: 400px; }
            </style>
        </head>
        <body>
            <h1>Indiana Law Enforcement Job Opportunities</h1>
            <p>Complete listing of all available positions across Indiana counties</p>
        """
        
        total_jobs = sum(len(jobs) for jobs in county_jobs.values())
        html_content += f"<p><strong>Total Job Opportunities: {total_jobs}</strong></p>"
        
        for county, jobs in sorted(county_jobs.items()):
            html_content += f"""
            <div class="county-header">
                <h2>{county} County - {len(jobs)} Job(s)</h2>
            </div>
            <table>
                <thead>
                                    <tr>
                    <th>Department</th>
                    <th>Location</th>
                    <th>Details</th>
                    <th>Closing Date</th>
                    <th>Contact Info</th>
                    <th>ILEA Link</th>
                    <th>Posted Date</th>
                </tr>
                </thead>
                <tbody>
            """
            
            for job in jobs:
                closing_date_cell = f'<span class="closing-date">{job["closing_date"]}</span>' if job['closing_date'] else 'No closing date'
                contact_cell = f'<div class="contact-info">{job["contact_info"]}</div>' if job['contact_info'] else 'No contact info'
                
                html_content += f"""
                <tr>
                    <td><strong>{job['department']}</strong></td>
                    <td>{job['location']}</td>
                    <td class="job-details">{job['details']}</td>
                    <td>{closing_date_cell}</td>
                    <td>{contact_cell}</td>
                    <td><a href="{job['ilea_link']}" target="_blank" style="color: #007bff; text-decoration: underline;">View Full Posting</a></td>
                    <td>{job['date_posted']}</td>
                </tr>
                """
            
            html_content += """
                </tbody>
            </table>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        return html_content
    
    def save_data_to_csv(self, county_jobs, filename='indiana_police_jobs.csv'):
        """Save job data to CSV file"""
        all_jobs = []
        for county, jobs in county_jobs.items():
            for job in jobs:
                job['county'] = county
                all_jobs.append(job)
        
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['department', 'location', 'details', 'full_description', 'closing_date', 'contact_info', 'anchor_id', 'ilea_link', 'county', 'date_posted']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for job in all_jobs:
                writer.writerow(job)
        
        print(f"Job data saved to {filename}")
    
    def run(self):
        """Main method to run the scraper and create the map"""
        print("Starting Indiana Police Jobs Scraper...")
        
        # Scrape job opportunities
        job_listings = self.scrape_job_opportunities()
        
        # Process and group by county
        county_jobs = self.process_job_data(job_listings)
        
        # Save data to CSV
        self.save_data_to_csv(county_jobs)
        
        # Create interactive map
        map_obj = self.create_interactive_map(county_jobs)
        
        # Save map
        map_filename = 'indiana_police_jobs_map.html'
        map_obj.save(map_filename)
        print(f"Interactive map saved to {map_filename}")
        
        # Create and save jobs table
        table_html = self.create_jobs_table_html(county_jobs)
        table_filename = 'indiana_police_jobs_table.html'
        with open(table_filename, 'w', encoding='utf-8') as f:
            f.write(table_html)
        print(f"Jobs table saved to {table_filename}")
        
        # Print summary
        print("\n" + "="*50)
        print("SUMMARY")
        print("="*50)
        total_jobs = sum(len(jobs) for jobs in county_jobs.values())
        print(f"Total job opportunities found: {total_jobs}")
        print(f"Counties with job opportunities: {len(county_jobs)}")
        
        for county, jobs in sorted(county_jobs.items()):
            print(f"{county} County: {len(jobs)} job(s)")
        
        print(f"\nFiles created:")
        print(f"- {map_filename} (Interactive map)")
        print(f"- {table_filename} (Jobs table)")
        print(f"- indiana_police_jobs.csv (Job data)")
        
        return map_obj, county_jobs

if __name__ == "__main__":
    scraper = IndianaPoliceJobsScraper()
    map_obj, county_jobs = scraper.run()

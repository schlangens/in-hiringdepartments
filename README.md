# Indiana Police Jobs Scraper and Mapper

A Python application that scrapes law enforcement job opportunities from the Indiana Law Enforcement Academy (ILEA) website and creates an interactive map showing job locations across Indiana counties.

## 🌐 Live Demo

**View the interactive map online:** [Indiana Police Jobs Map](https://schlangens.github.io/in-hiringdepartments/)

## Features

- **Real-time Job Scraping**: Automatically scrapes current job postings from the ILEA website
- **Interactive County Map**: Visual representation of job opportunities across Indiana's 92 counties
- **Clickable Job Links**: Direct links to original ILEA job postings
- **Searchable Side Panel**: Real-time filtering of job listings by department or county
- **Complete Job Details**: Full descriptions, closing dates, and contact information
- **Multiple Output Formats**: HTML map, detailed table, and CSV data export

## Files Generated

1. **`indiana_police_jobs_map.html`** - Interactive map with side panel (main output)
2. **`indiana_police_jobs_table.html`** - Complete job listings table
3. **`indiana_police_jobs.csv`** - Structured data export

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/schlangens/in-hiringdepartments.git
   cd in-hiringdepartments
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Quick Start
```bash
python run_scraper.py
```

### Manual Execution
```bash
python indiana_police_jobs_scraper.py
```

## Output

The scraper generates:
- **Interactive Map**: Color-coded counties showing job opportunities
- **Side Panel**: Searchable list of all jobs with direct links
- **Data Export**: CSV file with complete job information

## County Coverage

The application covers all 92 Indiana counties with:
- **Smart Location Detection**: Automatically maps departments to counties
- **City-to-County Mapping**: Handles major cities and their counties
- **Geographic Coordinates**: Precise county center points for mapping

## Error Handling

- **Fallback Data**: Uses sample data if website is unavailable
- **Robust Scraping**: Handles website structure changes gracefully
- **Comprehensive Logging**: Detailed output for troubleshooting

## Customization

### Adding New Counties
Edit the `county_coordinates` dictionary in the scraper to add new counties.

### Modifying Job Extraction
Customize the `extract_location_from_department()` method for different department naming patterns.

### Styling Changes
Modify the CSS in `create_interactive_map()` and `create_side_panel_html()` methods.

## Troubleshooting

### Common Issues

1. **No jobs found**: Check internet connection and ILEA website availability
2. **Missing counties**: Verify county names match the coordinates dictionary
3. **Installation errors**: Ensure Python 3.7+ and all dependencies are installed

### Dependencies

- `requests` - HTTP requests
- `beautifulsoup4` - HTML parsing
- `folium` - Interactive mapping
- `lxml` - XML/HTML parser

## Future Enhancements

- [ ] Email notifications for new job postings
- [ ] Historical job data tracking
- [ ] Salary information extraction
- [ ] Mobile-responsive design improvements
- [ ] Job application status tracking

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please open an issue on GitHub or contact the maintainer.

---

**Last Updated**: January 2024  
**Data Source**: [ILEA Job Opportunities](https://www.in.gov/ilea/bulletin-board/law-enforcement-job-opportunities/)

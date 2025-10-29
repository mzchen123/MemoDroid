# MemoDroid Bug Collection System

This directory contains a comprehensive system for collecting and analyzing bug reports from F-Droid applications and their corresponding GitHub repositories. The system is designed to gather, process, and analyze bug reports to help understand common issues in open-source Android applications.

## System Components

### 1. Data Collection
- **F-Droid Spider** (`fdroid_spider.py`): A Scrapy-based spider that crawls F-Droid to collect information about available applications.
- **GitHub Spider** (`github_spider.py`): Collects bug reports and issues from GitHub repositories associated with F-Droid applications.

### 2. Data Processing
- **Merge and Analysis** (`merge_and_analysis.py`): Processes and analyzes the collected data, focusing on specific categories (money, multimedia, reading).
- **Data Selection** (`choose_data.py`): Helps in selecting and filtering relevant data from the collected information.

### 3. Testing
- **Single GitHub Test** (`test_single_github.py`): A utility script for testing GitHub repository data collection.

## Setup and Usage

1. **Environment Setup**
   ```bash
   pip install scrapy beautifulsoup4 pandas langchain-community tqdm
   ```

2. **Data Collection Process**
   ```bash
   # Generate start URLs
   python gen_start_urls.py
   
   # Run F-Droid spider
   scrapy runspider fdroid_spider.py
   
   # Collect GitHub issues
   python github_spider.py
   ```

3. **Data Analysis**
   ```bash
   python merge_and_analysis.py
   ```

## Output Files

The system generates several CSV files:
- `fdroid_data.csv`: Raw data from F-Droid
- `issues_closed.csv`: Closed issues from GitHub repositories
- `issues_open.csv`: Open issues from GitHub repositories
- `filtered_apps_all.csv`: Complete filtered results

## Configuration

- GitHub API token needs to be configured in `github_spider.py`
- Target categories can be modified in `merge_and_analysis.py`

## Notes

- The system focuses on applications updated since January 1, 2023
- Data is collected from both F-Droid and GitHub repositories
- Results are filtered by specific categories (money, multimedia, reading)
- All output files are saved in UTF-8 with BOM encoding for compatibility


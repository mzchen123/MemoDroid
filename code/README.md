# Code

This repository contains the core implementation of MemoDroid, a comprehensive system for analyzing and processing Android application interactions and bug reports.

## Project Structure

The codebase is organized into two main components:

### 1. Core Source Code (`/src`)

The core implementation of MemoDroid, organized into several modules:

#### Configuration (`/config`)
- `config.py`: Application-wide configuration settings and constants

#### Models (`/models`)
- `models.py`: Base model definitions and utilities
- `gme_model.py`: GME (General Memory Engine) model implementation
- `gme_inference.py`: GME model inference logic

#### Processors (`/processors`)
- `action_processor.py`: Action processing and execution logic
- `rag_processor.py`: RAG (Retrieval-Augmented Generation) processing

#### Utilities (`/utils`)
- `logger.py`: Logging configuration and utilities

### 2. Bug Collection System (`/collect_bugs`)

A comprehensive system for collecting and analyzing bug reports from F-Droid applications:

#### Data Collection
- `fdroid_spider.py`: Scrapy-based spider for F-Droid crawling
- `github_spider.py`: GitHub issues collection spider

#### Data Processing
- `merge_and_analysis.py`: Data processing and analysis
- `choose_data.py`: Data selection and filtering

#### Testing
- `test_single_github.py`: GitHub repository data collection testing

## Demo Implementation

The `demo.py` file provides a demonstration of the core functionality:
- Loads interaction records from JSON files
- Processes actions and screenshots
- Utilizes the ActionHistoryProcessor for analysis
- Saves results to output files

> **Note**: The `demo.py` and the MemoDroid implementation in `/src` serve as a knowledge base construction and retrieval system. The retrieved knowledge can be injected into LLM-based Testing Tools through prompts, enabling seamless integration of historical interaction data and bug reports into the testing process. This integration enhances the testing tool's ability to understand application context and potential issues.

## Environment Setup

### 1. Android Studio Setup
1. Download Android Studio from [official website](https://developer.android.com/studio)
2. Install Android Studio following the installation wizard
3. Launch Android Studio and complete the initial setup

### 2. Android Virtual Device (AVD) Setup
1. Open Android Studio
2. Click "Tools" > "Device Manager" > "Create Virtual Device"
3. Select a device definition (e.g., Pixel 2)
4. Select a system image:
   - Choose x86 Images for better performance
   - Recommended: API 30 (Android 11.0) or higher
   - Download the system image if not available
5. Configure AVD settings:
   - Set device name
   - Adjust RAM size (recommended: 2GB or more)
   - Set internal storage (recommended: 2GB or more)
6. Click "Finish" to create the AVD

### 3. Physical Device Setup (Alternative)
1. Enable Developer Options on your Android device:
   - Go to Settings > About Phone
   - Tap "Build Number" 7 times
2. Enable USB debugging in Developer Options
3. Connect device via USB
4. Allow USB debugging on device when prompted

## Setup and Installation

1. Install required dependencies:
```bash
pip install -r requirements.txt
```

2. Configure the application:
   - Set up API keys in the configuration
   - Adjust processor settings as needed

## Usage

### Running the Demo
```bash
python demo.py
```

### Bug Collection System
```bash
# Generate start URLs
python collect_bugs/gen_start_urls.py

# Run F-Droid spider
scrapy runspider collect_bugs/fdroid_spider.py

# Collect GitHub issues
python collect_bugs/github_spider.py

# Analyze data
python collect_bugs/merge_and_analysis.py
```

## Dependencies

Key dependencies include:
- Python 3.x
- PyTorch (>=2.0.0)
- Transformers (>=4.30.0)
- OpenAI (>=1.0.0)
- FAISS-CPU (>=1.7.4)
- Pillow (>=9.0.0)
- Pydantic (>=2.0.0)
- Qwen-VL-Utils
- DashScope
- NumPy (>=1.24.0)

# MemoDroid Source Code

This directory contains the core source code for the MemoDroid project. The codebase is organized into several modules, each serving a specific purpose in the application's architecture.

## Directory Structure

### `/config`
Configuration management for the application.
- `config.py`: Contains application-wide configuration settings and constants.

### `/models`
Core data models and model-related functionality.
- `models.py`: Base model definitions and common model utilities.
- `gme_model.py`: Implementation of the GME (General Memory Engine) model.
- `gme_inference.py`: Inference logic and utilities for the GME model.

### `/processors`
Data processing and business logic components.
- `action_processor.py`: Handles action processing and execution logic.
- `rag_processor.py`: Implements RAG (Retrieval-Augmented Generation) processing functionality.

### `/utils`
Utility functions and helper modules.
- `logger.py`: Logging configuration and utility functions.

## Key Components

### Models
The models module contains the core data structures and model implementations used throughout the application. The GME model implementation includes both the model definition and inference logic.

### Processors
The processors module handles the main business logic of the application, including:
- Action processing and execution
- RAG-based processing for enhanced memory and retrieval capabilities

### Configuration
The configuration module provides a centralized way to manage application settings and constants, making it easy to modify application behavior without changing the core code.

### Utilities
The utilities module provides common functionality used across the application, with a focus on logging and other helper functions.

## Usage

To use this codebase:
1. Ensure all dependencies are installed
2. Configure the application using the settings in `config/config.py`
3. Import and use the required modules as needed

## Dependencies
- Python 3.x
- Additional dependencies are listed in the project's requirements.txt file 
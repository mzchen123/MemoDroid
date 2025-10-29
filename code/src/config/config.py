from pydantic import BaseModel
from typing import Optional

class ProcessorConfig(BaseModel):
    """Processor configuration class"""
    api_key: str
    base_url: str
    window_size: int = 10
    model_name: str = "Alibaba-NLP/gme-Qwen2-VL-2B-Instruct"
    output_dir: str = "output"
    log_file: str = "action_history_processor.log"
    max_retries: int = 3
    timeout: int = 30
    gme_api_key: str = "api_key"

# Log configuration
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
LOG_LEVEL = 'INFO'

# File path configuration
DEFAULT_OUTPUT_DIR = "output"
DEFAULT_LOG_FILE = "action_history_processor.log"
DEFAULT_ANALYSIS_FILE = "app_analysis.txt"
DEFAULT_SEGMENTS_FILE = "segments_data.json" 
from src.config.config import ProcessorConfig
from src.processors.action_processor import ActionHistoryProcessor
from src.models.models import FunctionSegment, RAGResult
from pathlib import Path
import json

def load_record_data(record_path: str):
    """Load record.json data"""
    with open(record_path, 'r', encoding='utf-8') as f:
        record_data = json.load(f)
    
    actions = []
    screenshots = []
    
    # Add initial screenshot
    screenshots.append(f"data_demo/screenshots/step_0.png")
    
    # Process each step
    for step in record_data['steps']:
        # Build action description
        action_type = step['action_type']
        action_detail = step['action_detail']
        
        if action_type == 'click':
            action_desc = f"Click at coordinates ({action_detail['x']}, {action_detail['y']})"
        elif action_type == 'swipe':
            action_desc = f"Swipe from ({action_detail['start_x']}, {action_detail['start_y']}) to ({action_detail['end_x']}, {action_detail['end_y']})"
        else:
            action_desc = f"Execute {action_type} operation"
            
        actions.append(action_desc)
        screenshots.append(f"data_demo/screenshots/{step['screen_shot']}")
    
    return actions, screenshots

def main():
    # Configure processor
    config = ProcessorConfig(
        api_key="your_api_key_here",
        base_url="your_base_url_here",
        model_name="Alibaba-NLP/gme-Qwen2-VL-2B-Instruct",
        window_size=10,
        max_retries=3,
        timeout=30,
        output_dir="./output",
        log_file="processor.log"
    )

    # Initialize processor
    processor = ActionHistoryProcessor(config)

    try:
        # Load record.json data
        actions, screenshots = load_record_data("data_demo/record.json")
        
        print(f"Loaded {len(actions)} actions and {len(screenshots)} screenshots")
        
        # Process and save results
        processor.process_and_save(actions, screenshots, "app_analysis_result.txt")
        
        # Build RAG index from processed segments
        segments_data = []
        with open("output/segments_data.json", 'r', encoding='utf-8') as f:
            segments_data = json.load(f)
            
        # Convert segments data to FunctionSegment objects
        segments = []
        for data in segments_data:
            segment = FunctionSegment(
                actions=data['actions'],
                screenshots=data['screenshots'],
                func_desc=data['func_desc'],
                action_detail=data['action_detail'],
                reasoning=data['reasoning']
            )
            segments.append(segment)
            
        # Build RAG index
        processor.rag_processor.build_index(segments)
        
        # Example RAG search queries
        print("\nPerforming RAG searches...")
        
        # Text-based search
        text_results = processor.search_rag(
            query_text="How to navigate to settings",
            k=2
        )
        print("\nText search results:")
        for result in text_results:
            print(f"- {result.segment.func_desc} (Score: {result.similarity_score:.3f})")
            
        # Image-based search
        image_results = processor.search_rag(
            query_image="data_demo/screenshots/step_1.png",
            k=2
        )
        print("\nImage search results:")
        for result in image_results:
            print(f"- {result.segment.func_desc} (Score: {result.similarity_score:.3f})")
            
        # Combined search
        combined_results = processor.search_rag(
            query_text="How to perform login",
            query_image="data_demo/screenshots/step_2.png",
            k=2
        )
        print("\nCombined search results:")
        for result in combined_results:
            print(f"- {result.segment.func_desc} (Score: {result.similarity_score:.3f})")

    except Exception as e:
        print(f"Error occurred during processing: {str(e)}")

if __name__ == "__main__":
    main() 
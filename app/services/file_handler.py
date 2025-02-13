from typing import Optional, Dict, Any
import mimetypes
import os
from PIL import Image
import io
import logging

class FileHandler:
    SUPPORTED_EXTENSIONS = {
        'image': ['.jpg', '.jpeg', '.png', '.gif', '.webp'],
        'document': ['.pdf', '.txt', '.doc', '.docx'],
        'spreadsheet': ['.xlsx', '.csv'],
    }

    @staticmethod
    def process_file(file_content: bytes, mime_type: str) -> Optional[Dict[str, Any]]:
        """Process file content and return processed data"""
        try:
            file_type = mime_type.split('/')[0]
            
            if file_type == 'image':
                return FileHandler._process_image(file_content)
            elif file_type in ['text', 'application']:
                return FileHandler._process_document(file_content)
            
            return None
        except Exception as e:
            logging.error(f"Error processing file: {e}")
            return None

    @staticmethod
    def _process_image(content: bytes) -> Dict[str, Any]:
        """Process image content"""
        try:
            img = Image.open(io.BytesIO(content))
            return {
                'type': 'image',
                'content': content,
                'metadata': {
                    'format': img.format,
                    'size': img.size,
                    'mode': img.mode
                }
            }
        except Exception as e:
            logging.error(f"Error processing image: {e}")
            return None

    @staticmethod
    def _process_document(content: bytes) -> Dict[str, Any]:
        """Process document content"""
        try:
            return {
                'type': 'document',
                'content': content,
                'metadata': {
                    'size': len(content)
                }
            }
        except Exception as e:
            logging.error(f"Error processing document: {e}")
            return None
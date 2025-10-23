from io import BytesIO
from typing import List, Callable, Optional
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from .types import Dimensions

class PDFGenerator:
    @staticmethod
    def generate_from_images(
        image_data_list: List[bytes],
        dimensions: Dimensions,
        progress_callback: Optional[Callable[[int, int], None]] = None
    ) -> bytes:
        buffer = BytesIO()
        c = canvas.Canvas(buffer, pagesize=(dimensions.width, dimensions.height))
        
        total = len(image_data_list)
        for i, img_data in enumerate(image_data_list):
            img_buffer = BytesIO(img_data)
            img_reader = ImageReader(img_buffer)
            c.drawImage(img_reader, 0, 0, width=dimensions.width, height=dimensions.height)
            c.showPage()
            
            if progress_callback:
                progress_callback(i + 1, total)
        
        c.save()
        return buffer.getvalue()
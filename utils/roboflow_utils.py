import cv2
import numpy as np
from roboflow import Roboflow
from config import (
    ROBOFLOW_API_KEY,
    ROBOFLOW_WORKSPACE,
    ROBOFLOW_PROJECT,
    ROBOFLOW_MODEL_VERSION,
    CONFIDENCE_THRESHOLD
)

class DroughtDetector:
    """Kelas untuk mendeteksi kekeringan pada daun sorgum menggunakan Roboflow"""
    
    def __init__(self):
        """Inisialisasi model Roboflow"""
        try:
            rf = Roboflow(api_key=ROBOFLOW_API_KEY)
            self.project = rf.workspace(ROBOFLOW_WORKSPACE).project(ROBOFLOW_PROJECT)
            self.model = self.project.version(ROBOFLOW_MODEL_VERSION).model
            print("✅ Model berhasil dimuat dari Roboflow!")
        except Exception as e:
            print(f"❌ Error loading model: {str(e)}")
            self.model = None
    
    def predict(self, image_path):
        """
        Melakukan prediksi pada gambar
        
        Args:
            image_path (str): Path ke gambar atau URL
            
        Returns:
            dict: Hasil prediksi dengan deteksi dan confidence score
        """
        try:
            results = self.model.predict(image_path, confidence=CONFIDENCE_THRESHOLD)
            predictions = results.json()
            
            return {
                'success': True,
                'predictions': predictions,
                'raw_results': results
            }
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'predictions': None
            }
    
    def detect_drought_severity(self, predictions):
        """
        Menganalisis tingkat keparahan kekeringan
        
        Args:
            predictions (dict): Hasil prediksi dari model
            
        Returns:
            dict: Analisis keparahan kekeringan
        """
        if not predictions or 'predictions' not in predictions:
            return {'severity': 'Unknown', 'confidence': 0}
        
        preds = predictions['predictions'].get('predictions', [])
        
        if not preds:
            return {
                'severity': 'Sehat',
                'confidence': 100,
                'message': 'Tidak ada tanda kekeringan terdeteksi'
            }
        
        avg_confidence = np.mean([p.get('confidence', 0) for p in preds])
        
        if avg_confidence < 0.3:
            severity = 'Ringan'
        elif avg_confidence < 0.6:
            severity = 'Sedang'
        else:
            severity = 'Parah'
        
        return {
            'severity': severity,
            'confidence': round(avg_confidence * 100, 2),
            'detection_count': len(preds),
            'message': f'Terdeteksi {len(preds)} area dengan potensi kekeringan'
        }

def load_image(image_file):
    """Load gambar dari bytes"""
    return cv2.imdecode(np.frombuffer(image_file.read(), np.uint8), cv2.IMREAD_COLOR)
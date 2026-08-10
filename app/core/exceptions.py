"""Custom Application Exceptions."""


class MedicalAIException(Exception):
    """Base exception for CarePath AI platform."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class OCRExtractionError(MedicalAIException):
    """Raised when OCR document parsing fails."""
    pass


class DICOMProcessingError(MedicalAIException):
    """Raised when DICOM parsing or image analysis fails."""
    pass


class BioNERException(MedicalAIException):
    """Raised when entity extraction fails."""
    pass


class RAGRetrievalError(MedicalAIException):
    """Raised when vector database search fails."""
    pass

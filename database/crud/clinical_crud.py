from typing import Optional, Any
from sqlalchemy.orm import Session
from database.models import Visit, SymptomSession, PatientSymptom, Medication, MedicalFile
from database.crud.utils import create_record, get_record, update_record

def create_visit(session: Session, **kwargs) -> Visit:
    """Creates a new visit record."""
    return create_record(session, Visit, **kwargs)

def get_visit(session: Session, visit_id: Any) -> Optional[Visit]:
    """Retrieves a visit by visit_id."""
    return get_record(session, Visit, visit_id)

def create_session(session: Session, **kwargs) -> SymptomSession:
    """Creates a new symptom session."""
    return create_record(session, SymptomSession, **kwargs)

def create_symptom(session: Session, **kwargs) -> PatientSymptom:
    """Creates a patient symptom record."""
    return create_record(session, PatientSymptom, **kwargs)

def create_medication(session: Session, **kwargs) -> Medication:
    """Creates a medication record."""
    return create_record(session, Medication, **kwargs)

def create_medical_file(session: Session, **kwargs) -> MedicalFile:
    """Creates a metadata record for an uploaded medical file."""
    return create_record(session, MedicalFile, **kwargs)

def update_analysis_status(session: Session, file_id: Any, status: str) -> Optional[MedicalFile]:
    """Updates the analysis status of a specific medical file."""
    return update_record(session, MedicalFile, file_id, analysis_status=status)

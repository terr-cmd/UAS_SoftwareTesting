from dataclasses import dataclass
from typing import Optional


@dataclass
class Student:
    name: str
    nilai_tugas: float
    nilai_uts: float
    nilai_uas: float
    id: Optional[int] = None
    nilai_akhir: Optional[float] = None
    grade: Optional[str] = None


class ValidationError(Exception):
    pass
    

class StudentNotFoundError(Exception):
    pass

"""Reusable helpers for summarizing clinic systolic readings."""


def systolic_readings(encounters):
    """returns the systolic reading from each instance"""
    sys_readings = []

    for encounter in encounters:
        sys_readings.append(encounter[2])

    return sys_readings


def mean_systolic(readings):
    """returns the mean and None if not in readings"""
    if not readings:
        return None

    return sum(readings) / len(readings)


def count_patients(encounters):
    """Return the number of distinct patient IDs in the encounters."""
    patient_ids = set()

    for encounter in encounters:
        patient_ids.add(encounter[0])

    return len(patient_ids)


def patients_at_or_above(encounters, cutoff):
    """Return patient IDs with a systolic reading at or above the cutoff."""
    patients = set()

    for encounter in encounters:
        if encounter[2] >= cutoff:
            patients.add(encounter[0])

    return patients
    

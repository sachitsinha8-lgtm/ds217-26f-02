#!/usr/bin/env python3
"""Summarize one week of clinic encounters and save the two report files."""

from pathlib import Path

from vitals_tools import (
    count_patients,
    mean_systolic,
    patients_at_or_above,
    systolic_readings,
)


DATA_PATH = Path("data") / "clinic_encounters.csv"
OUTPUT_DIR = Path("output")


def read_encounters(data_path):
    """Return usable encounters and the number of skipped data rows."""

    encounters = []
    skipped = 0

    lines = data_path.read_text().splitlines()

    for line in lines[1:]:
        if not line.strip():
            skipped += 1
            print("Skipping a blank row")
            continue

        fields = line.split(",")

        if len(fields) != 3:
            skipped += 1
            print("Skipping row with wrong number of fields:", line)
            continue

        patient_id, visit_date, systolic_text = fields

        try:
            systolic = int(systolic_text)
        except ValueError:
            skipped += 1
            print("Skipping row with non-integer systolic:", line)
            continue

        if systolic < 60 or systolic > 250:
            skipped += 1
            print("Skipping row with implausible systolic:", line)
            continue

        encounters.append((patient_id, visit_date, systolic))

    return encounters, skipped


def main():
    """Write the vitals summary report and make patient follow-up list."""
    encounters, skipped = read_encounters(DATA_PATH)

    readings = systolic_readings(encounters)
    mean = mean_systolic(readings)
    patients = count_patients(encounters)

    report_lines = [
        f"Usable encounters: {len(encounters)}",
        f"Skipped rows: {skipped}",
        f"Patients seen: {patients}",
        f"Mean systolic: {mean:.1f} mmHg",
        f"Highest systolic: {max(readings)} mmHg",
        f"Lowest systolic: {min(readings)} mmHg",
    ]

    OUTPUT_DIR.mkdir(exist_ok=True)

    report_path = OUTPUT_DIR / "vitals_report.txt"
    report_path.write_text("\n".join(report_lines) + "\n")


    print(report_path.read_text())
    
    cutoff = 155
    reason = "I chose 155 mmHg to prioritize patients with higher systolic readings for the limited follow-up capacity and since they are more urgent."

    followup_patients = patients_at_or_above(encounters, cutoff)

    followup_lines = [
        f"Cutoff: {cutoff} mmHg",
        f"Reason: {reason}",
    ]

    followup_lines.extend(sorted(followup_patients))

    followup_path = OUTPUT_DIR / "followup_list.txt"
    followup_path.write_text("\n".join(followup_lines) + "\n")


if __name__ == "__main__":
    main()

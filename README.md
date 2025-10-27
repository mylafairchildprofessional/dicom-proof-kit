# DICOM / PACS Proof Kit — Tutorial Sandbox

A tiny, local sandbox to practice **RIS → MWL → Modality → PACS** with Orthanc (PACS), a minimal RIS API, and DCMTK tools.

## Services (via Docker)
- **Orthanc (PACS)**: DICOM `:4242`, Web/DICOMweb `:8042`, MWL `:10500`
- **RIS API (Flask)**: `POST /orders` writes MWL JSON files into Orthanc's worklist folder
- **Mirth (optional)**: NextGen Connect on `:8081` (no channels preloaded)

---

## Prereqs
- Docker (with either `docker compose` **or** `docker-compose`)
- DCMTK tools (`echoscu`, `findscu`, `storescu`)
- Python 3.10+ (to generate a test DICOM with pydicom/Pillow)

Ubuntu tips:
```bash
sudo apt-get install -y dcmtk python3-venv

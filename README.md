cat > README.md <<'EOF'
# DICOM / PACS Proof Kit

This repository demonstrates a fully functional local Picture Archiving and Communication System (PACS) environment built using Orthanc (open-source PACS) and DCMTK command-line tools.  
It provides hands-on evidence of DICOM protocol proficiency, including connectivity testing, image transmission, and study verification through a PACS web interface.

---

## Overview

The goal of this proof kit is to validate end-to-end understanding of DICOM networking and PACS workflows.  
The setup mirrors a simplified hospital imaging environment, with Orthanc acting as the PACS server and DCMTK tools acting as the modality or imaging workstation.

---

## Components

- **Orthanc** – lightweight open-source PACS running in Docker  
  - DICOM port: 4242  
  - Web interface: 8042  
- **DCMTK** – suite of DICOM command-line tools used for testing  
  - Tools used: `echoscu`, `storescu`, `findscu`, `img2dcm`, `dcmdump`  
- **Environment** – Linux workstation with Docker and DCMTK installed

---

## Demonstrated Capabilities

| Function | Description | Proof |
|-----------|--------------|-------|
| **C-ECHO** | Verification of DICOM connectivity (Association Accepted / Success) | Terminal output (`echoscu`) |
| **C-STORE** | Transmission of DICOM object to PACS | Terminal output (`storescu`) |
| **Web Viewer** | Verification of stored study in Orthanc Explorer | Screenshot showing patient DOE^JANE |
| **C-FIND (optional)** | Querying PACS for existing studies | `findscu` query results |

---

## Commands Used

```bash
# Launch Orthanc (Docker)
sudo docker run -d -p 8042:8042 -p 4242:4242 \
  -e ORTHANC__AuthenticationEnabled=false \
  --name orthanc orthancteam/orthanc

# Connectivity test (C-ECHO)
echoscu -v -aec ORTHANC localhost 4242

# Create and send DICOM file
img2dcm demo.jpg demo_uncompressed.dcm
storescu -v -aec ORTHANC localhost 4242 demo_uncompressed.dcm

# Optional: Query studies
findscu -v -S -aec ORTHANC localhost 4242 -k QueryRetrieveLevel=STUDY -k PatientName=DOE*


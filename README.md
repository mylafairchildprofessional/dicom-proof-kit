
# DICOM / PACS Proof Kit — Tutorial Sandbox

A tiny, local sandbox to practice a real imaging workflow:  
**RIS → MWL (worklist) → Modality → PACS** using open-source tools.

- **Orthanc (PACS)** — stores and serves studies  
- **RIS API (Flask)** — creates Modality Worklist items from simple JSON orders  
- **Docker Compose** — one command to run everything  
- **DCMTK tools** — C-ECHO, C-FIND (MWL), C-STORE for hands-on learning  

---

## What you’ll learn

- How a RIS places an order and a **Modality Worklist (MWL)** is created  
- How a modality queries MWL and sends images to a **PACS**  
- How to test DICOM connectivity (**C-ECHO**), query (**C-FIND**), and send (**C-STORE**)  
- Basics of **DICOMweb** via Orthanc  

---

## Requirements

- Docker (either `docker compose` **or** legacy `docker-compose`)  
- DCMTK tools: `echoscu`, `findscu`, `storescu`  
- Python 3.10+ (to generate a tiny uncompressed test DICOM)  

**Ubuntu tips**
```
sudo apt-get install -y dcmtk python3-venv
```
---

##  Quick Start (copy/paste)

### Start services

From the repo root:
```
docker compose up -d   # or: docker-compose up -d
```

Check they’re up:
```
curl -s http://localhost:8042/system | head -c 200; echo     # Orthanc JSON
curl -i -s http://localhost:5000/orders | head -n 1          # 405 on GET = OK
```

### Place an order → creates an MWL item
This simulates the RIS creating an order.
The RIS API writes a worklist JSON file that Orthanc serves.
```
curl -s -X POST http://localhost:5000/orders \
  -H 'Content-Type: application/json' \
  -d '{"patient_id":"P123","patient_name":"DOE^JANE","accession":"ACC-1001","modality":"CR","study_desc":"XR CHEST"}'
```
#See the MWL file appear:
```ls -l orthanc/worklists/```

### Query the MWL (modality side)
Use DCMTK Worklist C-FIND (-W):
```
findscu -v -W -aec ORTHANC localhost 10500 \
  -k 0008,0050=ACC-1001 \
  -k 0010,0020=P123
```

### Generate a tiny uncompressed DICOM & send to PACS
Create a small test DICOM and C-STORE it to Orthanc.
```
# one-time setup
python3 -m venv .venv && source .venv/bin/activate
pip install pydicom Pillow

# generate the file (writes demo_uncompressed.dcm)
python3 demo-scripts/03_make_dicom.py

#verify listener, then send
echoscu -v -aec ORTHANC localhost 4242
storescu -v -aec ORTHANC localhost 4242 demo_uncompressed.dcm
```
### Verify in Orthanc
Open http://localhost:8042
You should see a study for DOE^JANE
(PatientID P123, Accession ACC-1001, StudyDescription XR CHEST).

### How it works (in plain English)
- RIS API exposes POST /orders.
When you send a simple JSON order, it writes an MWL JSON into orthanc/worklists/.
- Orthanc runs a MWL SCP on port 10500 and serves those worklist items to modalities.
- Using DCMTK, you query MWL (findscu -W), then send a DICOM (storescu) to PACS on port 4242.
- You can explore the study in Orthanc Explorer at 8042, or via DICOMweb.

### Repo layout
graphql
Copy code
.
├─ docker-compose.yml                  # orchestrates services
├─ orthanc/
│  ├─ orthanc.json                     # enables DICOM, DICOMweb, MWL
│  └─ worklists/                       # RIS API drops MWL JSON here
├─ ris-api/
│  ├─ Dockerfile
│  ├─ requirements.txt
│  └─ app.py                           # POST /orders -> <accession>.json
└─ demo-scripts/
   └─ 03_make_dicom.py                 # creates demo_uncompressed.dcm

### Troubleshooting
echoscu connection refused
Orthanc not up yet. Start just Orthanc and check logs:
docker compose up -d orthanc
docker logs --tail=50 orthanc

### MWL query aborts
Use findscu -W (Worklist model), not -S.

### Store fails with JPEG conversion error
Send uncompressed DICOM (the provided script does).

### Permission denied: /run/docker.sock
Add your user to the docker group, then refresh your shell:
sudo usermod -aG docker $USER && newgrp docker

### Clean up
docker compose down -v
docker system prune -f
rm -f demo_uncompressed.dcm

### Why this exists
This sandbox is designed for learners and job-seekers to get real, hands-on practice with DICOM, PACS, MWL, and healthcare interoperability — using only open-source tools and a laptop.

It’s a great way to build skills for Radiology IT, Imaging Informatics, and Integration Engineering roles.

---




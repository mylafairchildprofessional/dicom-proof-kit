from flask import Flask, request, jsonify
import os, uuid, json, datetime as dt

app = Flask(__name__)
WORKLIST_DIR = "/worklists"  # shared volume with Orthanc

def mk_uid():
    return "2.25." + str(uuid.uuid4().int)

@app.post("/orders")
def create_order():
    data = request.get_json(force=True)
    # expected keys: patient_id, patient_name, accession, modality, study_desc
    now = dt.datetime.utcnow().strftime("%Y%m%d%H%M%S")
    mwl = {
      "0008,0050": data["accession"],               # AccessionNumber
      "0010,0010": data["patient_name"],            # PatientName
      "0010,0020": data["patient_id"],              # PatientID
      "0020,000D": mk_uid(),                        # StudyInstanceUID
      "0040,0100": [ {                              # ScheduledProcedureStepSequence
        "0008,0060": data.get("modality","CR"),     # Modality
        "0040,0001": "STATION1",                    # ScheduledStationAETitle
        "0040,0002": now,                           # Scheduled start (UTC yyyymmddHHMMSS)
        "0040,0007": data.get("study_desc","XR CHEST")
      } ]
    }
    os.makedirs(WORKLIST_DIR, exist_ok=True)
    out_path = os.path.join(WORKLIST_DIR, f"{data['accession']}.json")
    with open(out_path, "w") as f:
        json.dump(mwl, f)
    return jsonify({"status":"ok","file": os.path.basename(out_path)})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

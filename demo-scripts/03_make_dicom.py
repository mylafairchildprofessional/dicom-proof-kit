import pydicom as dcm
from pydicom.uid import (ExplicitVRLittleEndian, SecondaryCaptureImageStorage,
                         PYDICOM_IMPLEMENTATION_UID, generate_uid)
from PIL import Image

W,H=128,128
im=Image.new('L',(W,H),200)
pixels=im.tobytes()

file_meta=dcm.Dataset()
file_meta.FileMetaInformationVersion=b"\x00\x01"
file_meta.MediaStorageSOPClassUID=SecondaryCaptureImageStorage
file_meta.MediaStorageSOPInstanceUID=generate_uid()
file_meta.TransferSyntaxUID=ExplicitVRLittleEndian
file_meta.ImplementationClassUID=PYDICOM_IMPLEMENTATION_UID

ds=dcm.Dataset(); ds.file_meta=file_meta
ds.SOPClassUID=file_meta.MediaStorageSOPClassUID
ds.SOPInstanceUID=file_meta.MediaStorageSOPInstanceUID
ds.StudyInstanceUID=generate_uid(); ds.SeriesInstanceUID=generate_uid()
ds.PatientName="DOE^JANE"; ds.PatientID="P123"
ds.AccessionNumber="ACC-1001"; ds.StudyDescription="XR CHEST"; ds.Modality="CR"
ds.SamplesPerPixel=1; ds.PhotometricInterpretation="MONOCHROME2"
ds.Rows=H; ds.Columns=W; ds.BitsAllocated=8; ds.BitsStored=8; ds.HighBit=7
ds.PixelRepresentation=0; ds.PixelData=pixels
dcm.filewriter.dcmwrite("demo_uncompressed.dcm", ds, write_like_original=False)
print("Wrote demo_uncompressed.dcm")

"""Project-wide settings. Change values here, not inside the notebooks."""
from pathlib import Path

SEED = 42

# --- Where things live (Google Drive, mounted in Colab) -----------------
DRIVE_ROOT = Path("/content/drive/MyDrive/PrescriptionScanner")
RAW_DIR = DRIVE_ROOT / "data" / "raw"                 # downloaded datasets
BD_DIR = RAW_DIR / "bd"                               # Doctor's Handwritten Prescription BD (Kaggle)
RX_DIR = RAW_DIR / "rxhandbd"                         # RxHandBD (Mendeley)
SPLITS_CSV = DRIVE_ROOT / "data" / "splits.csv"       # one row per word crop, with its split
CHECKPOINT_DIR = DRIVE_ROOT / "checkpoints"           # resume training from here
RESULTS_DIR = DRIVE_ROOT / "results"                  # metric tables, charts, examples
DEMO_DIR = DRIVE_ROOT / "demo_photos"                 # anonymized real photos (demo only)

# --- Model ----------------------------------------------------------------
BASE_MODEL = "microsoft/trocr-small-handwritten"      # what we fine-tune

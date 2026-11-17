"""Project-wide settings. Change values here, not inside the notebooks."""
from pathlib import Path

SEED = 42

# --- Where things live (Google Drive, mounted in Colab) -----------------
DRIVE_ROOT = Path("/content/drive/MyDrive/PrescriptionScanner")
HF_CACHE_DIR = DRIVE_ROOT / "data" / "hf_cache"       # downloaded datasets/models
ADAPTER_DIR = DRIVE_ROOT / "models" / "qwen25vl-rx-lora"  # fine-tuned LoRA adapter
CHECKPOINT_DIR = DRIVE_ROOT / "checkpoints"            # resume training from here
RESULTS_DIR = DRIVE_ROOT / "results"                   # metric tables, charts, examples
DEMO_DIR = DRIVE_ROOT / "demo_photos"                  # anonymized real photos (demo only)

# --- Data ---------------------------------------------------------------
DATASET_ID = "naazimsnh02/medocr-vision-dataset"

# --- Models ---------------------------------------------------------------
BASE_MODEL = "Qwen/Qwen2.5-VL-3B-Instruct"                        # what we fine-tune
REFERENCE_MODEL = "KushagraWadhwa/medical-prescription-ocr-india"  # comparison only

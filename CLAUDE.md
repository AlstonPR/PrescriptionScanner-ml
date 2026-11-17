# Handwritten Prescription Text Recognition

ML course project. The model takes a photo of a doctor's handwritten prescription and extracts the text, mainly medicine names and dosages.
**Deadline: 7 Dec 2026** (20 days from 17 Nov 2026).
**Deliverables:** a working model, evaluation results, a small demo and a project report.

## How to work with me (the student)
- Explain things in simple language.
- Build in stages. After each stage, list what to check before moving on.
- Give runnable code with comments, and include fallbacks for download failures, running out of GPU memory and Colab disconnects.
- Be honest about accuracy. Never inflate results, and flag data leakage or evaluation mistakes as soon as you see them.
- Remind me that this is an **assistive tool, not a medical decision-maker**. Every output needs human review.

## Constraints
- Free tools only. Training runs on free Google Colab or Kaggle (T4 GPU, 16 GB).
- Everything must run in a Colab notebook.
- Fine-tune pretrained models. Don't train from scratch.
- **English only for now.** Drop or set aside non-English (Bengali or mixed) labels, and record how many were removed.

## Where things run
- **Training, evaluation and anything that needs a GPU run in Colab only, never on the local laptop.** Don't run training, model downloads or dataset downloads locally.
- This folder holds the notebooks and `src/` code, and it's a Git repo pushed to GitHub.
- **Workflow:** edit here → commit and push → in Colab, open the notebook from GitHub (File → Open notebook → GitHub). The first cell `git clone`s (or `git pull`s) the repo so `src/` can be imported.
- Mount Google Drive in Colab and save datasets, checkpoints and results there, so a disconnect doesn't lose work.
- **Never commit** datasets, model checkpoints, real prescription photos or API tokens. `.gitignore` covers these, and big files stay on Drive.
- Before committing a notebook, clear its outputs to keep diffs small and avoid leaking data.

## Pipeline
```
photo → preprocess (OpenCV) → detect words/lines (PaddleOCR or EasyOCR)
      → recognize text (TrOCR-small-handwritten, fine-tuned)
      → correct with fuzzy match against a medicine-name list (rapidfuzz)
      → output text + confidence + "needs review" flag
```

## Datasets
| Dataset | Source | Size |
|---|---|---|
| Doctor's Handwritten Prescription BD | Kaggle `mamun1113/doctors-handwritten-prescription-bd-dataset` | 4,680 word crops, 78 medicine names |
| RxHandBD | Mendeley `dsb5r6vskg` | 5,578 word crops, 1,559 unique labels |
| Real prescription photos | collected by the student | a few, **demo only** |

## Metrics
CER, WER, exact-match accuracy and drug-name accuracy. Compare three setups:
1. Pretrained TrOCR only
2. Fine-tuned
3. Fine-tuned + fuzzy correction

## Evaluation rules (avoid inflated results)
- **Split before doing anything else**, and keep the test set untouched until the final evaluation. Tune on the validation set only.
- **Split by writer/prescription ID** (both datasets have them), not by random word crop. No writer may appear in more than one of train, validation and test. Assert this in code.
- **The correction list must not leak test labels.** Build it from an independent source or from training labels only, and state in the report how it was built.
- Check for duplicate or near-duplicate images across splits, especially if the two datasets overlap.
- Reported metrics are **word-crop recognition only**. The full-photo pipeline (detection + recognition) on real prescriptions is a qualitative demo unless we label those photos.
- Fix random seeds (`seed=42`) and record library versions.

## Real prescription photos
- Use them for the demo and qualitative examples only. **Never train on them.**
- Blur or crop out patient names, phone numbers, addresses and the doctor's registration number before using or sharing them.

## Planned structure
```
ML Prescription prj/
├── CLAUDE.md
├── README.md
├── requirements.txt
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_baseline_pretrained.ipynb
│   ├── 03_finetune_trocr.ipynb
│   ├── 04_correction_and_eval.ipynb
│   └── 05_full_pipeline_demo.ipynb
├── src/                 # shared code imported by the notebooks
│   ├── data.py          # loading, cleaning, splits
│   ├── preprocess.py    # OpenCV image cleanup
│   ├── detect.py        # PaddleOCR/EasyOCR word/line boxes
│   ├── recognize.py     # TrOCR inference
│   ├── correct.py       # rapidfuzz medicine-name correction
│   └── metrics.py       # CER, WER, exact match, drug-name accuracy
├── data/                # not committed; downloaded in Colab
├── demo/                # demo app + anonymized sample photos
└── results/             # metric tables, charts, error examples (saved for the report later)
```

## Schedule (20 days)
| Days | Stage |
|---|---|
| 1–2 | Colab setup, download both datasets, explore and clean labels, make splits |
| 3–4 | Baseline: pretrained TrOCR on the validation set (CER/WER) |
| 5–9 | Fine-tune TrOCR-small, tune on validation, save checkpoints to Drive |
| 10–11 | Medicine-name list + rapidfuzz correction + confidence / "needs review" flag |
| 12 | Final evaluation on the test set: all three setups, error analysis |
| 13–15 | Full pipeline on real photos (preprocess → detect → recognize → correct) + demo |
| 16–20 | Buffer, plus the report (postponed: we'll plan it later) |

## Decisions made
- Writer/prescription IDs exist, so we use a grouped split.
- English labels only for now.
- Training runs in Colab, never on the laptop.
- The report is postponed. Keep saving metrics, charts and error examples to `results/` so it's easy to write later.
- Code reaches Colab through GitHub. Data and checkpoints live on Google Drive.

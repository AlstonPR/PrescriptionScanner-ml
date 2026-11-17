"""Helpers for the medocr-vision-dataset: keep prescription rows, check for leakage.

The dataset mixes prescriptions with lab reports, invoices and forms, and it has
no column saying which is which. We recognise prescriptions by their label
format (`doctor_name: ... medications: ...`). Notebook 01 prints how many rows
match, so check that count against what you see in the pictures.
"""
import hashlib


def is_prescription(text):
    t = str(text)
    return "doctor_name:" in t and "medications:" in t


def prescription_indices(ds_dict):
    """{split: [row numbers]} for rows that look like prescriptions."""
    return {name: [i for i, t in enumerate(ds["text"]) if is_prescription(t)]
            for name, ds in ds_dict.items()}


def image_md5(pil_image):
    """Hash of the decoded pixels, so re-saved copies of one image still match."""
    return hashlib.md5(pil_image.convert("RGB").tobytes()).hexdigest()


def leakage_report(ds_dict, idx_by_split):
    """Count exact duplicate images and identical labels shared between splits.

    Returns {(split_a, split_b): {"images": n, "labels": n}}. Anything above 0 means
    the same prescription (or a template copy of it) is in two splits.
    """
    hashes = {s: {image_md5(ds_dict[s][i]["image"]) for i in idx} for s, idx in idx_by_split.items()}
    labels = {s: {ds_dict[s][i]["text"] for i in idx} for s, idx in idx_by_split.items()}
    names = list(idx_by_split)
    out = {}
    for a in range(len(names)):
        for b in range(a + 1, len(names)):
            x, y = names[a], names[b]
            out[(x, y)] = {"images": len(hashes[x] & hashes[y]), "labels": len(labels[x] & labels[y])}
    return out

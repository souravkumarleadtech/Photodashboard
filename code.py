# app.py
# Streamlit dashboard for browsing local photos
# - Lists villages (folders in D:\patila\Photos)
# - Search for village
# - Show gallery per village
# - No upload functionality

import streamlit as st
from pathlib import Path

# ====== CONFIG ======
PHOTOS_ROOT = Path(r"D:\patila\Photos")  # <-- change if needed
ALLOWED_EXTS = {".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".tif", ".tiff"}
RECURSIVE_IN_VILLAGE = False

# ====== HELPERS ======
def is_allowed(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTS

def villages():
    PHOTOS_ROOT.mkdir(parents=True, exist_ok=True)
    return sorted([p for p in PHOTOS_ROOT.iterdir() if p.is_dir() and not p.name.startswith(".")],
                  key=lambda p: p.name.lower())

def list_images(folder: Path):
    if not folder.exists():
        return []
    it = folder.rglob("*") if RECURSIVE_IN_VILLAGE else folder.glob("*")
    imgs = [p for p in it if p.is_file() and p.suffix.lower() in ALLOWED_EXTS]
    return sorted(imgs, key=lambda p: (p.name.lower(), p.stat().st_mtime))

# ====== STREAMLIT UI ======
st.set_page_config(page_title="Photo Dashboard", layout="wide")

st.title("📸 Photo Dashboard")
st.caption(f"Serving photos from: `{PHOTOS_ROOT}`")

# --- Village search ---
search = st.text_input("🔍 Search for a village", "").strip().lower()

all_villages = villages()
if search:
    all_villages = [v for v in all_villages if search in v.name.lower()]

if not all_villages:
    st.warning("No villages found.")
else:
    # Sidebar village selector
    vnames = [v.name for v in all_villages]
    selected = st.sidebar.selectbox("Choose a village", vnames)

    # --- Gallery view ---
    st.header(f"Village: {selected}")
    vdir = PHOTOS_ROOT / selected
    imgs = list_images(vdir)

    if not imgs:
        st.info("No images in this village yet.")
    else:
        cols = st.columns(4)  # 4 images per row
        for i, img in enumerate(imgs):
            with cols[i % 4]:
                st.image(str(img), use_container_width=True, caption=img.name)

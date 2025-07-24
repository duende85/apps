# streamlit_morph.py
import streamlit as st
import numpy as np
from PIL import Image
import cv2
import tempfile
from io import BytesIO

st.set_page_config(page_title="Morphing simple (crossfade)", page_icon="🎬", layout="centered")

st.title("Morphing entre dos imágenes (crossfade)")

# --- Upload ---
col_u1, col_u2 = st.columns(2)
with col_u1:
    file1 = st.file_uploader("Imagen inicial", type=["jpg", "jpeg", "png"], key="img1")
with col_u2:
    file2 = st.file_uploader("Imagen final", type=["jpg", "jpeg", "png"], key="img2")

# --- Parámetros ---
with st.expander("Parámetros"):
    frame_count = st.slider("Número de fotogramas", 30, 600, 250, 10)
    fps = st.slider("FPS", 5, 60, 30, 1)
    auto_size = st.checkbox("Usar tamaño de la primera imagen", True)
    if not auto_size:
        width = st.number_input("Ancho", min_value=64, value=768, step=16)
        height = st.number_input("Alto", min_value=64, value=1024, step=16)

# --- Botón ---
generate = st.button("Generar video", disabled=not(file1 or file2))

# --- Lógica ---
if generate:
    if not (file1 and file2):
        st.error("Sube ambas imágenes.")
        st.stop()

    img1 = Image.open(file1).convert("RGB")
    img2 = Image.open(file2).convert("RGB")

    if auto_size:
        base_size = img1.size
    else:
        base_size = (int(width), int(height))

    img1 = img1.resize(base_size, Image.LANCZOS)
    img2 = img2.resize(base_size, Image.LANCZOS)

    img1_np = np.array(img1, dtype=np.float32)
    img2_np = np.array(img2, dtype=np.float32)

    frames = []
    progress = st.progress(0.0)
    for i in range(frame_count):
        alpha = i / (frame_count - 1)
        blended = cv2.addWeighted(img1_np, 1 - alpha, img2_np, alpha, 0)
        frames.append(np.clip(blended, 0, 255).astype(np.uint8))
        progress.progress((i + 1) / frame_count)

    h, w, _ = frames[0].shape
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')

    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    out = cv2.VideoWriter(tmp.name, fourcc, fps, (w, h))

    for f in frames:
        out.write(cv2.cvtColor(f, cv2.COLOR_RGB2BGR))
    out.release()

    st.success("¡Listo!")
    st.video(tmp.name)
    with open(tmp.name, "rb") as f:
        st.download_button("Descargar MP4", f, "morphing_video.mp4", "video/mp4")

    # Muestra primeras/últimas imágenes
    st.caption("Vista previa de las imágenes usadas:")
    st.image([img1, img2], caption=["Inicial", "Final"], width=300)

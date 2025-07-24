import streamlit as st
import numpy as np
from PIL import Image
import imageio.v2 as imageio
import tempfile

st.set_page_config(page_title="Morphing simple (crossfade)", page_icon="🎬")

st.title("Morphing entre dos imágenes (crossfade)")

# --- Uploads ---
col1, col2 = st.columns(2)
with col1:
    f1 = st.file_uploader("Imagen inicial", type=["jpg", "jpeg", "png"])
with col2:
    f2 = st.file_uploader("Imagen final", type=["jpg", "jpeg", "png"])

with st.expander("Parámetros"):
    frame_count = st.slider("Número de fotogramas", 30, 600, 250, 10)
    fps = st.slider("FPS", 5, 60, 30, 1)
    auto_size = st.checkbox("Usar tamaño de la primera imagen", True)
    if not auto_size:
        width = st.number_input("Ancho", 64, 4000, 768, 16)
        height = st.number_input("Alto", 64, 4000, 1024, 16)

with st.expander("Parámetros"):
    frame_count = st.slider("Número de fotogramas", 30, 600, 250, 10)
    fps = st.slider("FPS", 5, 60, 30, 1)
    auto_size = st.checkbox("Usar tamaño de la primera imagen", True)
    if not auto_size:
        width = st.number_input("Ancho", 64, 4000, 768, 16)
        height = st.number_input("Alto", 64, 4000, 1024, 16)

# Cálculo de duración y despliegue
duracion = frame_count / fps
st.markdown(f"**Duración estimada del video:** {duracion:.1f} segundos")

generate = st.button("Generar video", disabled=not (f1 and f2))

generate = st.button("Generar video", disabled=not (f1 and f2))

if generate:
    if not (f1 and f2):
        st.error("Sube ambas imágenes.")
        st.stop()

    img1 = Image.open(f1).convert("RGB")
    img2 = Image.open(f2).convert("RGB")

    base_size = img1.size if auto_size else (int(width), int(height))
    img1 = img1.resize(base_size, Image.LANCZOS)
    img2 = img2.resize(base_size, Image.LANCZOS)

    img1_np = np.array(img1, dtype=np.float32)
    img2_np = np.array(img2, dtype=np.float32)

    frames = []
    prog = st.progress(0.0)
    for i in range(frame_count):
        alpha = i / (frame_count - 1)
        blended = ((1 - alpha) * img1_np + alpha * img2_np).astype(np.uint8)
        frames.append(blended)
        prog.progress((i + 1) / frame_count)

    # Guardar MP4 con imageio (usa ffmpeg interno)
    tmp = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    with imageio.get_writer(tmp.name, fps=fps, codec="libx264") as writer:
        for fr in frames:
            writer.append_data(fr)

    st.success("¡Listo!")
    st.video(tmp.name)
    with open(tmp.name, "rb") as f:
        st.download_button("Descargar MP4", f, "morphing_video.mp4", "video/mp4")

    st.caption("Vista previa")
    st.image([img1, img2], caption=["Inicial", "Final"], width=260)

import streamlit as st
import numpy as np
from PIL import Image
import imageio.v2 as imageio
import tempfile
import os

st.set_page_config(page_title="Morphing simple (crossfade)", page_icon="🎬")
st.title("Morphing entre dos imágenes (crossfade) con audio opcional")

# --- Subida de imágenes ---
col1, col2 = st.columns(2)
with col1:
    f1 = st.file_uploader("Imagen inicial", type=["jpg", "jpeg", "png"])
with col2:
    f2 = st.file_uploader("Imagen final", type=["jpg", "jpeg", "png"])

# --- Subida de audio / YouTube ---
with st.expander("Audio / Música (opcional)"):
    audio_file = st.file_uploader("Sube un archivo de audio (mp3, wav)", type=["mp3", "wav"])
    youtube_url = st.text_input("O pega un link de YouTube para extraer audio")
    st.caption("Nota: la extracción de YouTube requiere pytube; la mezcla de audio requiere moviepy.")

# --- Parámetros de morphing ---
with st.expander("Parámetros de video"):
    frame_count = st.slider("Número de fotogramas", 30, 600, 250, 10)
    fps = st.slider("FPS", 5, 60, 30, 1)
    auto_size = st.checkbox("Usar tamaño de la primera imagen", True)
    if not auto_size:
        width = st.number_input("Ancho", 64, 4000, 768, 16)
        height = st.number_input("Alto", 64, 4000, 1024, 16)

generate = st.button("Generar video", disabled=not (f1 and f2))

def download_audio_from_youtube(url, output_path):
    from pytube import YouTube
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    temp_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    audio_stream.download(output_path=os.path.dirname(temp_file), filename=os.path.basename(temp_file))
    from moviepy.editor import AudioFileClip
    clip = AudioFileClip(temp_file)
    clip.write_audiofile(output_path)
    clip.close()
    os.remove(temp_file)
    return output_path

if generate:
    # Validación básica
    if not (f1 and f2):
        st.error("Sube ambas imágenes.")
        st.stop()

    # Carga y ajuste de tamaño
    img1 = Image.open(f1).convert("RGB")
    img2 = Image.open(f2).convert("RGB")
    base_size = img1.size if auto_size else (int(width), int(height))
    img1 = img1.resize(base_size, Image.LANCZOS)
    img2 = img2.resize(base_size, Image.LANCZOS)

    # Prepara arrays
    arr1 = np.array(img1, dtype=np.float32)
    arr2 = np.array(img2, dtype=np.float32)

    # Genera frames
    frames = []
    prog = st.progress(0)
    for i in range(frame_count):
        alpha = i / (frame_count - 1) if frame_count > 1 else 1
        blended = ((1 - alpha) * arr1 + alpha * arr2).astype(np.uint8)
        frames.append(blended)
        prog.progress((i + 1) / frame_count)

    # Guarda video sin audio
    tmp_vid = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    with imageio.get_writer(tmp_vid.name, fps=fps, codec="libx264") as writer:
        for fr in frames:
            writer.append_data(fr)
    final_video = tmp_vid.name

    # Procesa audio si se subió un archivo o URL
    if audio_file or youtube_url:
        try:
            st.info("Procesando audio…")
            # Descarga o usa archivo
            tmp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
            if youtube_url:
                tmp_audio = download_audio_from_youtube(youtube_url, tmp_audio)
            else:
                with open(tmp_audio, 'wb') as out:
                    out.write(audio_file.read())

            # Combina con MoviePy
            from moviepy.editor import VideoFileClip, AudioFileClip
            video_clip = VideoFileClip(final_video)
            audio_clip = AudioFileClip(tmp_audio).subclip(0, video_clip.duration)
            video_with_audio = video_clip.set_audio(audio_clip)
            tmp_out = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
            video_with_audio.write_videofile(tmp_out.name, codec="libx264", audio_codec="aac")
            final_video = tmp_out.name
        except Exception as e:
            st.warning(f"No se pudo procesar audio; se generará video sin sonido. (Error: {e})")

    # Mostrar y ofrecer descarga
    st.success("¡Listo!")
    st.video(final_video)
    with open(final_video, "rb") as f:
        st.download_button("Descargar MP4", f, "morph_con_audio.mp4", "video/mp4")

    # Preview de imágenes
    st.caption("Vista previa de las imágenes inicial y final")
    st.image([img1, img2], caption=["Inicial", "Final"], width=260)

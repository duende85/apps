import streamlit as st
import numpy as np
from PIL import Image
import imageio.v2 as imageio
import tempfile
import os

# -- Optional audio/video merging libraries --
import moviepy.editor as mpe
from pytube import YouTube

st.set_page_config(page_title="Morphing simple (crossfade)", page_icon="🎬")

st.title("Morphing entre dos imágenes (crossfade) con audio opcional")

# --- Uploads ---
col1, col2 = st.columns(2)
with col1:
    f1 = st.file_uploader("Imagen inicial", type=["jpg", "jpeg", "png"])
with col2:
    f2 = st.file_uploader("Imagen final", type=["jpg", "jpeg", "png"])

# --- Audio options ---
with st.expander("Audio / Música (opcional)"):
    audio_file = st.file_uploader("Sube un archivo de audio (mp3, wav)", type=["mp3", "wav"])
    youtube_url = st.text_input("O pega un link de YouTube para extraer audio")

# --- Morph parameters ---
with st.expander("Parámetros de video"):
    frame_count = st.slider("Número de fotogramas", 30, 600, 250, 10)
    fps = st.slider("FPS", 5, 60, 30, 1)
    auto_size = st.checkbox("Usar tamaño de la primera imagen", True)
    if not auto_size:
        width = st.number_input("Ancho", 64, 4000, 768, 16)
        height = st.number_input("Alto", 64, 4000, 1024, 16)

generate = st.button("Generar video", disabled=not (f1 and f2))


def download_audio_from_youtube(youtube_url, output_path):
    """
    Descarga la pista de audio de YouTube y la guarda como MP3
    """
    yt = YouTube(youtube_url)
    audio_stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    # Download to temporary file
    temp_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    audio_stream.download(output_path=os.path.dirname(temp_path), filename=os.path.basename(temp_path))
    # Convert a clip to MP3
    clip = mpe.AudioFileClip(temp_path)
    clip.write_audiofile(output_path)
    clip.close()
    os.remove(temp_path)
    return output_path

if generate:
    if not (f1 and f2):
        st.error("Sube ambas imágenes.")
        st.stop()

    # Load and resize images
    img1 = Image.open(f1).convert("RGB")
    img2 = Image.open(f2).convert("RGB")
    base_size = img1.size if auto_size else (int(width), int(height))
    img1 = img1.resize(base_size, Image.LANCZOS)
    img2 = img2.resize(base_size, Image.LANCZOS)

    img1_np = np.array(img1, dtype=np.float32)
    img2_np = np.array(img2, dtype=np.float32)

    # Create frames
    frames = []
    prog = st.progress(0.0)
    for i in range(frame_count):
        alpha = i / (frame_count - 1)
        blended = ((1 - alpha) * img1_np + alpha * img2_np).astype(np.uint8)
        frames.append(blended)
        prog.progress((i + 1) / frame_count)

    # Save silent video
    tmp_video = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
    with imageio.get_writer(tmp_video.name, fps=fps, codec="libx264") as writer:
        for fr in frames:
            writer.append_data(fr)

    final_video_path = tmp_video.name

    # If audio provided, merge
    if audio_file or youtube_url:
        st.info("Agregando pista de audio…")
        # Prepare audio file
        tmp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
        if youtube_url:
            try:
                tmp_audio = download_audio_from_youtube(youtube_url, tmp_audio)
            except Exception as e:
                st.error(f"Error descargando audio de YouTube: {e}")
                st.stop()
        else:
            # Save uploaded audio
            with open(tmp_audio, 'wb') as out:
                out.write(audio_file.read())

        # Combine video + audio via MoviePy
        video_clip = mpe.VideoFileClip(final_video_path)
        audio_clip = mpe.AudioFileClip(tmp_audio).subclip(0, video_clip.duration)
        video_with_audio = video_clip.set_audio(audio_clip)
        tmp_out = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False)
        video_with_audio.write_videofile(tmp_out.name, codec="libx264", audio_codec="aac")
        final_video_path = tmp_out.name

    st.success("¡Listo!")
    # Mostrar y ofrecer descarga
    st.video(final_video_path)
    with open(final_video_path, "rb") as f:
        st.download_button("Descargar MP4", f, "morph_con_audio.mp4", "video/mp4")

    st.caption("Vista previa de las imágenes inicial y final")
    st.image([img1, img2], caption=["Inicial", "Final"], width=260)

import streamlit as st
import numpy as np
from PIL import Image
import imageio
import tempfile
import os

st.set_page_config(page_title="Morphing simple (crossfade)", page_icon="🎬")
st.title("Morphing entre dos imágenes (crossfade) con audio opcional")

col1, col2 = st.columns(2)
with col1:
    img1_file = st.file_uploader("Imagen inicial", type=["jpg", "jpeg", "png"])
with col2:
    img2_file = st.file_uploader("Imagen final", type=["jpg", "jpeg", "png"])

with st.expander("Audio (opcional)"):
    audio_file = st.file_uploader("Archivo de audio (mp3, wav)", type=["mp3", "wav"])
    youtube_url = st.text_input("O pega un link de YouTube (requiere pytube)")
    st.caption("La mezcla de audio requiere moviepy. YouTube requiere pytube.")

with st.expander("Parámetros de video"):
    frame_count = st.slider("Número de fotogramas", 30, 600, 250, 10)
    fps = st.slider("FPS", 5, 60, 30, 1)
    auto_size = st.checkbox("Usar tamaño de la primera imagen", True)
    if not auto_size:
        width = st.number_input("Ancho", 64, 4000, 768, 16)
        height = st.number_input("Alto", 64, 4000, 1024, 16)

generate = st.button("Generar video", disabled=not (img1_file and img2_file))

def download_youtube_audio(url, output_path):
    from pytube import YouTube
    from moviepy.editor import AudioFileClip
    yt = YouTube(url)
    stream = yt.streams.filter(only_audio=True).order_by('abr').desc().first()
    temp_mp4 = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
    stream.download(output_path=os.path.dirname(temp_mp4), filename=os.path.basename(temp_mp4))
    clip = AudioFileClip(temp_mp4)
    clip.write_audiofile(output_path)
    clip.close()
    os.remove(temp_mp4)
    return output_path

if generate:
    try:
        img1 = Image.open(img1_file).convert("RGB")
        img2 = Image.open(img2_file).convert("RGB")
        target_size = img1.size if auto_size else (int(width), int(height))
        img1 = img1.resize(target_size, Image.LANCZOS)
        img2 = img2.resize(target_size, Image.LANCZOS)

        arr1, arr2 = np.array(img1, float), np.array(img2, float)
        frames = []
        prog = st.progress(0.0)
        for i in range(frame_count):
            alpha = i/(frame_count-1) if frame_count > 1 else 1
            frame = ((1-alpha)*arr1 + alpha*arr2).astype(np.uint8)
            frames.append(frame)
            prog.progress((i+1)/frame_count)

        tmp_vid = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
        with imageio.get_writer(tmp_vid, fps=fps, codec="libx264") as writer:
            for fr in frames:
                writer.append_data(fr)
        final_path = tmp_vid

    except Exception as e:
        st.error(f"Error al generar video: {e}") 
        st.stop()

    # Audio
    if audio_file or youtube_url:
        try:
            from moviepy.editor import VideoFileClip, AudioFileClip
            if youtube_url:
                tmp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
                tmp_audio = download_youtube_audio(youtube_url, tmp_audio)
            else:
                tmp_audio = tempfile.NamedTemporaryFile(suffix=".mp3", delete=False).name
                with open(tmp_audio, 'wb') as af:
                    af.write(audio_file.read())
            video_clip = VideoFileClip(final_path)
            audio_clip = AudioFileClip(tmp_audio).subclip(0, video_clip.duration)
            merged = video_clip.set_audio(audio_clip)
            out_file = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
            merged.write_videofile(out_file, codec="libx264", audio_codec="aac")
            final_path = out_file
        except Exception as e:
            st.warning(f"No se pudo procesar audio, se entrega video sin sonido. (Error: {e})")

    st.success("¡Video generado!")
    st.video(final_path)
    with open(final_path, 'rb') as vf:
        st.download_button("Descargar video", vf, "morphing.mp4", "video/mp4")
    st.caption("Imágenes inicial y final:")
    st.image([img1, img2], width=240, caption=["Inicial", "Final"])

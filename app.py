import os
import streamlit as st
from downloader import YouTubeDownloader

# -------------------------------
# Streamlit Page Config
# -------------------------------
st.set_page_config(
    page_title="YouTube Downloader Pro",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# -------------------------------
# Custom CSS
# -------------------------------
st.markdown("""
<style>

.stApp{
    background:#0E1117;
    color:white;
}

.main-title{
    font-size:38px;
    font-weight:bold;
    text-align:center;
    color:#FF4B4B;
}

.subtitle{
    text-align:center;
    color:#BBBBBB;
    margin-bottom:25px;
}

.card{
    background:#161B22;
    padding:18px;
    border-radius:15px;
    border:1px solid #30363D;
}

.footer{
    text-align:center;
    color:gray;
    margin-top:40px;
}

</style>
""", unsafe_allow_html=True)

# -------------------------------
# Title
# -------------------------------
st.markdown(
    '<p class="main-title">🎬 YouTube Downloader Pro</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Download YouTube Videos & MP3 in High Quality</p>',
    unsafe_allow_html=True
)

# -------------------------------
# Downloader Object
# -------------------------------
downloader = YouTubeDownloader()

# -------------------------------
# Session State
# -------------------------------
if "video_info" not in st.session_state:
    st.session_state.video_info = None

if "url" not in st.session_state:
    st.session_state.url = ""

# -------------------------------
# URL Input
# -------------------------------
url = st.text_input(
    "Paste YouTube URL",
    value=st.session_state.url,
    placeholder="https://youtube.com/watch?v=..."
)

# -------------------------------
# Fetch Button
# -------------------------------
if st.button("🔍 Get Video Information"):

    if not url.strip():
        st.warning("Please enter a valid YouTube URL.")

    else:

        with st.spinner("Fetching video information..."):

            try:

                info = downloader.get_video_info(url)

                st.session_state.video_info = info
                st.session_state.url = url

            except Exception as e:

                st.error(str(e))
                # -------------------------------
# Show Video Information
# -------------------------------

if st.session_state.video_info:

    info = st.session_state.video_info

    st.markdown("---")

    if info.get("thumbnail"):
        st.image(info["thumbnail"], use_container_width=True)

    st.markdown(f"## 🎬 {info['title']}")

    col1, col2 = st.columns(2)

    with col1:
        st.write("👤 **Uploader**")
        st.success(info["uploader"])

        st.write("⏱️ **Duration**")
        st.success(info["duration"])

    with col2:
        st.write("👁️ **Views**")
        st.success(f"{info['views']:,}")

        st.write("👍 **Likes**")
        st.success(str(info["likes"]))

    st.markdown("---")

    # -------------------------------
    # Video Quality Selector
    # -------------------------------

    quality_map = {}

    for fmt in info["formats"]:

        label = f"{fmt['quality']} ({fmt['extension']})"

        quality_map[label] = fmt["format_id"]

    selected_quality = st.selectbox(
        "📂 Select Video Quality",
        list(quality_map.keys())
    )

    st.markdown("")

    audio_quality = st.selectbox(
        "🎵 Audio Quality",
        [
            "128 kbps",
            "192 kbps",
            "320 kbps"
        ]
    )

    st.markdown("---")
    
             # -------------------------------
# Download Buttons
# -------------------------------

col1, col2 = st.columns(2)

with col1:

    if st.button("🎥 Download Video"):

        try:

            with st.spinner("Downloading video..."):

                file_path = downloader.download_video(
                    st.session_state.url,
                    quality_map[selected_quality]
                )

            with open(file_path, "rb") as f:

                st.download_button(
                    label="📥 Save MP4",
                    data=f.read(),
                    file_name=os.path.basename(file_path),
                    mime="video/mp4",
                    use_container_width=True,
                )

            st.success("✅ Video is ready to download!")

        except Exception as e:

            st.error(f"Video Download Failed\n\n{e}")

with col2:

    if st.button("🎵 Download MP3"):

        try:

            with st.spinner("Extracting audio..."):

                file_path = downloader.download_audio(
                    st.session_state.url
                )

            with open(file_path, "rb") as f:

                st.download_button(
                    label="📥 Save MP3",
                    data=f.read(),
                    file_name=os.path.basename(file_path),
                    mime="audio/mpeg",
                    use_container_width=True,
                )

            st.success("✅ MP3 is ready to download!")

        except Exception as e:

            st.error(f"Audio Download Failed\n\n{e}")

# -------------------------------
# Footer
# -------------------------------

st.markdown("---")

st.markdown(
    """
<div class='footer'>
Made with ❤️ using Python • Streamlit • yt-dlp
</div>
""",
    unsafe_allow_html=True,
        )   

import streamlit as st
from PIL import Image
import io
import os

st.set_page_config(
    page_title="Smart Poster Branding Tool",
    layout="wide"
)

st.title("🎨 Smart Poster Branding Tool")

st.write(
    "Upload a poster and optionally upload your own banner."
)

# Upload Poster
poster_file = st.file_uploader(
    "📤 Upload Poster",
    type=["png", "jpg", "jpeg"]
)

# Upload Custom Banner
banner_file = st.file_uploader(
    "📤 Upload Custom Banner (Optional)",
    type=["png", "jpg", "jpeg"]
)

if poster_file:

    poster = Image.open(poster_file).convert("RGB")

    # Banner Selection
    if banner_file:
        banner = Image.open(banner_file).convert("RGB")
        banner_name = "Custom Banner"
    else:
        banner = Image.open("banner.jpeg").convert("RGB")
        banner_name = "Default Banner"

    st.subheader("Preview")

    col1, col2 = st.columns(2)

    with col1:
        st.image(
            poster,
            caption="Poster",
            use_container_width=True
        )

    with col2:
        st.image(
            banner,
            caption=banner_name,
            use_container_width=True
        )

    if st.button("🚀 Generate Final Poster"):

        # Resize Banner
        poster_width = poster.width

        ratio = poster_width / banner.width

        banner_height = int(
            banner.height * ratio
        )

        banner = banner.resize(
            (poster_width, banner_height),
            Image.LANCZOS
        )

        # Final Image Size
        final_height = (
            poster.height +
            banner.height
        )

        final_image = Image.new(
            "RGB",
            (
                poster.width,
                final_height
            ),
            "white"
        )

        # Paste Poster
        final_image.paste(
            poster,
            (0, 0)
        )

        # Paste Banner
        final_image.paste(
            banner,
            (
                0,
                poster.height
            )
        )

        st.success(
            "✅ Poster Generated Successfully!"
        )

        st.image(
            final_image,
            caption="Final Poster",
            use_container_width=True
        )

        buffer = io.BytesIO()

        final_image.save(
            buffer,
            format="JPEG",
            quality=95
        )

        st.download_button(
            label="📥 Download Final Poster",
            data=buffer.getvalue(),
            file_name="final_poster.jpg",
            mime="image/jpeg"
        )

import streamlit as st
from PIL import Image, ImageStat
import io

st.set_page_config(
    page_title="Smart Poster Branding Tool",
    layout="wide"
)

st.title("🎨 Smart Poster Branding Tool")

st.write(
    "Upload your poster. The footer banner will be added automatically."
)

# Upload poster only
poster_file = st.file_uploader(
    "Upload Poster",
    type=["png", "jpg", "jpeg"]
)

if poster_file:

    # Load poster
    poster = Image.open(poster_file).convert("RGB")

    # Load permanent banner
    banner = Image.open("banner.jpg").convert("RGB")

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
            caption="Permanent Footer Banner",
            use_container_width=True
        )

    if st.button("Generate Final Poster"):

        # Resize banner according to poster width
        poster_width = poster.width

        ratio = poster_width / banner.width
        banner_height = int(
            banner.height * ratio
        )

        banner = banner.resize(
            (poster_width, banner_height),
            Image.LANCZOS
        )

        # Dynamic separator color
        separator_height = 4

        sample_height = min(
            30,
            poster.height
        )

        bottom_part = poster.crop(
            (
                0,
                poster.height - sample_height,
                poster.width,
                poster.height
            )
        )

        stat = ImageStat.Stat(bottom_part)

        avg_color = tuple(
            int(x)
            for x in stat.mean[:3]
        )

        # Create final canvas
        final_height = (
            poster.height
            + separator_height
            + banner.height
        )

        final_image = Image.new(
            "RGB",
            (
                poster.width,
                final_height
            ),
            "white"
        )

        # Paste poster
        final_image.paste(
            poster,
            (0, 0)
        )

        # Color matching separator
        separator = Image.new(
            "RGB",
            (
                poster.width,
                separator_height
            ),
            avg_color
        )

        final_image.paste(
            separator,
            (
                0,
                poster.height
            )
        )

        # Paste banner
        final_image.paste(
            banner,
            (
                0,
                poster.height + separator_height
            )
        )

        st.success(
            "Poster Generated Successfully!"
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
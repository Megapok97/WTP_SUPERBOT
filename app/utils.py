import io

from PIL import Image


def image2bytes_stream(image: Image):
    bytes_stream = io.BytesIO()
    image.save(bytes_stream, format='PNG')
    bytes_stream.seek(0)

    return bytes_stream

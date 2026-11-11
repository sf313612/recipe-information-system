import os
import re
import shutil
import tempfile
from pathlib import Path
from typing import BinaryIO

from PIL import Image, UnidentifiedImageError


PHOTO_STORAGE_DIR = Path(
    os.environ.get(
        "PHOTO_STORAGE_DIR",
        Path(__file__).resolve().parent.parent / "photo_uploads",
    )
)
_SAFE_PHOTO_ID = re.compile(r"^[A-Za-z0-9_-]+$")


class InvalidPhotoError(ValueError):
    """Raised when an uploaded file is empty or cannot be verified as an image."""


def _photo_path(photo_id: str) -> Path:
    if not _SAFE_PHOTO_ID.fullmatch(photo_id):
        raise ValueError("Invalid photo ID")
    return PHOTO_STORAGE_DIR / f"{photo_id}.image"


def _image_media_type(path: Path) -> str:
    Image.init()
    with Image.open(path) as image:
        image_format = image.format
    return _media_type_for_format(image_format)


def _media_type_for_format(image_format: str | None) -> str:
    media_type = Image.MIME.get(image_format) if image_format else None
    if media_type and media_type.startswith("image/"):
        return media_type

    # Pillow can decode formats without a registered MIME mapping. Give those
    # formats a syntactically valid, format-specific image media type instead
    # of claiming that accepted image bytes are arbitrary binary data.
    subtype = re.sub(r"[^a-z0-9.-]", "-", (image_format or "unknown").lower())
    subtype = subtype.strip(".-") or "unknown"
    return f"image/x-pillow-{subtype}"


def store_uploaded_photo(photo_id: str, source: BinaryIO) -> tuple[Path, str]:
    """Validate a staged upload and atomically publish it under its stable photo ID."""
    destination = _photo_path(photo_id)
    PHOTO_STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    file_descriptor, temporary_name = tempfile.mkstemp(
        prefix=".photo-upload-",
        suffix=".tmp",
        dir=PHOTO_STORAGE_DIR,
    )
    temporary_path = Path(temporary_name)

    try:
        with os.fdopen(file_descriptor, "wb") as temporary_file:
            shutil.copyfileobj(source, temporary_file)

        if temporary_path.stat().st_size == 0:
            raise InvalidPhotoError("Uploaded photo is empty")

        try:
            Image.init()
            with Image.open(temporary_path) as image:
                image_format = image.format
                image.verify()
        except (
            UnidentifiedImageError,
            Image.DecompressionBombError,
            OSError,
            SyntaxError,
            ValueError,
        ) as error:
            raise InvalidPhotoError(
                "Uploaded file is not a valid image"
            ) from error

        media_type = _media_type_for_format(image_format)
        os.replace(temporary_path, destination)
        return destination, media_type
    finally:
        temporary_path.unlink(missing_ok=True)


def get_stored_photo(photo_id: str) -> tuple[Path, str] | None:
    path = _photo_path(photo_id)
    if not path.is_file():
        return None
    return path, _image_media_type(path)


def delete_stored_photo(photo_id: str) -> None:
    _photo_path(photo_id).unlink(missing_ok=True)

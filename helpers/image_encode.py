import base64
import httpx
import mimetypes


async def image_to_base64(image_url: str) -> tuple[str, str]:
    mime_type, _ = mimetypes.guess_type(image_url)
    if not mime_type:
        mime_type = "image/png"

    async with httpx.AsyncClient(timeout=10.0) as client:
        response = await client.get(image_url)
    response.raise_for_status()

    content_type = response.headers.get("content-type", "")
    if not content_type.startswith("image/"):
        raise ValueError(f"URL não retornou uma imagem válida (content-type={content_type})")

    image_data = base64.b64encode(response.content).decode("utf-8")
    return image_data, mime_type

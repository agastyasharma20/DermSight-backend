import io
from PIL import Image
from typing import Dict


class VisionAnalyzer:

    def analyze_image_bytes(self, image_bytes: bytes) -> Dict:

        try:
            image = Image.open(io.BytesIO(image_bytes))
        except Exception:
            raise ValueError("Invalid image file.")

        width, height = image.size
        if width < 100 or height < 100:
            raise ValueError("Image resolution too low for reliable analysis.")

        image = image.convert("RGB")

        pixels = list(image.getdata())
        red_pixels = 0
        total_pixels = len(pixels)

        for r, g, b in pixels:
            if r > 150 and r > g + 20 and r > b + 20:
                red_pixels += 1

        redness_ratio = red_pixels / total_pixels if total_pixels > 0 else 0

        return {
            "width": width,
            "height": height,
            "redness_ratio": round(redness_ratio, 3),
            "resolution_quality": self._assess_quality(width, height)
        }

    def _assess_quality(self, width: int, height: int) -> str:
        if width < 300 or height < 300:
            return "Low"
        elif width < 800:
            return "Medium"
        else:
            return "High"

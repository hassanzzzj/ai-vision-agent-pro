"""
SiliconFlow API Service
Image generation ke liye external API calls
"""
import os
import base64
import httpx
from typing import Optional, Dict, Any
from io import BytesIO
from PIL import Image


class SiliconFlowService:
    """SiliconFlow API integration for image generation"""
    
    def __init__(self):
        self.api_key = os.getenv("SILICONFLOW_API_KEY")
        self.base_url = os.getenv(
            "SILICONFLOW_BASE_URL", 
            "https://api.siliconflow.cn/v1/images/generations"
        )
        
        if not self.api_key:
            raise ValueError("SILICONFLOW_API_KEY environment variable not set")
    
    async def generate_image(
        self, 
        prompt: str,
        negative_prompt: Optional[str] = None,
        width: int = 1024,
        height: int = 1024,
        num_inference_steps: int = 30,
        guidance_scale: float = 7.5,
        seed: Optional[int] = None
    ) -> Dict[str, Any]:
        """
        Generate image using SiliconFlow API
        
        Args:
            prompt: Image generation prompt
            negative_prompt: Things to avoid in image
            width: Image width (default: 1024)
            height: Image height (default: 1024)
            num_inference_steps: Generation steps (default: 30)
            guidance_scale: How closely to follow prompt (default: 7.5)
            seed: Random seed for reproducibility
        
        Returns:
            Dict with 'image' (base64) and 'metadata'
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "black-forest-labs/FLUX.1-schnell",
                "prompt": prompt,
                "negative_prompt": negative_prompt or "blurry, low quality, distorted",
                "width": width,
                "height": height,
                "num_inference_steps": num_inference_steps,
                "guidance_scale": guidance_scale,
            }
            
            if seed is not None:
                payload["seed"] = seed
            
            async with httpx.AsyncClient(timeout=120.0) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                )
                response.raise_for_status()
                
                result = response.json()
                
                # Extract base64 image from response
                if "data" in result and len(result["data"]) > 0:
                    image_data = result["data"][0]
                    
                    # Response format: {"b64_json": "..."} or {"url": "..."}
                    if "b64_json" in image_data:
                        return {
                            "image": image_data["b64_json"],
                            "metadata": {
                                "prompt": prompt,
                                "width": width,
                                "height": height,
                                "steps": num_inference_steps,
                                "guidance": guidance_scale
                            }
                        }
                    elif "url" in image_data:
                        # Download from URL and convert to base64
                        image_response = await client.get(image_data["url"])
                        image_response.raise_for_status()
                        
                        # Convert to base64
                        img = Image.open(BytesIO(image_response.content))
                        buffered = BytesIO()
                        img.save(buffered, format="PNG")
                        img_base64 = base64.b64encode(buffered.getvalue()).decode()
                        
                        return {
                            "image": img_base64,
                            "metadata": {
                                "prompt": prompt,
                                "width": width,
                                "height": height,
                                "steps": num_inference_steps,
                                "guidance": guidance_scale
                            }
                        }
                
                raise ValueError("No image data in API response")
                
        except httpx.HTTPStatusError as e:
            raise Exception(f"SiliconFlow API error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            raise Exception(f"Image generation failed: {str(e)}")
    
    def validate_prompt(self, prompt: str) -> bool:
        """Validate if prompt is suitable for image generation"""
        if not prompt or len(prompt.strip()) < 3:
            return False
        
        # Check for inappropriate content (basic check)
        blocked_words = ["nsfw", "explicit", "violent"]
        prompt_lower = prompt.lower()
        
        for word in blocked_words:
            if word in prompt_lower:
                return False
        
        return True


# Global instance
silicon_flow_service = SiliconFlowService()

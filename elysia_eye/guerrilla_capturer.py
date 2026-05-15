import os
import json
import torch
import httpx
from huggingface_hub import hf_hub_url
from safetensors import safe_open
from io import BytesIO

class GuerrillaCapturer:
    """
    Zero-Disk Guerrilla Capturer:
    Intercepts model 'waves' (weights) directly from the network into RAM.
    Bypasses local SSD caching entirely to maintain Hardware Sovereignty.
    """
    def __init__(self, model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        self.model_id = model_id
        self.client = httpx.Client(follow_redirects=True)
        print(f"[Guerrilla Capturer] Target: {model_id}")
        print(f"[Hardware Sovereignty] Mode: Zero-Disk (Streaming Waves)")

    def get_index(self):
        """Fetches the safetensors index if the model is sharded."""
        index_url = hf_hub_url(self.model_id, filename="model.safetensors.index.json")
        try:
            response = self.client.get(index_url)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"Index fetch failed (maybe not sharded): {e}")
        return None

    def fetch_layer_metadata(self, filename="model.safetensors"):
        """
        Fetches only the header of a safetensors file to get weight offsets.
        This is a 'Surgical Strike' on the giant's data.
        """
        url = hf_hub_url(self.model_id, filename=filename)

        # Safetensors header: first 8 bytes indicate header length
        header_len_resp = self.client.get(url, headers={"Range": "bytes=0-7"})
        if header_len_resp.status_code != 206 and header_len_resp.status_code != 200:
            raise ConnectionError(f"Failed to fetch header length for {url}")

        header_size = int.from_bytes(header_len_resp.content, "little")

        # Fetch the actual header
        header_resp = self.client.get(url, headers={"Range": f"bytes=8-{7 + header_size}"})
        header = json.loads(header_resp.content)

        return header, url, header_size + 8

    def stream_layer_weights(self, layer_name_pattern):
        """
        Locates and streams specific weights directly into RAM.
        No local files are created.
        """
        index = self.get_index()

        if index and "weight_map" in index:
            # Find which file contains the requested weights
            target_file = None
            for weight_name, filename in index["weight_map"].items():
                if layer_name_pattern in weight_name:
                    target_file = filename
                    break
            if not target_file:
                raise ValueError(f"Weight pattern '{layer_name_pattern}' not found in index.")
        else:
            target_file = "model.safetensors"

        header, url, total_header_offset = self.fetch_layer_metadata(target_file)

        # Find the specific weight offsets in the header
        target_weight_meta = None
        full_weight_name = None
        for weight_name, meta in header.items():
            if weight_name != "__metadata__" and layer_name_pattern in weight_name:
                target_weight_meta = meta
                full_weight_name = weight_name
                break

        if not target_weight_meta:
             raise ValueError(f"Weight '{layer_name_pattern}' not found in {target_file}.")

        start, end = target_weight_meta["data_offsets"]

        # Fetch only the specific bytes for this weight
        actual_start = total_header_offset + start
        actual_end = total_header_offset + end - 1

        print(f"  -> Guerilla Capture: {full_weight_name} ({actual_end - actual_start + 1} bytes)")
        weight_data_resp = self.client.get(url, headers={"Range": f"bytes={actual_start}-{actual_end}"})

        # Convert to Torch tensor (In-Memory)
        dtype_map = {
            "F16": torch.float16,
            "F32": torch.float32,
            "BF16": torch.bfloat16
        }
        torch_dtype = dtype_map.get(target_weight_meta["dtype"], torch.float32)

        # Load the weight from the byte stream
        # Note: safetensors uses simple byte buffers
        tensor = torch.frombuffer(weight_data_resp.content, dtype=torch_dtype)
        # Reshape if possible (requires shape info from meta)
        if "shape" in target_weight_meta:
            tensor = tensor.view(target_weight_meta["shape"])

        return tensor

if __name__ == "__main__":
    capturer = GuerrillaCapturer()
    # Test capture of a small weight (e.g., embedding or first layer)
    try:
        weight = capturer.stream_layer_weights("model.layers.0.self_attn.q_proj.weight")
        print(f"Captured Weight Shape: {weight.shape}")
        print("Success: Weight captured in RAM with Zero-Disk footprint.")
    except Exception as e:
        print(f"Capture failed: {e}")

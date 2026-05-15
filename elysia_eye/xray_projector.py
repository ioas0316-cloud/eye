import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

class XRayProjector:
    def __init__(self, model_id="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        print(f"Loading model: {model_id}...")
        self.tokenizer = AutoTokenizer.from_pretrained(model_id)
        self.model = AutoModelForCausalLM.from_pretrained(model_id, torch_dtype=torch.float32, device_map="cpu")
        self.model.eval()
        print("Model loaded successfully.")

    def get_attention_weights(self, layer_idx):
        """Extracts attention weights (O projection) from a specific layer."""
        if layer_idx >= len(self.model.model.layers):
            raise ValueError(f"Layer index {layer_idx} out of range.")

        # We focus on the 'o_proj' weights as the 'bone structure' of the attention output
        weights = self.model.model.layers[layer_idx].self_attn.o_proj.weight.data
        return weights

    def get_activations(self, text, layer_idx):
        """Captures activations during inference."""
        inputs = self.tokenizer(text, return_tensors="pt")
        activations = {}

        def hook(module, input, output):
            activations['value'] = output.detach()

        # Hook into the attention output
        handle = self.model.model.layers[layer_idx].self_attn.o_proj.register_forward_hook(hook)

        with torch.no_grad():
            self.model(**inputs)

        handle.remove()
        return activations['value']

if __name__ == "__main__":
    projector = XRayProjector()
    w = projector.get_attention_weights(0)
    print(f"Layer 0 Attention O-proj weights shape: {w.shape}")

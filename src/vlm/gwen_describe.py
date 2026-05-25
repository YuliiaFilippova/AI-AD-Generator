from transformers import Qwen2VLForConditionalGeneration, AutoProcessor
from PIL import Image
import torch
import torchvision
print(torchvision.__version__)

#model_name = "Qwen/Qwen2-VL-7B-Instruct" # This is a much better model! Should work well when run on cuda
model_name = "Qwen/Qwen2-VL-2B-Instruct"

#model = Qwen2VLForConditionalGeneration.from_pretrained(
 #   model_name,
  #  torch_dtype=torch.float16,
   # device_map="auto"
#)

device = "mps" if torch.backends.mps.is_available() else "cpu"

model = Qwen2VLForConditionalGeneration.from_pretrained(
    model_name,
    torch_dtype=torch.float16 if device == "mps" else torch.float32
).to(device)

processor = AutoProcessor.from_pretrained(model_name)
def describe_scene(frame_paths):

    #- Do not guess emotions or intentions
    #- People (include gender if clearly visible)
    #- Visible physical traits (e.g. hair color, clothing, disabilities) if clear

    images = [Image.open(p).convert("RGB") for p in frame_paths]
    prompt = f"""
You are given several keyframes from the same scene. They show how the scene evolves.

Describe the scene for visually impaired viewers.

Focus on:
- People (include gender)
- Main actions
- Main objects
- Written text containing important information
- Consistency (same people, same setting)

Rules:
- Use only clearly visible information.
- Do not mention black background and blurred elements
- Do NOT use words like "appears", "seems", "possibly", "contemplatively", "engaged", etc
- If unsure about a detail, omit it
- If no significant change, omit it
- Use simple, direct language
- Use simple present tense
- Avoid repeating the same information
- Do NOT mention "video", "scene", "frame", "caption", etc

Output:
ONE short English sentence.
"""

    messages = [
        {
            "role": "user",
            "content": [
                *[{"type": "image", "image": img} for img in images],
                {"type": "text", "text": prompt},
            ],
        }
    ]

    text = processor.apply_chat_template(
        messages,
        tokenize=False,
        add_generation_prompt=True
    )

    inputs = processor(
        text=[text],
        images=images,
        return_tensors="pt"
    ).to(model.device)

    output = model.generate(
        **inputs,
        max_new_tokens=100,
        do_sample=False,
        repetition_penalty=1.15,
        no_repeat_ngram_size=3,
        eos_token_id=processor.tokenizer.eos_token_id,
        pad_token_id=processor.tokenizer.eos_token_id,
    )

    generated_ids = output[0][inputs.input_ids.shape[1]:]

    # Decode only the answer
    response = processor.decode(generated_ids, skip_special_tokens=True)

    return response

print(model.device)
print("Using device:", device)
import ollama

def build_global_context(vlm_descriptions):
    all_text = "\n".join(
        f"Scene {i+1}: {d}" for i, d in enumerate(vlm_descriptions)
    )

    prompt = f"""
Extract ONLY stable global context from these raw video descriptions.

Raw descriptions:
{all_text}

Create a very short factual context summary for subtitle generation.

Rules:
- Do NOT tell the story.
- Do NOT describe scene-by-scene events.
- Include only facts that are repeated or strongly supported.
- Omit uncertain details.
- Use short phrases, not full paragraphs.
- Maximum 80 words total.
- Output ONLY the template below.

Template:

Setting: <very short setting>

People:
- <person/group>: <stable appearance>; <main recurring role/action>
- <person/group>: <stable appearance>; <main recurring role/action>

Objects/Text:
- <recurring object or visible text>: <short note>

Main idea:
<one short sentence about the overall situation>
"""
    response = ollama.chat(
        model="qwen2.5:14b",
        messages=[{"role": "user", "content": prompt}],
        options={
            "num_predict": 80,
            "temperature": 0.1,
            "repeat_penalty": 1.2,
        }
    )

    return response["message"]["content"].strip()
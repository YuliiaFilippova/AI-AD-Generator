import ollama

def describe_frame(frame_path):

    prompt = """
    Describe what is clearly visible in these frames from the same video scene. You are doing this for for visually impaired people.

Focus on:
- actions of people (if present)
- important objects and their state
- interactions between people and objects
- scene changes or transitions
- visible emotions (only if clearly expressed)

Rules:
- Include all relevant visible details, but stay concise (2–3 sentences max)
- Describe only observable facts
- Do NOT guess or infer
- Ignore unclear or unimportant background details
- Use short, simple sentences

Avoid:
- speculation ("appears", "might", "suggests")
- inventing emotions or intentions
- long or complex descriptions

Output plain text only.
    """

    response = ollama.chat(
        model="llava",
        messages=[
            {
                "role": "user",
                "content": prompt,
                "images": [frame_path],
            }
        ],
        # maximum number of tokens the model is allowed to generate.
        #options={
    # "temperature": 0.2,
        #    "num_predict":20
        #}
    )

    return response["message"]["content"]

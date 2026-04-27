import ollama


def summarize_scene(descriptions, previous_summary, max_words):

    curr_text = "\n".join(descriptions)
    prompt = f"""
You are writing audio descriptions for a short silent video for visually impaired people.

Previous scene description:
{previous_summary}

Current scene visual information:
{curr_text}

Write ONE short sentence describing only what is NEW in the current scene.

Requirements:
- Do not repeat previous information
- Do not use the word "now", "still", etc
- Be concise and natural (max {max_words} words)
- Do not guess
- Describe only clearly visible information
- Use pronouns for previously introduced people when possible
- Do not mention "image", "video", "frame", "scene", "screenshot", "screen", etc

If there is no meaningful change, output: ""
Output only one sentence.

Example:
Previous: A man enters the room.
Current: The man stands near a table and looks around.
Output: He stands by the table and looks around.
"""

    response = ollama.chat(
        #model="mistral",
        #model="qwen2.5:3b",
        model="llama3.1:8b",
        messages=[
            {"role": "user", "content": prompt}
        ],
        options={
            "num_predict": 30,
            "temperature": 0.2,
            "top_p": 0.9,
            "repeat_penalty": 1.2
        }
    )

    sentence = response["message"]["content"].strip()

    return sentence




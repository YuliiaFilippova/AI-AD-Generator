import ollama
#Semantic context (from metadata):
#{semantic_context}

#Global context:
#{global_context}
#Use global context ONLY to keep people, setting and recurring objects consistent.
#Do not copy actions from global context unless they are also in the CURRENT raw description.

def generate_subtitle(current_description, previous_subtitles, max_words, local_context):

    history = "\n".join(previous_subtitles[-3:])  # last 3 only

    prompt = f"""
You are writing audio descriptions for a video for blind and visually impaired viewers.

CURRENT SCENE:
{current_description}

PREVIOUS SUBTITLES:
{history}
Do not restate these previous facts using different words.

PREVIOUS RAW CONTEXT:
{local_context}
Use this only to keep names/pronouns consistent. Do not copy actions or objects from it.

TASK:
Write ONE short sentence describing ONLY the CURRENT SCENE.

IMPORTANT:
- The CURRENT SCENE is the source of truth.
- Use PREVIOUS SUBTITLES only to avoid repetition.
- Use PREVIOUS RAW CONTEXT only for continuity:
  - same person
  - pronouns
  - stable clothing
- NEVER copy actions or objects from PREVIOUS RAW CONTEXT unless they are visible in CURRENT SCENE.

RULES:
- Preserve important details from CURRENT SCENE.
- DO NOT REPEAT previous subtitles using different wording.
- Do not invent names
- Do not infer things not clearly described.
- Do not mention black background
- Do not add cinematic language.
- Do not describe lighting.
- Do not use words like:
  "appears", "seems", "possibly", "likely", "contemplatively", "engaged".
- Prefer concrete actions and objects.
- Use simple present tense.
- Use English language.
- Use natural pronouns when identity is clear.
- Keep wording natural and concise.
- Include visible text only if important.
- Output ONLY the final sentence.
- Maximum {max_words} words.
"""

    # These two models are much better! Should work well when run on cuda
    #model = "qwen2.5:32b", # ollama pull qwen2.5:32b
    #model = "qwen2.5:72b", # ollama pull qwen2.5:72b
    response = ollama.chat(
        model="qwen2.5:14b",
        messages=[{"role": "user", "content": prompt}],
        options={
            "num_predict": 40,
            "temperature": 0.1,
            "repeat_penalty": 1.3
        }
    )

    return response["message"]["content"].strip()

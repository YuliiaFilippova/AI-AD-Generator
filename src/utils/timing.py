def max_words(start, end):

    duration = end - start

    return max(3, int(duration * 2.5))

# add hard word limit (optional)
# if so, modify summarize_scene by adding:
# sentence = trim_sentence(sentence, max_words)

def trim_sentence(text, max_words):

    words = text.split()

    if len(words) > max_words:
        words = words[:max_words]

    return " ".join(words)

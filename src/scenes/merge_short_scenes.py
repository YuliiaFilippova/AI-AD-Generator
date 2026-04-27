def merge_short_scenes(scenes, min_duration=5.0):

    if not scenes:
        return []

    merged = []
    current_start, current_end = scenes[0]

    for start, end in scenes[1:]:

        duration = current_end - current_start

        if duration < min_duration:
            # extend current scene, merge with next
            current_end = end
        else:
            # save scene and start new one
            merged.append((current_start, current_end))
            current_start, current_end = start, end

    # add final scene
    merged.append((current_start, current_end))

    return merged


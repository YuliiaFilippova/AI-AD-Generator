from datetime import timedelta

def format_time(seconds):

    t = str(timedelta(seconds=seconds))

    if "." not in t:
        t += ".000"

    t = t.split(".")

    ms = t[1][:3]

    return f"{t[0]},{ms}"

#def create_srt(scenes, descriptions):

    with open("data/output/output.srt", "w") as f:

        for i, ((start, end), text) in enumerate(zip(scenes, descriptions), 1):

            f.write(f"{i}\n")
            f.write(f"{format_time(start)} --> {format_time(end)}\n")
            f.write(text.strip() + "\n\n")

def create_srt(scenes, descriptions, output_path):

    with open(output_path, "w") as f:

        for i, ((start, end), text) in enumerate(
            zip(scenes, descriptions), 1
        ):

            f.write(f"{i}\n")
            f.write(
                f"{format_time(start)} --> "
                f"{format_time(end)}\n"
            )
            f.write(text.strip() + "\n\n")

    print(f"SRT saved to: {output_path}")
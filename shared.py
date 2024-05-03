from ffmpeg import FFmpeg, Progress


# https://www.geeksforgeeks.org/break-list-chunks-size-n-python/
def chunks(l, n):
    # looping till length l
    for i in range(0, len(l), n):
        yield l[i:i + n]


def generate_mp3(src, dest, cover, title, track_number, total_number):
    ffmpeg = (
        FFmpeg() .option("y") .input(src) .input(cover) .option("vn") .output(
            dest,
            {
                "map": [
                    "0",
                    "1"],
                "b:a": "64k",
                "id3v2_version": "3",
                "metadata:s:v": [
                    "title=\"Album cover\"",
                    "comment=\"Cover (front)\""],
                "metadata": [
                    "title=" +
                    title,
                    "artist=RAND Corporation",
                    "album=A Million Random Digits with 100,000 Normal Deviates",
                    "TYER=1955",
                    "TCOP=1955 RAND Corporation",
                    "track=" +
                    str(track_number) +
                    "/" +
                    str(total_number)]},
            ar="44100",
            ac="1",
        ))

    @ffmpeg.on("start")
    def on_start(arguments: list[str]):
        print("arguments:", arguments)

    ffmpeg.execute()

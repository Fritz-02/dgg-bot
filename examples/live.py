"""
Example of how to use DGGLive, which gives stream info when stream is live, and the latest youtube videos and vods.
Prints the same text as the !live command message in chat, and youtube video and vod names, url, and stream length if
applicable.
"""
import logging
from datetime import datetime

from dggbot import DGGLive
from dggbot.live import Embed, StreamInfo, YoutubeVideo

logging.basicConfig(level=logging.INFO)
live = DGGLive()


def sec_to_hm(sec: int) -> str:
    hours, rem = divmod(sec, 3600)
    minutes, _ = divmod(rem, 60)
    return f"{hours}h {minutes}m"


@live.event()
def on_streaminfo(streaminfo: StreamInfo):
    if streaminfo.is_live():
        stream = streaminfo.get_livestreams()[0]
        started_at = datetime.strptime(stream.started_at, "%Y-%m-%dT%H:%M:%S+0000")
        started_ago = datetime.utcnow() - started_at
        print(
            f"Viewers: {streaminfo.viewers}. Stream live as of {sec_to_hm(started_ago.seconds)} ago"
        )
    else:
        ended_at = datetime.strptime(
            streaminfo.youtube.ended_at, "%Y-%m-%dT%H:%M:%S+0000"
        )
        last_online = datetime.utcnow() - ended_at
        s = ["Stream was last online"]
        if last_online.days:
            s.append(f"{last_online.days}d")
        s.append(
            f"{sec_to_hm(last_online.seconds)} ago. Time Streamed: {sec_to_hm(streaminfo.youtube.duration)}"
        )
        print(" ".join(s))


@live.event()
def on_stream_start():
    print("Gnomey is live!")


@live.event()
def on_videos(videos: tuple[YoutubeVideo]):
    s = ["Videos:"]
    for video in videos:
        s.append(f"\t{video.title} ({video.url})")
    print("\n".join(s))


@live.event()
def on_youtubevods(vods: tuple):
    s = ["Vods:"]
    for vod in vods:
        start = datetime.strptime(vod.streamStartTime, "%Y-%m-%dT%H:%M:%S+0000")
        end = datetime.strptime(vod.streamEndTime, "%Y-%m-%dT%H:%M:%S+0000")
        duration = end - start
        s.append(
            f"\t{vod.title} ({vod.url}). Streamed for {sec_to_hm(duration.seconds)}"
        )
    print("\n".join(s))


@live.event()
def on_embeds(embeds: list[Embed]):
    for embed in embeds:
        print(f"#{embed.platform}/{embed.id} - {embed.count} viewers")


if __name__ == "__main__":
    live.run_forever()

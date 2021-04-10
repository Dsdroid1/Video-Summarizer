from __future__ import unicode_literals
from django.http.response import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

import argparse
import uuid
import os
import re
from itertools import starmap
import multiprocessing
import pysrt
import imageio
import youtube_dl
import chardet
import nltk

# imageio.plugins.ffmpeg.download()
#nltk.download('punkt')

from moviepy.editor import VideoFileClip, concatenate_videoclips
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.nlp.stemmers import Stemmer
from sumy.utils import get_stop_words
from sumy.summarizers.lsa import LsaSummarizer


# https://www.youtube.com/watch?v=Fkd9TWUtFm0
# imageio.plugins.ffmpeg.download()


def summarize(srt_file, n_sentences, language="english"):
    # generate segmented summary
    parser = PlaintextParser.from_string(
        srt_to_txt(srt_file), Tokenizer(language))
    stemmer = Stemmer(language)
    summarizer = LsaSummarizer(stemmer)
    summarizer.stop_words = get_stop_words(language)
    segment = []
    for sentence in summarizer(parser.document, n_sentences):
        index = int(re.findall("\(([0-9]+)\)", str(sentence))[0])
        item = srt_file[index]
        segment.append(srt_segment_to_range(item))
    
    return segment


def srt_to_txt(srt_file):
    # extract text from subtitles file
    text = ''
    for index, item in enumerate(srt_file):
        if item.text.startswith("["):
            continue
        text += "(%d) " % index
        text += item.text.replace("\n", "").strip("...").replace(
            ".", "").replace("?", "").replace("!", "")
        text += ". "

    return text


def srt_segment_to_range(item):
    # handling of srt segments to time range
    start_segment = item.start.hours * 60 * 60 + item.start.minutes * \
                    60 + item.start.seconds + item.start.milliseconds / 1000.0
    end_segment = item.end.hours * 60 * 60 + item.end.minutes * \
                  60 + item.end.seconds + item.end.milliseconds / 1000.0
    
    return start_segment, end_segment


def time_regions(regions):
    # duration of segments
    return sum(starmap(lambda start, end: end - start, regions))


def find_summary_regions(srt_filename, duration=30, language="english"):
    # find important sections
    #srt_filename = "C:/Users/kumar/Desktop/mywork/vidsum/media/1.en.srt"
    srt_file = pysrt.open(srt_filename)

    enc = chardet.detect(open(srt_filename, "rb").read())['encoding']
    srt_file = pysrt.open(srt_filename, encoding=enc)

    # generate average subtitle duration
    subtitle_duration = time_regions(
        map(srt_segment_to_range, srt_file)) / len(srt_file)
    # compute number of sentences in the summary file
    n_sentences = duration / subtitle_duration
    summary = summarize(srt_file, n_sentences, language)
    total_time = time_regions(summary)
    too_short = total_time < duration
    if too_short:
        while total_time < duration:
            n_sentences += 1
            summary = summarize(srt_file, n_sentences, language)
            total_time = time_regions(summary)
    else:
        while total_time > duration:
            n_sentences -= 1
            summary = summarize(srt_file, n_sentences, language)
            total_time = time_regions(summary)
    return summary


def create_summary(filename, regions):
    # join segments
    subclips = []
    input_video = VideoFileClip(filename)
    last_end = 0
    for (start, end) in regions:
        subclip = input_video.subclip(start, end)
        subclips.append(subclip)
        last_end = end
    return concatenate_videoclips(subclips)


def get_summary(filename, subtitles):
    # abstract function
    regions = find_summary_regions(subtitles, 60, "english")
    summary = create_summary(filename, regions)
    base, ext = os.path.splitext(filename)
    output = "{0}_summarized.mp4".format(base)
    summary.to_videofile(
        output,
        codec="libx264",
        temp_audiofile="temp.m4a", remove_temp=True, audio_codec="aac")
    return output

def download_video_srt(url):
    # downloads specified Youtube video's subtitles as a vtt/srt file.

    id = uuid.uuid1()

    ydl_opts = {
        'format': 'best',
        'outtmpl': 'media/'+str(id)+'.%(ext)s',
        'subtitlesformat': 'srt',
        'writeautomaticsub': True,
        '--no-check-certificate': True,
        # 'allsubtitles': True # Get all subtitles
    }

    print('yt function called')
    movie_filename = ""
    subtitle_filename = ""
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        # ydl.download([subs])
        ydl.cache.remove()
        result = ydl.extract_info("{}".format(url), download=True)
        movie_filename = ydl.prepare_filename(result)
        subtitle_info = result.get("requested_subtitles")
        subtitle_language = 'en'
        subtitle_ext = subtitle_info.get(subtitle_language).get("ext")
        subtitle_filename = movie_filename.replace(".mp4", ".%s.%s" %
                                                   (subtitle_language,
                                                    subtitle_ext))


    print('video downloads')
    print((movie_filename,subtitle_filename))
    return movie_filename, subtitle_filename


@csrf_exempt
def summarize_view(request):

   link = request.POST.get("link")
   print(link)
   movie_filename, subtitle_filename = download_video_srt(link)
   output = get_summary(movie_filename,subtitle_filename)

   return JsonResponse({'result':output})


def index(request):

    return render(request,"index.html")
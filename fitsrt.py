import fitparse
import datetime
import srt
def fitsrt(fit_file, srt_file, delay = 0):
    fitfile = fitparse.FitFile(fit_file)
    delay = datetime.timedelta(seconds=delay)
    starttime = None
    subtitles = []
    for record in fitfile.get_messages("record"):
        for data in record:
            if data.name=="heart_rate":
                hr = f"{data.value} {data.units}"
                if len(hr) < 7:
                    hr='0'+hr
            if data.name=="timestamp":
                if starttime == None:
                    starttime = data.value
                    newtime = data.value
                    continue
                prevtime = newtime
                newtime = data.value
                subtitles.append(srt.Subtitle(index = len(subtitles)+1, start = prevtime - starttime + delay, end = newtime - starttime + delay, content=hr))
    with open(srt_file, 'w') as f:
        f.write(srt.compose(subtitles))
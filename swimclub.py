import statistics

FOLDER = 'swimdata/'
CHARTS = 'charts/'

def read_swim_data(filename):
    """Return swim data drom a file.

    Given the name of a swimmer's file (in filename), extract all the required
    data, then return it to the caller as a tuple
    """
    swimmer, age, distance, stroke = filename.removesuffix(".txt").split('-')
    with open(FOLDER + filename) as file:
        lines = file.readlines()
        times = lines[0].strip().split(',')
    converts = []
    for t in times:
        # The minutes value might be missing, so guard against this causing a crash.
        if ':' in t:
            minutes, rest = t.split(':')
            seconds, hundredths = rest.split('.')
        else:
            minutes = 0
            seconds, hundredths = t.split('.')
        converted_time = (int(minutes) * 60 * 100) + (int(seconds) * 100) + int(hundredths)
        converts.append(converted_time)
        # print(t,'->',converted_time)
    average = statistics.mean(converts)
    mins_secs , hundredths = f"{(average / 100):.2f}".split('.')
    mins_secs = int(mins_secs)
    minutes = mins_secs // 60
    seconds = mins_secs - minutes * 60
    # average = str(minutes) + ':' + str(seconds) + '.' + hundredths
    average = f"{minutes}:{seconds:0>2}.{hundredths}"
    return swimmer, age, distance, stroke, times, average, converts # Returned as a tuple

def convert2range(v, f_min, f_max, t_min, t_max):
    """Given a value (v) in the range f_min-f_max, convert the value
    to its equivalent value in the range t_min-t_max.

    Based on the technique described here:
        http://james-ramsden.com/map-a-value-from-one-number-scale-to-another-formula-and-c-code/
        
    for n in converts:
        print(n, "->", hfpy_utils.convert2range(n, 0, max(converts), 0, 400))
    """
    return round(t_min + (t_max - t_min) * ((v - f_min) / (f_max - f_min)), 2)

def produce_bar_chart(fn):
    """
        Given the name of a swimmer's file, produce a HTML/SVG-based bar chart.
        Save the chart to the CHARTs folder. Return the path to the bar chart file
    """
    swimmer, age, distance, stroke, times, average, converts = read_swim_data(fn)
    times.reverse()
    converts.reverse()
    title = f"{swimmer} (Under {age}) {distance} {stroke}"
    header = f"""<!DOCTYPE html>
                    <html>
                        <head>
                            <title>{title}</title>
                        </head>
                        <body>
                            <h3>{title}</h3>"""
    body = ""
    for n, t in enumerate(times):
        bar_width = convert2range(converts[n], 0, max(converts), 0, 350)
        body = body + f"""
                            <svg height="30" width="400">
                                <rect height="30" width="{bar_width}" style="fill:rgb(0,0,255);" />
                            </svg>{t}<br />
                        """
    footer = f"""
                            <p>Average time:{average}</p>
                        </body>
                    </html>
        """
    page = header + body + footer
    save_to = f"{CHARTS}{fn.removesuffix('.txt')}.html"
    with open(save_to,"w") as tf:
        print(page, file=tf)
    
    return save_to

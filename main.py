import os
import webbrowser
import swimclub

chart = swimclub.produce_bar_chart("Darius-13-100m-Fly.txt")
webbrowser.open('file://' + os.path.realpath(chart))
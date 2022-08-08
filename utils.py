from datetime import datetime


def progress_bar(start, end, actual):
    actual = end if actual > end else actual
    percent = 100 * ((actual - start) / float(end - start))
    bar = "█" * int(percent) + "░" * (100 - int(percent))
    print(f"\r{bar} {percent:.2f}%", end="\r")


def date_to_str(date):
    return datetime.fromtimestamp(date).strftime("%d/%m/%Y %H:%M")
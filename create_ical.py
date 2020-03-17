from icalendar import Calendar, Event, vText
from datetime import datetime, date, timezone

def next_30_min(h,m):
    h = (h + (m+30 == 60)) % 24
    m = (m+30)%60
    return h, m

cal = Calendar()

with open("data.txt", encoding="utf-8") as f:
    day = []
    for line in f:
        if not len(line.strip()): pass
        elif line[0]=="-": # new day from DD/MM/YYYY
            day = list(map(int, line[1:].split("/")[::-1]))
        else:
            p = line.strip().split(" ")
            time, name, link = p[0], " ".join(p[1:-1]), p[-1]
            h, m = map(int, time.split("h"))
            e = Event()
            e.add("summary", name)
            e.add('dtstart', datetime(*day, h, m, tzinfo=timezone.utc))
            e.add('dtend', datetime(*day, *next_30_min(h, m), tzinfo=timezone.utc))
            e["location"] = vText(link)
            cal.add_component(e)

print(cal.to_ical())
with open("out.ics", "w", encoding="utf-8") as o:
    o.write(cal.to_ical().decode("utf-8").replace("\r\n", "\n"))
#!/usr/bin/python3
from datetime import date
from github import Github
import re


def get_tag_date(tag):
    pattern = re.compile('^(raspberrypi-kernel_1\.)([0-9]{8,})(.*)')
    x = pattern.match(tag.name)
    return(x.group(2))


g = Github()
raspberrypi = g.get_repo("raspberrypi/linux")
tags = raspberrypi.get_tags()
highest_date = 0
latest_tag = ""
for tag in tags:
    try:
        tag_date = get_tag_date(tag)
        if int(tag_date) > highest_date:
            highest_date = int(tag_date)
            latest_tag = tag.name
    except:
        pass

print(latest_tag)

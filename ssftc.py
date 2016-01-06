#!/usr/bin/env python3

"""
A small scraper to check all my Sweepstakes for the Cure calendar numbers
for winners.
"""

import datetime
import os
import re
import smtplib

import requests


def check_winners(recipients, winners_url, cal_num_fname):

    winners = get_winners_from_web(winners_url)
    cal_numbers = get_cal_numbers(cal_num_fname)

    winners = find_matches(cal_numbers, winners)
    if winners:
        msg =  "Winning numbers: {}".format(", ".join(winners))
    else:
        msg =  "No winning numbers"

    send_msg(recipients, msg)


def get_winners_from_web(url):
    resp = requests.get(url)
    return re.findall("\d{8}", resp.content.decode("UTF-8"))


def get_cal_numbers(fname):
    with open(fname, "r") as f:
        calendar_numbers = {n.strip() for n in f.readlines()}
    return calendar_numbers


def find_matches(cal_numbers, winners):
    return set(cal_numbers).intersection(set(winners))


def send_msg(recipients, msg):

    gmail_user = os.environ["SSFTC_GMAIL_ADDRESS"]
    gmail_pwd = os.environ["SSFTC_GMAIL_APP_PWD"]

    from_ = "ssftc@randlet.com"
    to = recipients if type(recipients) is list else [recipients]
    subject = "SSFTC Scraper Results For {}".format(datetime.date.today())

    message = """\From: %s\nTo: %s\nSubject: %s\n\n%s""" % (from_, ", ".join(to), subject, msg)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.ehlo()
        server.starttls()
        server.login(gmail_user, gmail_pwd)
        server.sendmail(from_, to, message)
        server.close()
    except:
        pass


if __name__ == "__main__":

    WINNERS_URL = "https://sweepstakesforthecure.ca/winners.aspx"
    CAL_NUM_FILE = "numbers.txt"
    SEND_TO = ["randle.taylor@gmail.com"]

    check_winners(SEND_TO, WINNERS_URL, CAL_NUM_FILE)




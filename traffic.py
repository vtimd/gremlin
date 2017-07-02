#!/usr/bin/python

from faker import Factory
import logging
import requests
from time import sleep
import sys
import os
import argparse
import string

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
fake = Factory.create()


url = "http://52.53.160.113/signup/"

def parse_args():
    #defining and parsing arguments from the command line
    parser = argparse.ArgumentParser (description = 'Type in your urls')
    parser.add_argument('-u1', '--url1', help= "your first url")
    parser.add_argument('-u2' ,'--url2', help="your second url")
    return parser.parse_args()


def check_args(args):

  if args.url1 or args.url2:
    return 1
  else:
    return 0


def push_form(url,payload,s):
    r = s.post(url, data=payload, headers=dict(Referer=url))
    if (r.status_code == 200):
        log.info('Added user %s %s', payload["firstname"], payload["lastname"])
    else:
        log.info('Failure adding user, error code ' + str(r.status_code))
    log.debug(r.content)
    return r

def create_payload(csrftoken):
    person = fake.profile()
    log.debug(person)
    fname,lname = person["name"].split(" ")
    payload = {
      "firstname":fname,
      "lastname":lname,
      "email":person["mail"],
      "csrfmiddlewaretoken":csrftoken
        }
    log.debug(payload)
    return payload


def senddata(url):

    s = requests.session()
    s.get(url)
    csrftoken = s.cookies['csrftoken']
    log.debug("Using token " + csrftoken)
    payload = create_payload(csrftoken)
    r = push_form(url,payload,s)
    log.info(r.status_code)



def main():
    args = parse_args()
    if check_args(args):
      if args.url1: 
        url1=args.url1
        senddata(url1)

      if args.url2:
        url2=args.url2
        senddata(url2)

    else:
      print "enter in at least one url"



if __name__ == '__main__':
    main()


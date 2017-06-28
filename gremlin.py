#!/usr/bin/python

from faker import Factory
import logging
import requests
from time import sleep

logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)
fake = Factory.create()


url = "http://52.53.160.113/signup/"

def push_form(url,payload):
    r = s.post(url, data=payload, headers=dict(Referer=url))
    if (r.status_code == 200):
        log.info('Added user %s %s', payload["firstname"], payload["lastname"])
    else:
        log.info('Failure adding user, error code ' + str(r.status_code))
    log.debug(r.content)
    return r

def create_payload():
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

s = requests.session()
s.get(url)
csrftoken = s.cookies['csrftoken']
log.debug("Using token " + csrftoken)
payload = create_payload()
r = push_form(url,payload)
log.info(r.status_code)

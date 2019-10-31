#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

from telegram.ext import Updater, CommandHandler
from settings import TOKEN

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar']

def event(Title):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)

    # Refer to the Python quickstart on how to setup the environment:
    # https://developers.google.com/calendar/quickstart/python
    # Change the scope to 'https://www.googleapis.com/auth/calendar' and delete any
    # stored credentials.

    event = {
      'summary': Title,
      'location': '',
      'description': 'Test',
      'start': {
        'dateTime': '2019-10-29T10:00:00',
        'timeZone':  'Europe/Paris' ,
      },
      'end': {
        'dateTime': '2019-10-30T17:00:00',
        'timeZone': 'Europe/Paris' ,
      },
      # BUG: This insert events DAILY and 2 times
      # 'recurrence': [
        # 'RRULE:FREQ=DAILY;COUNT=2'
      # ],
      'attendees': [
        # Insert here the emails
        # {'email': ''},
      ],
      'reminders': {
        'useDefault': False,
        'overrides': [
          {'method': 'email', 'minutes': 24 * 60},
          {'method': 'popup', 'minutes': 10},
        ],
      },
    }

    event = service.events().insert(calendarId='primary', body=event).execute()
    #print 'Event created: %s' % (event.get('htmlLink'))
    print('Event created')

def create(update, context): 

    print('Hello')
    update.message.reply_text('Hello! What is the name of the event')
    Title = update.message.text[len('/create'):]
    print(Title)

    event(Title)
    

def hello(update, context):
    update.message.reply_text(
        'Hello {}'.format(update.message.from_user.first_name))

updater = Updater(TOKEN, use_context=True)

updater.dispatcher.add_handler(CommandHandler('create', create))
updater.dispatcher.add_handler(CommandHandler('hello', hello))

updater.start_polling()
updater.idle()


#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import os
import pickle
from datetime import datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from telegram.ext import (CommandHandler, ConversationHandler, Filters,
                          MessageHandler, Updater)

from settings import TOKEN

# Possible states in the conversation
TITLE, START_DATE, START_TIME, END_DATE,\
    END_TIME, DESCRIPTION, LOCATION = range(7)



def start(update, context):
    # TODO Let me say something
    update.message.reply_text("Salve, questo bot crea eventi per un calendario google. Premi /create_event per iniziare")
    pass

def create_event(update, context):
    update.message.reply_text("Come si chiama l'evento?")
    return TITLE


def check_title(update, context):
    # Get sent message and save it for later
    text = update.message.text
    context.user_data['title'] = text

    update.message.reply_text("Quando inizia? (DD-MM-YYYY)")
    return START_DATE


def check_start_date(update, context):
    # Get sent message
    text = update.message.text

    # TODO Check if string is a valid date

    # Convert the date to YYYY-MM-DD
    date = datetime.strptime(text, "%d-%m-%Y").strftime("%Y-%m-%d")

    # Save it for later
    context.user_data['start_date'] = date
    update.message.reply_text("A che ora? (HH:MM)")

    return START_TIME


def check_start_time(update, context):
    # Get sent message
    text = update.message.text

    # TODO Check if string is a valid time

    # Save it for later
    context.user_data['start_time'] = text
    update.message.reply_text("Quando finisce? (DD-MM-YYYY)")

    return END_DATE


def check_end_date(update, context):
    text = update.message.text

    # Convert the date to YYYY-MM-DD
    date = datetime.strptime(text, "%d-%m-%Y").strftime("%Y-%m-%d")

    # TODO Check if string is a valid date

    # Save it for later
    context.user_data['end_date'] = date
    update.message.reply_text("A che ora? (HH:MM)")

    return END_TIME


def check_end_time(update, context):
    # Get sent message
    text = update.message.text

    # TODO Check if string is a valid time

    # Save it for later
    context.user_data['end_time'] = text
    update.message.reply_text("Cosa metto come descrizione dell'evento?")

    return DESCRIPTION


def check_description(update, context):
    # Get sent message and save it for later
    text = update.message.text
    context.user_data['description'] = text

    update.message.reply_text("Dove si terrà l'evento? (Via X, Citta' Y)")

    return LOCATION


def check_location(update, context):
    # Get location
    location = update.message.text

    # Get date from user_data
    title = context.user_data['title']
    start_date = context.user_data['start_date']
    start_time = context.user_data['start_time']
    end_date = context.user_data['end_date']
    end_time = context.user_data['end_time']
    description = context.user_data['description']

    # Insert event with gathered data
    insert_event(title, start_date, end_date, start_time,
                 end_time, description, location)

    context.user_data = {}
    update.message.reply_text("Evento creato con successo!")

    return ConversationHandler.END


def cancel(update, context):
    # Reset user data
    context.user_data = {}
    update.message.reply_text("Ho cancellato tutto!")

    return ConversationHandler.END


def insert_event(title, start_date, end_date, start_time, end_time, description, location):
    """Insert a new event in the calendar"""

    # Get API connection
    service = get_calendar_service()

    # Prepare event
    event = {
        'summary': title,
        'location': location,
        'description': description,
        'start': {
            'dateTime': '{0}T{1}:00'.format(start_date, start_time),
            'timeZone':  'Europe/Rome',
        },
        'end': {
            'dateTime': '{0}T{1}:00'.format(end_date, end_time),
            'timeZone': 'Europe/Rome',
        },
    }

    # Insert event
    calendar_id = settings.DEFAULTS.get('calendar_id', 'primary')
    event = service.events().insert(calendarId=calendar_id, body=event).execute()
    #update.message.reply_text('Evento creato con successo!')

def get_calendar_service():
    """Create a connection to the Calendar API"""
    creds = None

    # Delete the file token.pickle if modifying these scopes
    SCOPES = ['https://www.googleapis.com/auth/calendar']

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

    return build('calendar', 'v3', credentials=creds)


def main():
    print("---Starting bot---")

    # Initialize the bot
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler('start', start))

    # Create new conversation handler
    dispatcher.add_handler(ConversationHandler(
        # Conversation start from this handler
        entry_points=[CommandHandler('create_event', create_event)],

        # Defines the different states of conversation a user can be in
        states={
            # Filter messages looking just for text
            TITLE: [MessageHandler(Filters.text, check_title)],

            # Filter messages looking for date (31/12/19)
            START_DATE: [MessageHandler(Filters.regex('[0-9]{2}-[0-9]{2}-[0-9]{2}'), check_start_date)],

            # Filter messages looking for time (09:00)
            START_TIME: [MessageHandler(Filters.regex('[0-9]{2}:[0-9]{2}'), check_start_time)],

            # Filter messages looking for date (31/12/19)
            END_DATE: [MessageHandler(Filters.regex('[0-9]{2}-[0-9]{2}-[0-9]{2}'), check_end_date)],

            # Filter messages looking for time (09:00)
            END_TIME: [MessageHandler(Filters.regex('[0-9]{2}:[0-9]{2}'), check_end_time)],

            # Filter messages looking just for text
            DESCRIPTION: [MessageHandler(Filters.text, check_description)],

            # Filter messages for text
            LOCATION: [MessageHandler(Filters.text, check_location)],
        },

        # A list of handlers that might be used if the user is in a conversation,
        # but every handler for their current state returned
        fallbacks=[CommandHandler('cancel', cancel)],

        # Determines if a user can restart a conversation with an entry point
        allow_reentry=True
    ))

    # Start bot
    updater.start_polling()
    updater.idle()


if __name__ == "__main__":
    main()

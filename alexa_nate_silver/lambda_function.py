#!/usr/local/bin/python2.7

from __future__ import print_function
import random
import gzip
import urllib2
from StringIO import StringIO
import re
import json

# --------------- Helpers that build all of the responses ----------------------
def build_speechlet_response(title, output, reprompt_text, should_end_session):
    print(output)
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': "SessionSpeechlet - " + title,
            'content': "SessionSpeechlet - " + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }


def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def get_welcome_response():
    session_attributes = {}
    card_title = "Nate Silver Election Tracker"
    speech_output = "Welcome to the Nate Silver Election Tracker"
    
    # If the user either does not reply to the welcome message or says something
    # that is not understood, they will be prompted again with this text.
    reprompt_text = "Ask me who will win."
    should_end_session = False
    return build_response(session_attributes, build_speechlet_response(
        card_title, speech_output, reprompt_text, should_end_session))


def handle_session_end_request():
    card_title = "Goodbye"
    speech_output = "Thanks for checking in!"
    # Setting this to true ends the session and exits the skill.
    should_end_session = True
    return build_response({}, build_speechlet_response(
        card_title, speech_output, None, should_end_session))


# There is a beautiful, rich json string embedded in this html. Let's
# extract and parse it.
def extract_election_info(htmlstring):
    extract_re = re.compile(r'race\.stateData\s=\s(.*);\s*race\.pathPrefix')
    m = extract_re.search(htmlstring)
    if m:
        json_string = m.group(1)
        try:
            data = json.loads(json_string)
            return data
        except:
            pass
    return None

def election_prob(intent, session):
    req = urllib2.Request('https://projects.fivethirtyeight.com/2016-election-forecast/')
    req.add_header('Accept-encoding','gzip')
    resp = urllib2.urlopen(req)

    data = None

    if resp.info().get('Content-Encoding') == 'gzip':
        buf = StringIO(resp.read())
        f = gzip.GzipFile(fileobj=buf)
        data = f.read()
    else:
        data = resp.read()

    if data is not None:
        pdata = extract_election_info(data)

        parties = {
          'D': 'Hillary Clinton',
          'R': 'Donald Trump',
          'L': 'Gary Johnson',
        }
        results = {}
        for party in parties:
            v = pdata['latest'][party]['models']['now']['winprob']
            results[party] = str(v) + '%'

        resp = "If the election were held right now, Nate Silver predicts "
        for party in parties:
            resp += parties[party] + " has a " + results[party] + ' probability of winning. '
        return build_response({}, build_speechlet_response("Right now", resp, "", True))


    resp = "Could not contact the 538 blog successfully."
    return build_response({}, build_speechlet_response("Uh oh", resp, "", False))
    

def on_session_started(session_started_request, session):
    pass

def on_launch(launch_request, session):
    return get_welcome_response()

def on_session_ended(session_ended_request, session):
    handle_session_end_request()

def on_intent(intent_request, session):
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == 'election':
        return election_prob(intent, session)
    else:
        raise ValueError("Invalid intent")


# --------------- Main handler ------------------
def lambda_handler(event, context):
    if (event['session']['application']['applicationId'] !=
            "amzn1.ask.skill.758208a4-1eaf-44b1-8101-241c2c4254cf"):
        raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},
                           event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


x = {
 'request': {
  'requestId': 'blein23423523',
  'type': 'IntentRequest',
  'intent': {
   'name': 'election',
  },
 },
 'session': {
  'new': 'False',
  'application': {
   'applicationId': 'amzn1.ask.skill.758208a4-1eaf-44b1-8101-241c2c4254cf',
  },
 },
}

# lambda_handler(x, {})



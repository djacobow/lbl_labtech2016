#!/usr/local/bin/python2.7

from __future__ import print_function
import random
import gzip
import zlib 
from HTMLParser import HTMLParser
import urllib2
from StringIO import StringIO


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


class my_parser(HTMLParser):
    def __init__(self):
        self.edata = {
         'done_R': False,
         'done_D': False,
         'done_L': False,
         'in_R': False,
         'in_D': False,
         'in_L': False,
         'D': '',
         'R': '',
         'L': '',
        }
        HTMLParser.__init__(self)
    def handle_starttag(self, tag, attrs):
        if tag == 'p' :
            print(attrs)
            is_winprob = False
            party = None
            if True:
                for attr in attrs:
                    if attr[0] == 'data-key' and attr[1] == 'winprob':
                        is_winprob = True
                    if attr[0] == 'data-party':
                        party = attr[1]
                self.edata['started'] = True
                if is_winprob:
                    if not self.edata['done_R']:
                        self.edata['in_R'] = party == 'R'
                    if not self.edata['done_D']:
                        self.edata['in_D'] = party == 'D'
                    if not self.edata['done_L']:
                        self.edata['in_L'] = party == 'L'

    def handle_endtag(self, tag):
        if tag == 'p':
            if self.edata['in_D']: 
                self.edata['in_D'] = False
                self.edata['done_D'] = True
            if self.edata['in_R']: 
                self.edata['in_R'] = False
                self.edata['done_R'] = True
            if self.edata['in_L']: 
                self.edata['in_L'] = False
                self.edata['done_L'] = True

    def handle_data(self, data):
        print(data)
        if self.edata['in_D']:
            self.edata['D'] += data
        if self.edata['in_R']:
            self.edata['R'] += data
        if self.edata['in_L']:
            self.edata['L'] += data

    def getResults(self):
        return self.edata

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
        parser = my_parser()
        parser.feed(data)
        results = parser.getResults()
        resp = "If the election were held right now, Nate Silver predicts "
        if 'D' in results:
            resp += "Hillary Clinton has a " + results['D'] + ' probability of winning. '
        if 'R' in results:
            resp += "Donald Trump has a " + results['R'] + ' probability of winning. '
        if 'L' in results:
            resp += "Gary Johnsnon has a " + results['L'] + ' probability of winning. '
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



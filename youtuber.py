import os
import webbrowser

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors


# import requests
# from typing import Final


class YoutuveRequests(object):
    youtube = None

    def __init__(self, youtube):
        self.youtube = youtube


class YoutubeLiveBroadcasts(YoutuveRequests):

    def list_by_id(self, youtube_translation_id: str) -> str:
        request = self.youtube.liveBroadcasts().list(
            id=youtube_translation_id,
            part=['id', 'snippet', 'contentDetails', 'status']
        )
        response = request.execute()
        return response

    def list_by_broadcast_status(self, broadcast_status: str) -> str:
        request = self.youtube.liveBroadcasts().list(
            broadcastStatus=broadcast_status,
            part=['id', 'snippet', 'contentDetails', 'status']
        )
        response = request.execute()
        return response


class YoutubeLiveChatMessage(YoutuveRequests):
    # max_results min 200 max 2000
    # profile_image_size min 16 max 720
    def list(self, live_chat_id: str, part: str, max_results: int = 500, page_token: str = None, profile_image_size: int = 88) -> str:
        request = self.youtube.liveChatMessages().list(
            liveChatId=live_chat_id,
            part=part,
            maxResults=max_results,
            pageToken=page_token,
            profileImageSize=profile_image_size
        )
        response = request.execute()
        return response


class Youtube(object):
    YOUTUBE_SERVICE_NAME = 'youtube'
    YOUTUBE_API_VERSION = 'v3'
    YOUTUBE_CLIENT_SECRETS_FILE = 'client_secret.json'
    YOUTUBE_SCOPES = ['https://www.googleapis.com/auth/youtube.readonly']

    live_broadcasts = None
    youtube_live_chat = None

    def __init__(self):
        # TODO вынести эту хуйню из init

        # Disable OAuthlib's HTTPS verification when running locally.
        # *DO NOT* leave this option enabled in production.
        os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'

        # Get credentials and create an API client
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            self.YOUTUBE_CLIENT_SECRETS_FILE,
            self.YOUTUBE_SCOPES,
            redirect_uri='urn:ietf:wg:oauth:2.0:oob'
        )

        auth_url, _ = flow.authorization_url()
        webbrowser.open(auth_url, new=0, autoraise=True)  # redirect to url

        code = input('Enter the authorization code: ')
        flow.fetch_token(code=code)

        youtube = googleapiclient.discovery.build(
            self.YOUTUBE_SERVICE_NAME,
            self.YOUTUBE_API_VERSION,
            credentials=flow.credentials
        )

        self.live_broadcasts = YoutubeLiveBroadcasts(youtube)
        self.youtube_live_chat = YoutubeLiveChatMessage(youtube)

    @staticmethod
    def extract_live_chat_id(response):
        live_chats = []
        items = response.get('items')
        if len(items) == 0:
            return live_chats

        for key in range(len(items)):
            try:
                live_chat_id = items[key]['snippet']['liveChatId']
                live_chats.append({
                    'translation_id': items[key].get('id'),
                    'live_chat_id': live_chat_id
                })
            except KeyError:
                pass

        return live_chats

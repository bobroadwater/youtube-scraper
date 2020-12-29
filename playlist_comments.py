import csv
import os
import pickle

import google.oauth2.credentials

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow

# The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
# the OAuth 2.0 information for this application, including its client_id and
# client_secret.
CLIENT_SECRETS_FILE = "client_secret.json"

# This OAuth 2.0 access scope allows for full read/write access to the
# authenticated user's account and requires requests to use an SSL connection.
SCOPES = ['https://www.googleapis.com/auth/youtube.force-ssl']
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'


def get_authenticated_service():
    credentials = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            credentials = pickle.load(token)
    #  Check if the credentials are invalid or do not exist
    if not credentials or not credentials.valid:
        # Check if the credentials have expired
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                CLIENT_SECRETS_FILE, SCOPES)
            credentials = flow.run_console()

        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(credentials, token)

    return build(API_SERVICE_NAME, API_VERSION, credentials = credentials)

def write_to_text(comments):
    with open('comments.txt', 'w', encoding='utf-8') as comments_file:
        comments_file.writelines(comments)

def get_video_comments(service, **kwargs):
    comments = []
    results = service.commentThreads().list(**kwargs).execute()

    while results:
        for item in results['items']:
            comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
            comments.append(comment)

        # Check if another page exists
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.commentThreads().list(**kwargs).execute()
        else:
            break

    return comments

def get_videos_from_playlist(service, **kwargs):
    final_results = []
    results = service.playlistItems().list(**kwargs).execute()

    i = 0
    max_pages = 10
    while results and i < max_pages:
        final_results.extend(results['items'])

        # Check if another page exists
        if 'nextPageToken' in results:
            kwargs['pageToken'] = results['nextPageToken']
            results = service.playlistItems().list(**kwargs).execute()
            i += 1
        else:
            break

    return final_results


def get_playlist_comments(service, **kwargs):
    results = get_videos_from_playlist(service, **kwargs)
    final_result = []
    for item in results:
        # check if video is still public
        if item['status']['privacyStatus'] == 'public':
            video_id = item['snippet']['resourceId']['videoId']
            # check if comments are still enabled
            if 'commentCount' in service.videos().list(part='id,statistics',id=video_id).execute()['items'][0]['statistics']:
                comments = get_video_comments(service, part='snippet', videoId=video_id, textFormat='plainText')
                final_result.extend(comments) 

    write_to_text(final_result)


if __name__ == '__main__':
    # When running locally, disable OAuthlib's HTTPs verification. When
    # running in production *do not* leave this option enabled.
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    service = get_authenticated_service()
    pid = input('Enter a playlist ID (enter "PIC" for Partners in Cream Playlist): ')
    if pid == 'PIC':
        pid = 'PL1zPctfe530k4BTOqyEKtrk2n4qF3Zvn9'
    get_playlist_comments(service, playlistId=pid, part='snippet,status',maxResults=50)

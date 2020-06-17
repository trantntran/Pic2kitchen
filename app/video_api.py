# import argparse

# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# DEVELOPER_KEY = 'AIzaSyAASxTSqfFFIHF0hzyGMEDWsVSskLyyMgo'
# YOUTUBE_API_SERVICE_NAME = 'youtube'
# YOUTUBE_API_VERSION = 'v3'

# def youtube_search(options):
#   youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,
#     developerKey=DEVELOPER_KEY)

#   # Call the search.list method to retrieve results matching the specified
#   # query term.
#   search_response = youtube.search().list(
#     q=options['q'],
#     part='id,snippet',
#     maxResults=options['max_results']
#     return 
#   ).execute()

#   videos = []
#   channels = []
#   playlists = []

#     # Add each result to the appropriate list, and then display the lists of
#     # matching videos, channels, and playlists.
#   for search_result in search_response.get('items', []):
#   if search_result['id']['kind'] == 'youtube#video':
#       videos.append('%s (%s)' % (search_result['snippet']['title'],\
#                                   search_result['id']['videoId']))
#   elif search_result['id']['kind'] == 'youtube#channel':
#       channels.append('%s (%s)' % (search_result['snippet']['title'],\
#                                   search_result['id']['channelId']))
#   elif search_result['id']['kind'] == 'youtube#playlist':
#       playlists.append('%s (%s)' % (search_result['snippet']['title'],\
#                                   search_result['id']['playlistId']))
  
#   return {""

#   }



# def query(name):
#   options = {'q':'how to cook '+name, 'max_results':1}
#   youtube_search(options)
#   #return output
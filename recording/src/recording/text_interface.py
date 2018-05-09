from apiclient.discovery import build_from_document
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from recording.src.constants import path_consts as pc
import httplib2
import os
import sys
#
class TextInterface():
    """
    This class is reserved for logic pertaining to text acquisition from
    online resources. The logic is structured to serve two different modes
    of text gathering:

    1) Pre-recorded text acquisition - Applies to YouTube comments &
    comment threads only

    2) Live text acquisition - Applies to live chats which are updated
    in realtime.

    This class will operate on data pulled off the config_interface.
    """
    #
    def __init__(self,config_obj):
        """
        Default Constructor

        :param config_obj:  A class structure used to contain information acquired from the input_channels.json config file
        """
        self.config_obj = config_obj
        #
        """
        The CLIENT_SECRETS_FILE variable specifies the name of a file that contains
        the OAuth 2.0 information for this application, including its client_id and
        client_secret. You can acquire an OAuth 2.0 client ID and client secret from
        the {{ Google Cloud Console }} at {{ https://cloud.google.com/console }}.
        
        Please ensure that you have enabled the YouTube Data API for your project.
        For more information about using OAuth2 to access the YouTube Data API, see:
        https://developers.google.com/youtube/v3/guides/authentication
        
        For more information about the client_secrets.json file format, see:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """
        self.CLIENT_SECRETS_FILE = pc.FILE_YOUTUBE_API_SECRET
        #
        """
        This OAuth 2.0 access scope allows for full read/write access to the
        authenticated user's account and requires requests to use an SSL connection.
        """
        self.YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"
        #
        # This variable defines a message to display if the CLIENT_SECRETS_FILE is
        # missing.
        self.MISSING_CLIENT_SECRETS_MESSAGE = """
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file
        found at:
           %s
        with information from the APIs Console
        https://console.developers.google.com

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           self.CLIENT_SECRETS_FILE))
    #
    def get_authenticated_service(self, args):
        """
        Authorize the request and store authorization credentials.

        :param args:
        :return:
        """
        print("Authenticating with yt API..")
        flow = flow_from_clientsecrets(self.CLIENT_SECRETS_FILE, scope=self.YOUTUBE_READ_WRITE_SSL_SCOPE,
                                       message=self.MISSING_CLIENT_SECRETS_MESSAGE)
        #
        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()
        #
        if credentials is None or credentials.invalid:
            credentials = run_flow(flow, storage, args)
        #
        # Trusted testers can download this discovery document from the developers page
        # and it should be in the same directory with the code.
        with open(pc.FILE_YOUTUBE_API_V3_DISCOVERYDOCUMENT, "r") as f:
            doc = f.read()
            return build_from_document(doc, http=credentials.authorize(httplib2.Http()))
    #
    def get_comment_threads(self, youtube, video_id):
        """
        Call the API's commentThreads.list method to list the existing comment threads.

        :param youtube:
        :param video_id:
        :return:
        """
        print("Retrieving YouTube comment threads..")
        results = youtube.commentThreads().list(
            part="snippet",
            videoId=video_id,
            textFormat="plainText",
            maxResults=100
        ).execute()
        #
        comment_map = dict()
        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]
            author = comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            if author in comment_map:
                comment_map[author].append(text)
            else:
                comment_map[author] = []
                comment_map[author].append(text)
        #
        return results["items"], comment_map
    #
    def get_comments(self, youtube, parent_id, comment_map):
        """
        Call the API's comments.list method to list the existing comment replies.

        :param youtube:
        :param parent_id:
        :param comment_map:
        :return:
        """
        print("Retrieving YouTube comment replies with pid [" + str(parent_id) + "]..")
        results = youtube.comments().list(
            part="snippet",
            parentId=parent_id,
            textFormat="plainText",
            maxResults=100
        ).execute()
        #
        for item in results["items"]:
            author = item["snippet"]["authorDisplayName"]
            text = item["snippet"]["textDisplay"]
            if author in comment_map:
                comment_map[author].append(text)
            else:
                comment_map[author] = []
                comment_map[author].append(text)
        #
        return comment_map
    #
    def __get_video_id(self):
        """
        Parses youtube url and returns only the video id

        :return:
        """
        src_url = self.config_obj.get_details()['src']
        match_string_to_remove = "https://www.youtube.com/watch?v="
        src_url = src_url.replace(match_string_to_remove,'')
        return src_url
    #
    def get_youtube_comments(self):
        """
        Wrapper method used to return all textual information

        :return:
        """
        argparser.add_argument("--videoid", help="Required; ID for video for which the comment will be inserted.")
        argparser.add_argument("--text", help="Required; text that will be used as comment.")
        args = argparser.parse_args()
        #
        args.videoid = self.__get_video_id()
        #
        youtube = self.get_authenticated_service(args)
        try:
            video_comment_threads, comment_map = self.get_comment_threads(youtube, args.videoid)
            for i in range(len(video_comment_threads)):
                parent_id = video_comment_threads[i]["id"]
                comment_map = self.get_comments(youtube, parent_id, comment_map)
        except Exception as e:
            comment_map = None
            print(str(e))
        #
        return comment_map
    """ 
    Unused code below this line
    ---------------------------
    """
    # #
    # # Call the API's comments.insert method to reply to a comment.
    # # (If the intention is to create a new to-level comment, commentThreads.insert
    # # method should be used instead.)
    # def insert_comment(youtube, parent_id, text):
    #     insert_result = youtube.comments().insert(
    #         part="snippet",
    #         body=dict(
    #             snippet=dict(
    #                 parentId=parent_id,
    #                 textOriginal=text
    #             )
    #         )
    #     ).execute()
    #
    #     author = insert_result["snippet"]["authorDisplayName"]
    #     text = insert_result["snippet"]["textDisplay"]
    #     print("Replied to a comment for " + str(author) + ": " + str(text) + "")
    #
    # # Call the API's comments.update method to update an existing comment.
    # def update_comment(youtube, comment):
    #     comment["snippet"]["textOriginal"] = 'updated'
    #     update_result = youtube.comments().update(
    #         part="snippet",
    #         body=comment
    #     ).execute()
    #
    #     author = update_result["snippet"]["authorDisplayName"]
    #     text = update_result["snippet"]["textDisplay"]
    #     print("Updated comment for " + str(author) + ": " + str(text) + "")
    #
    # # Call the API's comments.setModerationStatus method to set moderation status of an
    # # existing comment.
    # def set_moderation_status(youtube, comment):
    #     youtube.comments().setModerationStatus(
    #         id=comment["id"],
    #         moderationStatus="published"
    #     ).execute()
    #
    #     print(comment["id"] + " moderated succesfully")
    #
    # # Call the API's comments.markAsSpam method to mark an existing comment as spam.
    # def mark_as_spam(youtube, comment):
    #     youtube.comments().markAsSpam(
    #         id=comment["id"]
    #     ).execute()
    #
    #     print(comment["id"] + " marked as spam succesfully")
    #
    # # Call the API's comments.delete method to delete an existing comment.
    # def delete_comment(youtube, comment):
    #     youtube.comments().delete(
    #         id=comment["id"]
    #     ).execute()
    #
    #     print(comment["id"] + " deleted succesfully")
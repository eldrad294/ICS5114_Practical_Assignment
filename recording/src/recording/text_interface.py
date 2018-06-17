import httplib2
import os
import sys
import requests
import time
from apiclient.discovery import build_from_document
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import argparser, run_flow
from recording.src.constants import path_consts as pc
from irc import bot


class _YouTubeInterface():
    """
    Class dedicated to interfacing with the comment extraction Youtube API
    """

    def __init__(self, config_obj):
        """
        Default Constructor

        :param config_obj:  A class structure used to contain information acquired from the input_channels.json config
                            file
        """
        self.config_obj = config_obj
        """
        The CLIENT_SECRETS_FILE variable specifies the name of a file that contains the OAuth 2.0 information for this 
        application, including its client_id and client_secret. You can acquire an OAuth 2.0 client ID and client secret 
        from the {{ Google Cloud Console }} at {{ https://cloud.google.com/console }}.
        
        Please ensure that you have enabled the YouTube Data API for your project. For more information about using 
        OAuth2 to access the YouTube Data API, see:
        https://developers.google.com/youtube/v3/guides/authentication
        
        For more information about the client_secrets.json file format, see:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """
        self.CLIENT_SECRETS_FILE = pc.FILE_YOUTUBE_API_SECRET

        """
        This OAuth 2.0 access scope allows for full read/write access to the authenticated user's account and requires 
        requests to use an SSL connection.
        """
        self.YOUTUBE_READ_WRITE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
        self.YOUTUBE_API_SERVICE_NAME = "youtube"
        self.YOUTUBE_API_VERSION = "v3"

        # This variable defines a message to display if the CLIENT_SECRETS_FILE is missing.
        self.MISSING_CLIENT_SECRETS_MESSAGE = """
        WARNING: Please configure OAuth 2.0

        To make this sample run you will need to populate the client_secrets.json file found at:
           %s
        with information from the APIs Console
        https://console.developers.google.com

        For more information about the client_secrets.json file format, please visit:
        https://developers.google.com/api-client-library/python/guide/aaa_client_secrets
        """ % os.path.abspath(os.path.join(os.path.dirname(__file__),
                                           self.CLIENT_SECRETS_FILE))

    def get_authenticated_service(self, args):
        """
        Authorize the request and store authorization credentials.
        :param args: Authentication params
        :return:
        """
        print("Authenticating with yt API..")
        flow = flow_from_clientsecrets(self.CLIENT_SECRETS_FILE, scope=self.YOUTUBE_READ_WRITE_SSL_SCOPE,
                                       message=self.MISSING_CLIENT_SECRETS_MESSAGE)

        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            # args.noauth_local_webserver = True
            credentials = run_flow(flow, storage, args)

        # Trusted testers can download this discovery document from the developers page and it should be in the same
        # directory with the code.
        with open(pc.FILE_YOUTUBE_API_V3_DISCOVERYDOCUMENT, "r", encoding='utf-8') as f:
            doc = f.read()
            return build_from_document(doc, http=credentials.authorize(httplib2.Http()))

    def get_comment_threads(self, youtube, video_ids, youtube_api_result_limit):
        """
        Call the API's commentThreads.list method to list the existing comment threads.
        :param youtube:                  YouTube session instance
        :param video_ids:                Video IDs
        :param youtube_api_result_limit: Max API results limit
        :return:                         Dictionary, representing users' comments
        """
        nextPageToken = ''
        comment_map = dict()

        for video_id in video_ids:
            while nextPageToken is not None:
                print("Retrieving a page comment thread..")
                try:
                    results = youtube.commentThreads().list(
                        part="snippet",
                        videoId=video_id,
                        textFormat="plainText",
                        maxResults=youtube_api_result_limit,
                        pageToken=nextPageToken
                    ).execute()
                    nextPageToken = results["nextPageToken"]
                except Exception as e:
                    print(str(e))
                    # Eventully nextPageToken will be returned as null and exit loop
                    nextPageToken = None
                    continue

                for item in results["items"]:
                    comment = item["snippet"]["topLevelComment"]
                    author = comment["snippet"]["authorDisplayName"]
                    text = comment["snippet"]["textDisplay"]
                    if author in comment_map:
                        comment_map[author].append(text)
                    else:
                        comment_map[author] = []
                        comment_map[author].append(text)

                    # Sleep Thread to avoid greedy consumption of resource api and get throttled
                    # time.sleep(1)

                    comment_map.update(self.get_comments(youtube=youtube,
                                                         parent_id=item['id'],
                                                         comment_map=comment_map,
                                                         youtube_api_result_limit=youtube_api_result_limit))

        return comment_map

    def get_comments(self, youtube, parent_id, comment_map, youtube_api_result_limit):
        """
        Call the API's comments.list method to list the existing comment replies.
        :param youtube:                  YouTube session instance
        :param parent_id:                Comment parent ID
        :param comment_map:              Dictionary, representing users' comments
        :param youtube_api_result_limit: Max API results limit
        :return:                         Dictionary, representing users' comments
        """
        print("Retrieving YouTube comment replies with pid [" + str(parent_id) + "]..")
        results = youtube.comments().list(
            part="snippet",
            parentId=parent_id,
            textFormat="plainText",
            maxResults=youtube_api_result_limit
        ).execute()

        for item in results["items"]:
            author = item["snippet"]["authorDisplayName"]
            text = item["snippet"]["textDisplay"]
            if author in comment_map:
                comment_map[author].append(text)
            else:
                comment_map[author] = []
                comment_map[author].append(text)

        return comment_map

    def __get_video_id(self):
        """
        Parses youtube urls and returns only the video ids
        :return: YouTube constructed video URLs
        """
        src_url_list = []
        src_urls = self.config_obj.get_details()['src']
        match_string_to_remove = "https://www.youtube.com/watch?v="
        for src in src_urls:
            src_url_list.append(src.replace(match_string_to_remove,''))
        return src_url_list

    def get_youtube_comments(self, youtube_api_result_limit):
        """
        Wrapper method used to return all textual information
        :param youtube_api_result_limit: Denotes maximum amount of results returned by YouTube API
        :return: Dictionary, representing users' comments
        """
        argparser.add_argument("--videoid", help="Required; ID for video for which the comment will be inserted.")
        argparser.add_argument("--text", help="Required; text that will be used as comment.")
        args = argparser.parse_args()

        args.videoid = self.__get_video_id()

        youtube = self.get_authenticated_service(args)
        comment_map = self.get_comment_threads(youtube=youtube,
                                               video_ids=args.videoid,
                                               youtube_api_result_limit=youtube_api_result_limit)

        return comment_map


class TwitchBot(bot.SingleServerIRCBot):
    """
    Twitch Bot Logic
    """
    def __init__(self, username, client_id, token, channel, producer_handler, kafka_config, kafka_topic):
        """
        Connects to the Twitch Channel
        :param username:          Channel username
        :param client_id:         Client ID
        :param token:             Authentication token
        :param channel:           Channel name
        :param producer_handler:  Reference to the producer handler
        :param kafka_config:      Kafka config
        :param kafka_topic:       Kafka topic
        """
        self.client_id = client_id
        self.token = token
        self.channel = '#' + channel
        self.channel_name = channel
        self.__producer_handler = producer_handler
        self.__kafka_config = kafka_config
        self.__kafka_topic = kafka_topic

        # Get the channel id, we will need this for v5 API calls
        url = 'https://api.twitch.tv/kraken/users?login=' + channel
        headers = {'Client-ID': client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
        r = requests.get(url, headers=headers).json()
        self.channel_id = r['users'][0]['_id']

        # Create IRC bot connection
        server = 'irc.chat.twitch.tv'
        port = 80
        print('Connecting to ' + server + ' on port ' + str(port) + '...')
        bot.SingleServerIRCBot.__init__(self, [(server, port, 'oauth:' + token)], username, username)

    def on_welcome(self, c, e):
        """
        This method is called when the bot connects to the streaming channel
        :param c: Twitch capabilities instance
        :param e: Unused parameter
        :return:  None
        """
        print('Joining ' + self.channel)

        # You must request specific capabilities before you can use them
        c.cap('REQ', ':twitch.tv/membership')
        c.cap('REQ', ':twitch.tv/tags')
        c.cap('REQ', ':twitch.tv/commands')
        c.join(self.channel)

    def on_pubmsg(self, c, e):
        """
        If a chat message starts with an exclamation point, try to run it as a command
            print("Author[" + e.source + "] - Message[" + e.arguments[0] + "]")
            if e.arguments[0][:1] == '!':
                cmd = e.arguments[0].split(' ')[0][1:]
                print('Received command: ' + cmd)
                self.do_command(e, cmd)

        :param c: Unused parameter
        :param e: Twitch encapsulated comments
        :return:  None
        """
        author = self.__clean_source(e.source)
        comment = e.arguments[0]
        self.__producer_handler.add_task(data=[author, comment],
                                         kafka_config=self.__kafka_config,
                                         kafka_topic=self.__kafka_topic)
        return

    def do_command(self, e, cmd):
        """
        Twitch command executer
        :param e:   Unused parameter
        :param cmd: Command string representation
        :return:    None
        """
        c = self.connection

        if cmd == "game":
            # Poll the API to get current game.
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' is currently playing ' + r['game'])
        elif cmd == "title":
            # Poll the API the get the current status of the stream
            url = 'https://api.twitch.tv/kraken/channels/' + self.channel_id
            headers = {'Client-ID': self.client_id, 'Accept': 'application/vnd.twitchtv.v5+json'}
            r = requests.get(url, headers=headers).json()
            c.privmsg(self.channel, r['display_name'] + ' channel title is currently ' + r['status'])
        elif cmd == "raffle":
            # Provide basic information to viewers for specific commands
            message = "This is an example bot, replace this text with your raffle text."
            c.privmsg(self.channel, message)
        elif cmd == "schedule":
            message = "This is an example bot, replace this text with your schedule text."
            c.privmsg(self.channel, message)
        else:
            # The command was not recognized
            c.privmsg(self.channel, "Did not understand command: " + cmd)

    def __clean_source(self, source):
        """
        Cleans Twitch Author String
        Ex: 'topkoumou!topkoumou@topkoumou.tmi.twitch.tv' into 'topkoumou'
        :param source: Author string
        :return:       Clean author string
        """
        char_index = source.find('!')
        return source[0:char_index]


class _TwitchInterface:
    """
    Class dedicated to interfacing with the live chat extraction of TwitchTV. Establishes an IRC (Internet Relay Chat)
    connection with Twitch servers, allowing the bot to connect to a desired Twitch chat and record all textual
    information passing through chat.
    """
    def __init__(self, config_obj):
        """
        Default Constructor
        :param config_obj:  A class structure used to contain information acquired from the input_channels.json config
                            file
        """
        self.__username = 'databot'                           # Name of Twitch bot - will appear using this alias in twitch chat
        self.__client_id = 'vixafhn68m11y18w6r3jhwvyhknwh1'   # Twitch secret client_id retrieved from Twitch console
        self.__token = 'ijxoygmxowpduu7iwumn7jb1t5k90r'       # Twitch Oauth toekn retrieved from Twitch console
        self.__channel = config_obj.get_details()['channel']  # Channel name with which to connect

    def start_twitch_bot(self, producer_handler, kafka_config, kafka_topic):
        """
        Initiates twitch bot
        :param producer_handler: Reference to the associated producer
        :param kafka_config:     Kafka config
        :param kafka_topic:      Kafka topic
        :return:                 None
        """
        bot = TwitchBot(self.__username,
                        self.__client_id,
                        self.__token,
                        self.__channel,
                        producer_handler,
                        kafka_config,
                        kafka_topic)
        bot.start()


class TextInterface(_YouTubeInterface, _TwitchInterface):
    """
    This class is reserved for logic pertaining to text acquisition from online resources. The logic is structured to
    serve two different modes of text gathering:

    1) Pre-recorded text acquisition - Applies to YouTube comments & comment threads only
    2) Live text acquisition - Applies to live chats which are updated in real-time.

    This class will operate on data pulled off the config_interface.
    """
    def __init__(self, config_obj):
        _YouTubeInterface.__init__(self, config_obj=config_obj)
        _TwitchInterface.__init__(self, config_obj=config_obj)

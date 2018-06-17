import json
from streamparse import Bolt
from speech_recognition.BDAGoogleStorage import BDAGoogleStorageConsume
from coding_framework.BDATextProcessing import BDATextProcessing


class VideoDecoder(Bolt):
    """
    This bolt contains the logic to recieve segmented video file paths, opens the respective file, and decodes the video
    speech audio into text.
    The decoded text is emitted to another bolt (graph_writer).
    """
    # Grouping Mechanism
    outputs = ['video']

    # Overriding Bolt Configuration
    auto_anchor = True
    auto_ack = True
    auto_fail = False

    def initialize(self, conf, ctx):
        """
        video decoder initialize method
        :param conf: Unused param
        :param ctx:  Unused param
        :return:     None
        """
        self.google_transcriber = BDAGoogleStorageConsume()

    def process(self, tup):
        """
        Decodes segment video into text, and emits that text
        :param tup:
        :return:    None
        """
        streaming_object = tup.values[0]
        streaming_object = streaming_object.replace("'", "\"")
        streaming_object = json.loads(streaming_object)

        if not streaming_object:
            return

        self.log("Received streaming object for URI: " + str(streaming_object['cloud_bucket_path']))

        try:

            decoded_video_string = self.google_transcriber.transcribe_file(streaming_object['cloud_bucket_name'],
                                                                           streaming_object['cloud_bucket_path'])

            clean_decoded_video_string = BDATextProcessing.simplify_text(decoded_video_string)

            streaming_object['text'] = clean_decoded_video_string

            self.log("Video decoding for [" + str(streaming_object['cloud_bucket_path']) +
                     "] complete - Pushing downstream.. ")
        except Exception as e:
            self.log("An exception was raised during video decoding!!")
            self.log(str(e))
            # We pass an error (dummy) string to avoid passing None values to graph writer
            streaming_object['text'] = ["?????"]
        finally:
            # Stream_obj (which is represented as a serialized dictionary) is pushed down stream through Storm, towards
            # awaiting graph_writer bolt
            self.emit([json.dumps(streaming_object)])

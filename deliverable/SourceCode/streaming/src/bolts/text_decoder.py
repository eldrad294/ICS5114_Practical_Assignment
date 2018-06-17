#
# Module Imports
from streamparse import Bolt
from speech_recognition.BDAGoogleStorage import BDAGoogleStorageConsume
from coding_framework.BDATextProcessing import BDATextProcessing
import json
#
class TextDecoder(Bolt):
    """
    This bolt contains the logic to recieve text
    [authors, comments], which are respectively
    processed, cleaned and pushed downstream.

    The decoded text is emitted to another bolt (graph_writer).
    """
    #
    # Grouping Mechanism
    outputs = ['text']
    #
    # Overriding Bolt Configuration
    auto_anchor = True
    auto_ack = True
    auto_fail = False
    #
    def initialize(self, conf, ctx):
        """
        video decoder initialize method
        :param conf:
        :param ctx:
        :return:
        """
        self.google_transcriber = BDAGoogleStorageConsume()
    #
    def process(self, tup):
        """
        Decodes segment video into text, and emits that text
        :param tup:
        :return:
        """
        streaming_object = tup.values[0]
        #
        #streaming_object = streaming_object.replace("'", "\"")
        streaming_object = json.loads(streaming_object)
        #
        if not streaming_object:
            return
        #
        self.log("Received streaming object for Author: " + str(streaming_object['viewer']))
        #
        try:
            streaming_object['viewer'] = str(streaming_object['viewer'])
            comments = "".join(streaming_object['text'])
            comments = BDATextProcessing.simplify_text(comments)
            streaming_object['text'] = comments
        except Exception as e:
            self.log("An exception was raised during text decoding!!")
            self.log(str(e))
            streaming_object['viewer'] = "??viewer??"
            streaming_object['text'] = "??text??" # We pass an error (dummy) string to avoid passing None values to graph writer
        finally:
            #
            # Stream_obj (which is represented as a serialized dictionary)
            # is pushed down stream through Storm, towards awaiting graph_writer bolt
            self.emit([json.dumps(streaming_object)])
            #
            self.log("Text cleanup for [" + str(streaming_object['viewer']) +
                     "] with comments [" + str(streaming_object['text']) +
                     "] complete - Pushing downstream.. ")

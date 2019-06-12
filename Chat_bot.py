from fbchat import Client, log
from fbchat.models import *
import apiai, codecs, json
import credentials

class JoWithME(Client):
    def apiaiCon(self):
            self.CLIENT_ACCESS_TOKEN = "Your_client_token"
            self.ai = apiai.ApiAI(self.CLIENT_ACCESS_TOKEN)
            self.request = self.ai.text_request()
            self.request.lang = 'de'
            self.request.session_id = "<SESSION ID, UNIQUE FOR EACH USER>"

    def onMessage(
        self,
        author_id=None,
        message_object=None,
        thread_id=None,
        thread_type=ThreadType.USER,
        **kwargs
    ):
        self.markAsRead(author_id)

        log.info("Message {} from {} in {}".format(message_object, thread_id, thread_type))

        self.apiaiCon()

        msgText = message_object.text

        self.request.query = msgText

        response = self.request.getresponse()

        obj = json.load(response)


        reply = obj['result']['fulfillment']['speech']
        # reply = "Sorry this is my first chatbot test. It's under development, so you might see this message over and over agian."

        if author_id != self.uid:
            self.send(Message(text=reply), thread_id = thread_id, thread_type = thread_type)

        self.markAsDelivered(author_id, thread_id)


client = JoWithME(credentials.myfb["email"], credentials.myfb["password"])
client.listen()

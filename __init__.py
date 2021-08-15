from mycroft import MycroftSkill, intent_file_handler


class Easyshopping(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('easyshopping.intent')
    def handle_easyshopping(self, message):
        self.speak_dialog('easyshopping')


def create_skill():
    return Easyshopping()


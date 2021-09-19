from json import detect_encoding
from mycroft import MycroftSkill, intent_file_handler, intent_handler
import cv2
from multiprocessing import Process
from mycroft.util import LOG
import threading
import os
import sys

sys.path.append('/opt/mycroft/skills/easyshopping-skill.camille7777')
from cvAPI import getDetail, getObjLabel

cur_img_path = '/opt/mycroft/skills/easyshopping-skill.camille7777/photo/cap_img_2.jpg'
def generate_str(possible_list):
    res = ''
    if len(possible_list) == 3:
        res = possible_list[0] + ' ' + \
            possible_list[1] + ' and ' + possible_list[2]
    elif len(possible_list) == 2:
        res = possible_list[0] + ' and ' + possible_list[1]
    elif len(possible_list) == 1:
        res = possible_list[0]

    return res
def take_photo():
    LOG.error('========================>>>>>>>>>>>>> take photo process start')
    cap = cv2.VideoCapture(0)
    img_num = 1
    flag = 0


    #<-- Take photo in specific time duration -->
    cout = 0
    while (flag != 1):
        ret, frame = cap.read()
        cv2.imshow('capture', frame)
        cout += 1 
        if cout == 50:
            img_name = 'cap_img_' + str(img_num) + '.jpg'
            img_path = os.path.join('/opt/mycroft/skills/easyshopping-skill.camille7777/photo', img_name)
            for img_num in range(1,100):
                img_name = 'cap_img_' + str(img_num) + '.jpg'
                img_path = os.path.join('/opt/mycroft/skills/easyshopping-skill.camille7777/photo', img_name)
                if not(os.path.exists(img_path)):
                    cv2.imwrite(img_path, frame)
                    flag = 1
                    cur_img_path = img_path
                    break
                else:
                    continue

        #<-- Take photo by pressing q key -->
        # if cv2.waitKey(1) & 0xFF == ord('q'):
        #     img_name = 'cap_img_' + str(img_num) + '.jpg'
        #     img_path = os.path.join('/opt/mycroft/skills/take-item-photo-skill.maoyuejingxian/photo', img_name)
        #     for img_num in range(1,100):
        #         img_name = 'cap_img_' + str(img_num) + '.jpg'
        #         img_path = os.path.join('/opt/mycroft/skills/take-item-photo-skill.maoyuejingxian/photo', img_name)
        #         if not(os.path.exists(img_path)):
        #             cv2.imwrite(img_path, frame)
        #             flag = 1
        #             break
        #         else:
        #             continue

    cap.release()
    cv2.destroyAllWindows()
    LOG.error('========================>>>>>>>>>>>>>>> take photo process end')
    os._exit(0)

class Easyshopping(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.log.error("=============================== _init_")

    def initialize(self):
        self.log.error("=============================== initialize")
        self.register_intent_file('view.goods.intent', self.handle_view_goods)
        self.register_intent_file('is.there.any.goods.intent', self.handle_is_there_any_goods)
        #self.register_entity_file('category.entity')
        #self.register_entity_file('location.entity')

    @intent_handler('view.goods.intent')
    def handle_view_goods(self, message):
        self.speak_dialog('view.goods')
        take_photo_process = Process(target=take_photo)
        take_photo_process.start()
        take_photo_process.join()
        self.speak('I find some goods here, you can ask me whatever goods you want.', expect_response=True)

    @intent_handler('is.there.any.goods.intent')
    def handle_is_there_any_goods(self, message):

        try:
            objectlist = getObjLabel.getObjectsThenLabel(cur_img_path)
            label_list = []
            loc_list = []
            detected = 0

            category_label = message.data.get('category')

            for obj in objectlist['objectList']:
                label_list.append(obj['name'])
                loc_list.append(obj['loc'])
            
            for i in range(0,len(label_list)):
                self.label_str = generate_str(label_list[i])
                self.label_str = self.label_str.lower()
                # self.log.error("=============================")
                # self.log.error(self.label_str)
                # self.log.error(loc_list)

                self.log.error(category_label)
            
                if category_label is not None:
                    if category_label in self.label_str:
                        self.speak_dialog('yes.goods',
                                        {'category': category_label,
                                        'location': loc_list[i]})
                        detected = 1
                        break
                else:
                    continue

            if detected == 0:
                self.speak_dialog('no.goods',
                {'category': category_label})

        except Exception as e:
            self.log.error("**************************###============================= Error: {0}".format(e))
            self.speak_dialog(
                "exception", {"action": "calling computer vision API"})

    def stop(self):
        pass


def create_skill():
    return Easyshopping()


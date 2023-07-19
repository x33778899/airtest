import Airtest_automated_start
from enum import IntEnum
# import test
import Json_creator


class ACTION(IntEnum):
    DEBUG = 0
    DEFAULT = 1
    TRANSLATION_STRING = 2


ACTION_TYPE = ACTION.DEBUG


def main():
    #     自動產生語系檔
    jc = Json_creator.Json_creator()
    jc.json_creator()
    automated_start = Airtest_automated_start.Airtest_automated_start()
    automated_start.start(ACTION_TYPE)


main()

print("start...")


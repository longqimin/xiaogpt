import sys
from codetiming import Timer
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.acs_exception.exceptions import ClientException
from aliyunsdkcore.acs_exception.exceptions import ServerException
from aliyunsdkalimt.request.v20181012 import TranslateGeneralRequest
import json
from typing import AsyncIterator
import time


class AlibabaMachineTranslator:
    client: AcsClient

    def __init__(self, access_id:str, access_secret_key:str, region:str="cn-hangzhou") -> None:
        self.client = AcsClient(access_id, access_secret_key, region)

    # chinese to english
    @Timer(name="alimt_translate_chinese_text", text="alimt_translate_chinese_text cost: {:0.4f} seconds")
    def chinese_to_english(self, text: str):
        # 创建request，并设置参数
        request = TranslateGeneralRequest.TranslateGeneralRequest()
        request.set_SourceLanguage("zh")  # zh or en
        request.set_SourceText(text)
        request.set_FormatType("text")
        request.set_TargetLanguage("en")
        request.set_method("POST")
        # 发起API请求并显示返回值
        try:
            response = self.client.do_action_with_exception(request)
            print(response)
            body = json.loads(response)
            return body.get("Code", "500"), body.get("Data", {}).get("Translated", "")
        except:
            return "500", ""

    # english to chinese
    @Timer(name="alimt_translate_english_text", text="alimt_translate_english_text cost: {:0.4f} seconds")
    def english_to_chinese(self, text: str):
        # 创建request，并设置参数
        request = TranslateGeneralRequest.TranslateGeneralRequest()
        request.set_SourceLanguage("en")  # zh or en
        request.set_SourceText(text)
        request.set_FormatType("text")
        request.set_TargetLanguage("zh")
        request.set_method("POST")
        # 发起API请求并显示返回值
        try:
            response = self.client.do_action_with_exception(request)
            body = json.loads(response)
            return body.get("Code", "500"), body.get("Data", {}).get("Translated", "")
        except:
            return "500", ""

    async def chinese_to_english_async(self, text: str) -> AsyncIterator[str]:
        code, message = self.chinese_to_english(text)
        print("{} chinese:{}, english={}, code={}".format(time.time(), text, message, code))
        yield str(message)
        return




def is_ascii(s):
    return all(ord(c) < 128 for c in s)


if __name__ == "__main__":
    region = "cn-hangzhou"
    access_id = ""
    access_secret_key = ""
    translator = AlibabaMachineTranslator(access_id,access_secret_key,region)

    if len(sys.argv) > 1:
        input_text = sys.argv[1]
        output_text = ""
        if is_ascii(input_text):
            code, output_text = translator.english_to_chinese(input_text)
        else:
            code, output_text = translator.chinese_to_english(input_text)

        print("[Input] : {}\n[Output]: {}".format(input_text, output_text))

    else:
        raise Exception("usage: python ali_translate.py [text]")

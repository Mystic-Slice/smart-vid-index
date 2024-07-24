from typing import List
import xml.etree.ElementTree as ET
from typing_extensions import Self

class Caption:
    def __init__(self, text, start, duration):
        self.__text = text
        self.__start = start
        self.__duration = duration

    @property
    def text(self):
        return self.__text

    @property
    def start(self):
        return self.__start

    @property
    def duration(self):
        return self.__duration

    @property
    def stop(self):
        return self.__start + self.__duration

    @property
    def is_empty(self):
        return self.__text is None or self.__text == ""
    
    def merge_caption(self, caption, max_segment_length):
        merged_time_interval = caption.stop - self.start
        if merged_time_interval > max_segment_length:
            return False
        
        self.__text += " " + caption.text
        self.__duration += caption.duration
        return True
    
    @staticmethod
    def parse_xml_caption(xml_caption: str) -> List[Self]:
        # parse xml caption and return list of Caption objects
        caption_list = [
            Caption(node.text, float(node.attrib['start']), float(node.attrib['dur']))
            for node in ET.fromstring(xml_caption)
        ]
        caption_list_filtered = list(filter(lambda x: not x.is_empty, caption_list))

        return caption_list_filtered
    
    @staticmethod
    def merge_captions(caption_list: List[Self], segment_length: int) -> List[Self]:
        # merge captions into segments of time interval of atmost segment_length
        caption_list_merged = []
        for caption in caption_list:
            if not caption_list_merged:
                caption_list_merged.append(caption)
                continue

            if not caption_list_merged[-1].merge_caption(caption, segment_length):
                caption_list_merged.append(caption)
        
        return caption_list_merged
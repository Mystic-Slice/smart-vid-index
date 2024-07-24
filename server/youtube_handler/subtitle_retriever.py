from pytubefix import YouTube
import logging

__all__ = [
    "CaptionRetriever"
]

class CaptionRetriever:
    def __init__(self, url):
        self.__url = url
        self.__video_id = url.split('=')[-1]
        self.__handler = YouTube(self.__url)

    def get_captions(self):
        if self.__handler is None:
            raise ValueError("Handler is not initialized")
        
        if self.__handler.captions is None:
            raise ValueError(f"Captions not found for the video: {self.__url}")

        return self.__handler.captions
    
    def get_english_captions(self):
        captions = self.get_captions()

        for caption in captions:
            caption_code = caption.code
            if 'en' in caption_code and not caption_code.startswith('a.'):
                logging.info(f"[id={self.__video_id}] Using manual English caption: {caption_code}")
                return captions[caption_code]
        
        if 'a.en' in captions:
            logging.info(f"[id={self.__video_id}] Using auto-generated English caption: a.en")
            return captions['a.en']
        
        logging.info(f"[id={self.__video_id}] English caption not found")
        return None
    
    def get_english_captions_xml(self):
        return self.get_english_captions().xml_captions
    
    def get_meta_data(self):
        attributes = [
            'author',
            'channel_url',
            'description',
            'length',
            'title',
            # 'keywords',
            # 'metadata'
            'video_id',
        ]
        return { attr: getattr(self.__handler, attr) for attr in attributes }
    
    
        

        


from pytubefix import YouTube, Playlist
import logging

__all__ = [
    "CaptionRetriever"
]

ATTRIBUTES = [
    'author',
    'channel_url',
    'description',
    'length',
    'title',
    # 'keywords',
    # 'metadata',
    'video_id',
]

class CaptionRetriever:    
    @staticmethod
    def get_english_captions_xml_video(video_url):
        handler = YouTube(video_url)
        video_id = handler.video_id

        if handler.captions is None:
            raise ValueError(f"Captions not found for the video: {video_url}")

        captions = handler.captions
        metadata = { attr: getattr(handler, attr) for attr in ATTRIBUTES }

        for caption in captions:
            caption_code = caption.code
            if 'en' in caption_code and not caption_code.startswith('a.'):
                logging.info(f"[id={video_id}] Using manual English caption: {caption_code}")
                return captions[caption_code].xml_captions, metadata
        
        if 'a.en' in captions:
            logging.info(f"[id={video_id}] Using auto-generated English caption: a.en")
            return captions['a.en'].xml_captions, metadata
        
        logging.info(f"[id={video_id}] English caption not found")
        return None, metadata
    
    @staticmethod
    def get_english_captions_xml_playlist(playlist_url):
        playlist = Playlist(playlist_url)
        logging.info(f"[Playlist: {playlist.playlist_id}] Found playlist with {len(playlist)} videos")
        return [
            CaptionRetriever.get_english_captions_xml_video(video_url) for video_url in playlist.video_urls
        ]
    
    @staticmethod
    def is_playlist(url):
        return 'playlist' in url
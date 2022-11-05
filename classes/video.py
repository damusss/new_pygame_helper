import pygame,os,moviepy.video.io.ImageSequenceClip

"""Contains the Video class."""

class Video:
    """
    Allows to register frames and output a video file from them.
    
    Remember to clear the saved frames to save space.
    """
    def __init__(self,frames_folder:str,fps:int,frames_extension:str="png",frames_prefix:str="video_capture_frame"):
        self.fps:int = fps
        """The speed of the video. <get>"""
        self.folder:str = frames_folder
        """The images folder name. <get>"""
        self.count:str = 0
        """How many frames have been registered yet. <get>"""
        self.extension:str = frames_extension
        """The frame data type. <get>"""
        self.prefix:str = frames_prefix
        """The frame prefix. <get>"""
        
    def save_frame(self,surface:pygame.Surface)->None:
        """Saves a surface in a folder with the appropriate name."""
        pygame.image.save(surface,f"{self.folder}/{self.prefix}{self.count}.{self.extension}")
        self.count += 1
        
    def save_video(self,filename:str="pygame_helper_video_capture.mp4")->None:
        if self.count > 0:
            """Converts the frame to a video file. Call clear_frames_from_folder after this."""
            image_files = [os.path.join(self.folder,img)
                for img in os.listdir(self.folder)
                if img.endswith(f".{self.extension}")]
            clip = moviepy.video.io.ImageSequenceClip.ImageSequenceClip(image_files, fps=self.fps)
            clip.write_videofile(filename)
        
    def clear_frames_from_folder(self)->None:
        """Deletes the frames from the drive after the video has been outputted."""
        if self.count > 0:
            for img in os.listdir(self.folder):
                if img.endswith(f".{self.extension}"):
                    os.remove(os.path.join(self.folder,img))
            self.count = 0
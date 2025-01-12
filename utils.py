"""Module with utils"""
import os

import requests

from ChromaGAN.SOURCE import config_model
from ChromaGAN.SOURCE.img_process import ImgProcess
from config_bot import Config
from interfaces.sender_interface import SenderInterface

MAX_FILE_SIZE = 100000000000
UPLOAD_POST = "https://api.imgbb.com/1/upload"

img_process = ImgProcess()
config = Config()


class Utils:
    """Class with utils"""

    def __init__(self):
        pass

    @staticmethod
    def clear_dir(file_dir):
        """Clean directory"""
        for filename in os.listdir(file_dir):
            filepath = os.path.join(file_dir, filename)
            os.remove(filepath)

    @staticmethod
    async def process_image(file_name, file_size, chat_id, sender: SenderInterface):
        """Process an image and sent to user"""
        if file_size > MAX_FILE_SIZE:
            await sender.send_message("Sorry, your photo is too big!")
        else:
            await sender.send_message("Wait, your image is processed!")
            img_process.sample_images()
            file_path = f"{config_model.OUT_DIR}/{file_name}.jpg"
            return file_path
        return None

    @staticmethod
    def clean_all_dirs():
        """Cleans dirs with black-and-white and reconstructed photos"""
        Utils.clear_dir(config_model.OUT_DIR)
        Utils.clear_dir(os.path.join(config_model.DATA_DIR, config_model.TEST_DIR))

    @staticmethod
    def save_image(file_path):
        with open(file_path, "rb") as image:
            params = {"key": config.properties["key_image_api"]}
            files = {"image": image}
            r = requests.post(UPLOAD_POST, params=params, files=files)
            json_dict = r.json()
            return json_dict["data"]["url"]

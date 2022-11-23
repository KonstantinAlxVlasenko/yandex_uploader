"""Module to upload photos to Yandex disk"""

import urllib.request
from datetime import datetime

import requests
from tqdm import tqdm


class YaUploader:
    """Class to upload photos to Yandex disk"""

    YA_URL = r'https://cloud-api.yandex.net/v1/disk/resources'

    def __init__(self, token: str):
        self.token = token
        self.headers = {
            'Authorization': token,
            'Content-Type': 'application/json',
            'Accept': 'application/json'
            }


    def folder_exist(self, ya_folder):
        """Method checks if folder ya_folder exist in Yandex disk.
        Returns if request method returns 200 code (folder exist)"""

        params = {'path': ya_folder}
        res = requests.get(self.YA_URL, headers=self.headers, params=params)
        return res.status_code == 200


    def create_folder(self, ya_folder):
        """Method creates folder ya_folder on Yandex disk if it doesn't exist.
        If folder can't be created fn throws exception with request code error"""

        if not self.folder_exist(ya_folder):
            params = {'path': ya_folder}
            res = requests.put(self.YA_URL, headers=self.headers, params=params)
            if not res.status_code in [200, 201]:
                raise Exception(f"Folder {ya_folder} can't be created on Yandex Disk"
                                f"Status code {res.status_code}" )


    def get_upload_link(self, ya_folder, ya_filename):
        """Method gets Yandex disk upload link"""

        resource_upload_url = self.YA_URL + '/' + 'upload'
        params = {'path': ya_folder + '/' + ya_filename, 'overwrite': True}
        res = requests.get(resource_upload_url, headers=self.headers, params=params)
        upload_ya_link = res.json()['href']
        return upload_ya_link


    def upload_photo(self, ya_folder, ya_filename, vk_photo_url: str):
        """Method uploads remote file to Yandex disk.
        Returns if file upload is succeed"""

        self.create_folder(ya_folder)
        upload_ya_link = self.get_upload_link(ya_folder, ya_filename)

        with urllib.request.urlopen(vk_photo_url) as vk_photo:
            res = requests.put(upload_ya_link, data=vk_photo)
        return res.status_code in [200, 201, 202]


    def upload_vk_photos(self, vk_id, vk_photos_lst, num=5):
        """Methods takes list of photos and uploads it to folder with vk_id name.
        Returns list with uploaded files details"""

        uploaded_vk_photos_lst = []
        # list with uploaded file names to avoid files with the same name
        uploaded_filename_lst = []
        ya_folder = 'id' + str(vk_id)

        # get first num photos from the sorted list
        if num >= len(vk_photos_lst):
            vk_photos_cut_lst = vk_photos_lst
        else:
            vk_photos_cut_lst = vk_photos_lst[:num]

        for _, vk_photo in zip(tqdm(range(1, len(vk_photos_cut_lst)+1),
                                desc ="Uploading VK photos to Yandex disk"),
                                vk_photos_cut_lst):
            # default filename is the number of VK likes
            ya_filename = str(vk_photo['likes_num']) + '.jpg'
            if ya_filename in uploaded_filename_lst:
                # add timestamp if file with the same name already uploaded
                dt_string = datetime.now().strftime("%d%m%Y_%H%M%S")
                ya_filename = str(vk_photo['likes_num']) + '_' + dt_string + '.jpg'
            # upload file
            if self.upload_photo(ya_folder, ya_filename, vk_photo['url']):
                # add uploaded file information
                uploaded_vk_photos_lst.append({
                    "file_name": ya_filename,
                    "size": vk_photo['size']
                    })
                uploaded_filename_lst.append(ya_filename)
        return uploaded_vk_photos_lst

"""Module to get list of photos and its details from VK profile"""

import requests


class VK:
    """Class to retreive VK profile photos details"""

    def __init__(self, vk_access_token, vk_user_id, version='5.131'):
        self.token = vk_access_token
        self.vk_id = vk_user_id
        self.version = version
        self.params = {'access_token': self.token, 'v': self.version}

    def users_info(self):
        """Method retreives user info"""

        url = 'https://api.vk.com/method/users.get'
        params = {'user_ids': self.vk_id}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_photos(self):
        """Method retreives list of photos for vk_id"""

        url = 'https://api.vk.com/method/photos.get'
        params = {'owner_id': self.vk_id, 'album_id': 'profile', 'extended': 1, 'photo_sizes': 1}
        response = requests.get(url, params={**self.params, **params})
        return response.json()

    def get_max_size_photos(self):
        """Method takes list of photos and filters photos with highest resolution"""

        vk_photos_dct = self.get_photos()
        vk_photos_lst = []

        for current_photo in vk_photos_dct['response']['items']:
            # last photo in the list has the highest resolution
            max_size_photo = current_photo['sizes'][-1]
            vk_photos_lst.append({
                'height': max_size_photo['height'],
                'width': max_size_photo['width'],
                'likes_num': current_photo['likes']['count'],
                'size': max_size_photo['type'],
                'url': max_size_photo['url']
                })
        # sort photos from highest to lowest resolution
        vk_photos_lst.sort(key=lambda dct: dct['height'] * dct['width'], reverse=True)
        return vk_photos_lst

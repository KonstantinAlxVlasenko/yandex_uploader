"""Main module to upload user VK photos to Yandex disk"""

from pprint import pprint

from tokens import VK_ACCESS_TOKEN
from vk import VK
from yandex import YaUploader


def main():
    """Main fn to get input from user with VK user id, photos quantity
    and Yandex token. Fn backing up photos from VK profile to Yandex Disk
    to VK user id folder. Returns list with backed up files"""

    print("\nVK photos backup\n")

    vk_user_id = input('VK user id: ')
    print('\n')

    photo_num = input('Photos quantity: ')
    if photo_num:
        photo_num = int(photo_num)
        print(f"Maximum {str(photo_num)} photos is going to be backed up")
    else:
        photo_num = 5
        print("Field is empty. Dafault value is 5.")
    print('\n')

    ya_disk_token = input('Yandex Disk token: ')
    print('\n')

    vk = VK(VK_ACCESS_TOKEN, vk_user_id)
    vk_photos_lst = vk.get_max_size_photos()

    ya_uploader = YaUploader(ya_disk_token)
    uploaded_vk_photos_lst = ya_uploader.upload_vk_photos(vk_user_id, vk_photos_lst, photo_num)
    print('\nUploaded files\n')
    pprint(uploaded_vk_photos_lst)
    return uploaded_vk_photos_lst


if __name__ == '__main__':
    main()

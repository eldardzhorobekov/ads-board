from django.template.defaultfilters import slugify as django_slugify
from django.core.files.uploadedfile import SimpleUploadedFile


alphabet = {'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'yo', 'ж': 'zh', 'з': 'z', 'и': 'i',
            'й': 'j', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r', 'с': 's', 'т': 't',
            'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch', 'ы': 'i', 'э': 'e', 'ю': 'yu',
            'я': 'ya'}


def slugify(s):
    """
    Overriding django slugify that allows to use russian words as well.
    """
    return django_slugify(''.join(alphabet.get(w, w) for w in s.lower()))


def get_test_image():
    """
    Get real image for testing
    """
    image_path='C:/Users/eldar/Documents/ads-board/src/static/tests/images/test_image1.jpg'
    upload_file = open(image_path, 'rb')
    return SimpleUploadedFile(name=upload_file.name, content=upload_file.read(), content_type='image/jpeg')

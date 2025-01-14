import mongoengine as me

class Image(me.Document):
    filename = me.StringField(required=True)
    image_data = me.BinaryField(required=True)
    format = me.StringField(required=True)
    size = me.DictField(required=True)  # Словарь для хранения размеров изображения
    url = me.StringField()

    meta = {
        'collection': 'images'
    }

    def save_image(self, image_data, filename, format, size, url):
        self.filename = filename
        self.image_data = image_data
        self.format = format
        self.size = size
        self.url = url
        self.save()

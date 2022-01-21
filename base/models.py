from django.db import models

class Section(models.Model):
    name = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.name

class Audio(models.Model):
    name_latin = models.CharField(max_length=100, unique=True)
    name_cyrillic = models.CharField(max_length=100, unique=True)
    audio_true = models.BooleanField('Audio')
    file = models.FileField('Audio File', upload_to='files', null=True, blank=True)
    youtube_id = models.CharField('Youtube Video Id', max_length=100, null=True, blank=True)
    section = models.ForeignKey(Section, on_delete=models.PROTECT)

    def __str__(self):
        return self.name_latin



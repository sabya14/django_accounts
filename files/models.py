from django.db import models
from django.core.urlresolvers import reverse
from picklefield.fields import PickledObjectField
from django.contrib.auth.models import User


def data_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/year/month/date/genre/slug
    return 'data/{username}/{name}'.format(
        name=filename,
        username=instance.user.username

    )


class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='file')
    name = models.CharField(max_length=255)
    collection = models.CharField(max_length=255)
    database = models.CharField(max_length=255)
    timestamp = models.DateTimeField(auto_now_add=True)
    file_name = models.CharField(max_length=255)
    file = models.FileField(upload_to=data_directory_path, null=True)
    headers_list = PickledObjectField()

    class Meta:
        unique_together= ['name', 'user']
        ordering = ['-timestamp']

    def __unicode__(self):
        return self.id

    def __str__(self):
        return str(self.id)

    def get_absolute_url(self):
        return reverse("files:update", kwargs={"pk": self.id})

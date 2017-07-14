# coding=utf-8
from django.core.files.uploadedfile import UploadedFile


class MemoryFile(UploadedFile):
    def open(self, *args, **kwargs):
        self.file.seek(0)

    def chunks(self, *args, **kwargs):
        self.file.seek(0)
        yield self.read()

    def multiple_chunks(self, *args, **kwargs):
        return False

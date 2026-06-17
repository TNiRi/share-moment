from werkzeug.utils import secure_filename

from models.marker_photo import MarkerPhotoUploadDto
from storages.abstract_file_storage import AbstractFileStorage


class OnlyPhotoCanBeUploadError(Exception):
    def __init__(self):
        super().__init__("Можно загружать только фото")


class MarkerPhotoFileStorage(AbstractFileStorage):

    def upload_file(self, upload_dto: MarkerPhotoUploadDto) -> str:
        self.check_and_create_dir("src")
        fpath = f"src/{upload_dto.marker_id}"
        self.check_and_create_dir(fpath)

        upload_dto.file.filename = self.preprocess_rus_file_name(upload_dto.file.filename)
        upload_dto.file.filename = secure_filename(upload_dto.file.filename)
        if not self.check_file_type(upload_dto.file.filename, upload_dto.file.mimetype, ["jpeg", "jpg", "png"]):
            raise OnlyPhotoCanBeUploadError()
        upload_dto.file.filename = self.check_unique_file_name_ts(upload_dto.file.filename)

        filepath = f"{fpath}/{upload_dto.file.filename}"
        upload_dto.file.save(filepath)
        return filepath
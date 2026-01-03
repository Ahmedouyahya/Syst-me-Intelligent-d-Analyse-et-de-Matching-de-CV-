import os
import uuid
from werkzeug.utils import secure_filename

def save_uploaded_file(file, upload_folder):
    """
    Saves an uploaded file to the specified folder with a unique name.
    """
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)
        
    filename = secure_filename(file.filename)
    unique_filename = f"{uuid.uuid4().hex}_{filename}"
    file_path = os.path.join(upload_folder, unique_filename)
    file.save(file_path)
    return file_path

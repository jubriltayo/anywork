from django.core.exceptions import ValidationError
import os



def validate_file_size(value):
    """
    Ensure file size is not more than 10MB
    """
    filesize = value.size
    if filesize > 10 * 1024 * 1024:
        raise ValidationError("The maximum file size that can be uploaded is 10MB.")
    
def validate_file_extension(value):
    """
    Ensure the file is a pdf 
    """
    extension = os.path.splitext(value.name)[1]
    valid_extensions = ['.pdf']
    if not extension.lower() in valid_extensions:
        raise ValidationError('Only PDF files are allowed.')

def image_extension(value):
    import os 
    from django.core.exceptions import ValidationError
    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.jpg', '.png', '.gif']
    if not ext.lower() in valid_extensions:
        raise ValidationError("Unsupported file extension. Supports only ('.jpg', '.png', '.gif')")


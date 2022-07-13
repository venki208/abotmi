def path_to_upload(instance, filename):
    '''
    This method returns the path to
    store the uploaded file based on its type image or document
    '''
    if 'UploadImage' in instance.__str__():
        return os.path.join('images', str(instance.project_id), filename)
    elif 'UploadFile' in instance.__str__():
        return os.path.join('documents', str(instance.project_id), filename)

"""
catch error => write into error file
"""


def write(msg, file_path=None):
    if file_path is None:
        import settings
        file_path = settings.ErrorHandler
        file_path = settings.ErrorHandler.error_file_path
    with open(file_path, mode='w') as file:
        s = str(msg) + '\n'
        file.write(s)

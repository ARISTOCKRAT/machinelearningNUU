"""
catch error => write into error file
"""


def write(msg, st=None, *_, file_path=None):
    import datetime
    import settings
    # TODO: need get st as arg!!
    if st is None:
        st = settings.AllSettings()
        # file_path =
        # file_path = settings.ErrorHandler
        # file_path = settings.ErrorHandler.error_file_path
    with open(st.path.error_log, mode='a+') as file:
        s = str(datetime.datetime.now()) + "\n" + str(msg) + '\n'
        file.write(s)

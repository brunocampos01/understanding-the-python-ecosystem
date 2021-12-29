c.NotebookApp.ip = '0.0.0.0'

# The port the notebook server will listen on
c.NotebookApp.port = 8888

# Whether to open in a browser after starting
c.NotebookApp.open_browser = False

# Set the Access-Control-Allow-Credentials: true header
c.NotebookApp.allow_password_change = False

# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False

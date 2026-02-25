c.ServerApp.ip = '0.0.0.0'

# The port the notebook server will listen on
c.ServerApp.port = 8888

# Whether to open in a browser after starting
c.ServerApp.open_browser = False

# Set the Access-Control-Allow-Credentials: true header
c.ServerApp.allow_password_change = False

# https://github.com/jupyter/notebook/issues/3130
c.FileContentsManager.delete_to_trash = False

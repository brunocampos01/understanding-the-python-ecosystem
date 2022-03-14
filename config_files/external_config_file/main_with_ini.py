import configparser

config = configparser.ConfigParser()
config.read('config.ini')

secret_key = config['DEFAULT']['SECRET_KEY']    # 'secret-key-of-myapp'
ci_hook_url = config['CI']['HOOK_URL']  # 'web-hooking-url-from-ci-service'

# other form
secret_key = config.get("DEFAULT", "SECRET_KEY")
ci_hook_url = config.get('CI', 'HOOK_URL')

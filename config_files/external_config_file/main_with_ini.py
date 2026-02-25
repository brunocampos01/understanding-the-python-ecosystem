import configparser

config = configparser.ConfigParser()
config.read('config.ini')

# Access values via bracket notation
secret_key = config['DEFAULT']['SECRET_KEY']    # 'secret-key-of-myapp'
ci_hook_url = config['CI']['HOOK_URL']  # 'web-hooking-url-from-ci-service'

# Alternative: access values via .get() method
secret_key_alt = config.get("DEFAULT", "SECRET_KEY")
ci_hook_url_alt = config.get('CI', 'HOOK_URL')

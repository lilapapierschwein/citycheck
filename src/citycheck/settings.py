from citycheck.core.utils.config import load_config

# WARN: since we are recursively searching for a match in the current wd and its subdirs
# we might get multiple hits, which might result in unintented settings being applied.
# however, if you are fine with this, you might want to set the `allow_multiple` option
# in the `load_config` function to `True`. this will select the first match we find,
# starting from our cwd downwards.
CONFIG_FILE_NAME = "config.toml"
APP_CONFIG = load_config(CONFIG_FILE_NAME)

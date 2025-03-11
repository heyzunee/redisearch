from environs import Env

env = Env()
env.read_env()

REDIS_HOST = env.str("REDIS_HOST")
REDIS_PORT = env.str("REDIS_PORT")
REDIS_USERNAME = env.str("REDIS_USERNAME")
REDIS_PASSWORD = env.str("REDIS_PASSWORD")
PROJECT_NAME = "copilot-example"

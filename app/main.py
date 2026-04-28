from loguru import logger

from uuid import uuid4

APP_NAME = "ai_hedge_fund"
USER_ID = str(uuid4())
SESSION_ID = str(uuid4())


def main():
    logger.info(f"App name: {APP_NAME}")
    logger.info(f"User ID: {USER_ID}")
    logger.info(f"Session ID: {SESSION_ID}")


if __name__ == "__main__":
    main()

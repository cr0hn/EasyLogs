import os

from easy_logs.setup import setup_app

app = setup_app()


if __name__ == '__main__':
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 8080))
    )


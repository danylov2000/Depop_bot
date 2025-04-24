from flask import Flask, request, Response
import logging

logging.basicConfig(level=logging.INFO,
                    format='[%(asctime)s] %(levelname)s - %(message)s',
                    datefmt='%H:%M:%S')

logger = logging.getLogger(__name__)

storage = []

app = Flask("Depop")


@app.route("/count")
def storage_count():
    count = len(storage)
    response = Response(str(count), 201)
    return response


@app.route("/publish", methods=["POST"])
def save_message():
    message = request.data
    storage.append(message)
    response = Response("Ok", 201)
    logger.info(f"{message} was posted to queue")

    return response


@app.route("/get")
def get_message():
    try:
        message = storage.pop(0)
        response = Response(message, 200)
        logger.info(f"{message} was taken and removed from the queue")
        return response
    except IndexError:
        response = Response("No more messages to get", 404)
        logger.info(f"No more messages to get from the queue. {len(storage)}")
        return response


if __name__ == "__main__":
    app.run(debug=True)

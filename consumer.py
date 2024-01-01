import json
import os
import sys

import pika
from mongoengine import connect

from producer import Contact

# MongoDB connection:
try:
    connect(
        db="WEB_HW_08",
        host="mongodb+srv://rabtsunvadim:UralM671976@vadimr89.hrio2i2.mongodb.net/?retryWrites=true&w=majority",
    )
except Exception as e:
    print(f"the error {e} occured")


def sender():
    pass


def main():
    # RabbitMQ connection:
    credentials = pika.PlainCredentials(username="guest", password="guest")
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host="localhost", port=5672, credentials=credentials)
    )
    channel = connection.channel()
    channel.queue_declare(queue="contacts_queue")
    print("RabbitMQ connected")

    # Callback function for handling messages
    def callback(ch, method, properties, body):
        data = json.loads(body)
        contact_id = data.get("contact_id")
        # Simulate email sending
        sender()

        contact = Contact.objects.get(id=contact_id)
        contact.message_sent = True
        contact.save()

        print(f"Message sent to {contact.full_name}")

    # listen for messages mode:
    channel.basic_consume(
        queue="contacts_queue", on_message_callback=callback, auto_ack=True
    )
    print("Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Message sending was interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)

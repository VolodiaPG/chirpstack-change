import grpc
import os
from chirpstack_api import api  # type: ignore
from dotenv import dotenv_values

# Configuration.
config = dotenv_values(".env")
config = {
    **dotenv_values(".env"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

server = config["SERVER"]
api_token = config["API_TOKEN"]
dev_eui = config["DEV_EUI"]

if __name__ == "__main__":
    # Connect without using TLS.
    channel = grpc.insecure_channel(server)

    # Device-queue API client.
    client = api.DeviceServiceStub(channel)

    # Define the API key meta-data.
    auth_token = [("authorization", "Bearer %s" % api_token)]

    # Construct request.
    req = api.EnqueueDeviceQueueItemRequest()
    req.queue_item.confirmed = False
    req.queue_item.data = bytes([0x01, 0x02, 0x03])
    req.queue_item.dev_eui = dev_eui
    req.queue_item.f_port = 10

    resp = client.Enqueue(req, metadata=auth_token)

    # Print the downlink id
    print(resp.id)

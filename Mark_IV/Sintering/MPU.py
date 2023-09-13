import usb.core
import usb.util


def read_data():
    # Find the USB device
    dev = usb.core.find(idVendor=0x1a86, idProduct=0x7523)

    # Check if the device is found
    if dev is None:
        raise ValueError("USB device not found")

    # Set up the configuration
    dev.set_configuration()

    # Find the data endpoint (assuming it's an IN endpoint)
    endpoint = dev[0][(0, 0)][0]

    # Read data from the USB device
    data = dev.read(endpoint.bEndpointAddress, endpoint.wMaxPacketSize)

    # Process the data as needed
    print(data)

def main():
    read_data()

if __name__ == "__main__":
    main()
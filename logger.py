import asyncio
from bleak import BleakClient, discover


TX_UUID = "a6ed0202-d344-460a-8075-b9e8ec90d71b"

def notification_handler(sender, data):
    text = data.decode('utf-8')
    print(text, end='')

    # Appending to file
    with open("log.txt", 'a') as log_file:
        log_file.write(text)


async def main():
    print(f"Scan devices...")
    counter = 0
    devices = await discover(timeout=10)
    for d in devices:
        if d.name != None:
            print(f"{counter}. {d.name}, MAC: {d.address}")
        counter += 1

    print(f"connect to device: ", end='')
    num = int(input())
    print()


    async with BleakClient(devices[num].address, timeout=30) as client:
        print(f"Connected: {client.is_connected}")

        await client.start_notify(TX_UUID, notification_handler)

        while True:
            await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(main())

import pandas as pd
from pythonosc.dispatcher import Dispatcher
from pythonosc.osc_server import BlockingOSCUDPServer


df = pd.DataFrame(data=None, index=None, columns=['headtracker', 'angle'])


def print_handler(address, *args):
    print(f"{address}: {args}")
    global df
    df = df.append({'headtracker': address, 'angle': args[0]}, ignore_index=True)
    df.to_csv('.\\df_mac.csv')


def default_handler(address, *args):
    print(f"DEFAULT {address}: {args}")


dispatcher = Dispatcher()
dispatcher.map("/SceneRotator1/yaw", print_handler)
dispatcher.map("/SceneRotator2/yaw", print_handler)
dispatcher.map("/SceneRotator3/yaw", print_handler)

server = BlockingOSCUDPServer(("127.0.0.1", 7000), dispatcher)
server.serve_forever()  # Blocks forever

#####
from random import randrange

from PeerFactory import PatientFactory
from config import Config
from server import Server


def mpc_algo(value, parts):
    shares = [round(value / parts)] * parts
    remainder = value % parts

    for _ in range(remainder):
        sel_share_idx = randrange(0, len(shares))
        shares[sel_share_idx] += 1

    return shares


# main method
def main():
    config = Config()
    factory = PatientFactory()
    server = Server(config, factory)
    server.start()
    server.wait_for_peers()

    # patients
    if int(config.peer_id) != 0:

        # Three-Party Computation - addition
        # input
        val = mpc_algo(randrange(25, 100), config.peer_amount)
        server.send_message_to_peer(1, str(val[1]))
        server.send_message_to_peer(2, str(val[2]))

        # addition
        p2 = server.get_message_from_peer(1)
        p3 = server.get_message_from_peer(2)
        out = val[0] + int(p2) + int(p3)

        # output
        server.send_message_to_peer(0, str(out))
        print(f"val: {val}, p2: {p2}, p3: {p3}, out: {out}")

    # hospital
    else:

        # output
        out1 = server.get_message_from_peer(0)
        out2 = server.get_message_from_peer(1)
        out3 = server.get_message_from_peer(2)

        # aggregated value
        total = int(out1) + int(out2) + int(out3)
        print(f"out1: {out1}, out2: {out2}, out3: {out3}, aggr: {total}")


# main call
if __name__ == "__main__":
    main()

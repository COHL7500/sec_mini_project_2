from random import randrange

from PeerFactory import PatientFactory
from config import Config
from server import Server

config = Config()


def mpc_algo(value: int, parts: int):
    shares = [randrange(config.p_rand_max) for _ in range(parts)]
    remainder = value - sum(shares) % config.p_rand_max

    for i in range(remainder):
        sel_share_idx = randrange(parts)
        shares[sel_share_idx] = (shares[sel_share_idx] + 1) % config.p_rand_max

    '''
    shares = [round(value / parts)] * parts
    remainder = value % parts

    for _ in range(remainder):
        sel_share_idx = randrange(0, len(shares))
        shares[sel_share_idx] += 1
    '''
    return shares


# main method
def main():
    factory = PatientFactory()
    server = Server(config, factory)
    server.start()
    server.wait_for_peers()

    # If not hospital (patient)...
    if int(config.peer_id) != 0:

        # Performing MPC computation
        mpc_res = mpc_algo(randrange(2, config.p_rand_max), config.peer_amount)
        server.send_message_to_peer(1, str(mpc_res[1]))
        server.send_message_to_peer(2, str(mpc_res[2]))

        # addition
        p2_message = server.get_message_from_peer(1)
        p3_message = server.get_message_from_peer(2)
        result = (mpc_res[0] + int(p2_message) + int(p3_message)) % config.p_rand_max

        # output
        server.send_message_to_peer(0, str(result))
        print(f"mpc_res: {mpc_res}, p2: {p2_message}, p3: {p3_message}, out: {result}")

    # ...Otherwise (hospital)
    else:

        p1_calc = server.get_message_from_peer(0)
        p2_calc = server.get_message_from_peer(1)
        p3_calc = server.get_message_from_peer(2)

        # aggregated value
        total = (int(p1_calc) + int(p2_calc) + int(p3_calc)) % config.p_rand_max
        print(f"out1: {p1_calc}, out2: {p2_calc}, out3: {p3_calc}, aggr: {total}")


# main call
if __name__ == "__main__":
    main()

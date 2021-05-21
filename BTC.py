from DarkWebHelpers.DataTracker.BitCoinTracker import Track
from DarkWebHelpers.db.DB_Handler import SQL_Manger
from DarkWebHelpers.app import AppConfigurations

config = AppConfigurations()


def FixAddress(raw_data):
    addresses = []
    if len(raw_data) != 2 or 0:
        for sub_address in raw_data.replace('[', '').replace(']', '').split(','):
            config.debug(str(sub_address).replace('"', ''))
            addresses.append(str(sub_address).replace('"', ''))
    return addresses


def Run():
    db = SQL_Manger()
    btc_reader = db.ReadBTC()
    for row_data in btc_reader:
        address, keyword, user_id = row_data
        config.debug("The owner of the addresses is {} for keyword: {}".format(user_id, keyword))
        for btc_addreass in FixAddress(address):
            track = Track(btc_addreass)
            if track.track():
                config.debug(track.result)
                if db.DoseBTCExist(address=btc_addreass):
                    db.UpdateBTC(address=track.result['address'],
                                 total_received=track.result['total_received'],
                                 total_sent=track.result['total_sent'], balance=track.result['balance']
                                 , unconfirmed_balance=track.result['unconfirmed_balance'],
                                 final_balance=track.result['final_balance'], n_tx=track.result['n_tx'],
                                 unconfirmed_n_tx=track.result['unconfirmed_n_tx'],
                                 final_n_tx=track.result['final_n_tx'], user_id=user_id)
                    config.debug("Updating address: {} ".format(""))
                else:
                    db.InsertBTC(keyword=keyword, address=track.result['address'],
                                 total_received=track.result['total_received'],
                                 total_sent=track.result['total_sent'], balance=track.result['balance']
                                 , unconfirmed_balance=track.result['unconfirmed_balance'],
                                 final_balance=track.result['final_balance'], n_tx=track.result['n_tx'],
                                 unconfirmed_n_tx=track.result['unconfirmed_n_tx'],
                                 final_n_tx=track.result['final_n_tx'], user_id=user_id)
                    config.debug("Inserting A new BTC Info")
            else:
                config.debug('Not Valid Address: {}'.format(address[0]))

    exit(0)
Run()

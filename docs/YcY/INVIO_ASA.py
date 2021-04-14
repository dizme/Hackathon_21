import json
from algosdk.v2client import algod
from algosdk import account, mnemonic
from algosdk.future.transaction import AssetConfigTxn, AssetTransferTxn, AssetFreezeTxn
from algosdk.future import transaction

# =====================================================================================
# ==================================== METODI =========================================

def wait_for_confirmation(client, txid):
    """
    Utility function to wait until the transaction is
    confirmed before proceeding.
    """
    last_round = client.status().get('last-round')
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get('confirmed-round') and txinfo.get('confirmed-round') > 0):
        print("Waiting for confirmation")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print("Transaction {} confirmed in round {}.".format(txid, txinfo.get('confirmed-round')))
    return txinfo

#   Utility function used to print created asset for account and assetid
def print_created_asset(algodclient, account, assetid):    
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then use 'account_info['created-assets'][0] to get info on the created asset
    account_info = algodclient.account_info(account)
    idx = 0;
    for my_account_info in account_info['created-assets']:
        scrutinized_asset = account_info['created-assets'][idx]
        idx = idx + 1       
        if (scrutinized_asset['index'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['index']))
            print(json.dumps(my_account_info['params'], indent=4))
            break

#   Utility function used to print asset holding for account and assetid
def print_asset_holding(algodclient, account, assetid):
    # note: if you have an indexer instance available it is easier to just use this
    # response = myindexer.accounts(asset_id = assetid)
    # then loop thru the accounts returned and match the account you are looking for
    account_info = algodclient.account_info(account)
    idx = 0
    for my_account_info in account_info['assets']:
        scrutinized_asset = account_info['assets'][idx]
        idx = idx + 1        
        if (scrutinized_asset['asset-id'] == assetid):
            print("Asset ID: {}".format(scrutinized_asset['asset-id']))
            print(json.dumps(scrutinized_asset, indent=4))
            break


# =====================================================================================
# =====================================================================================
# ============================= INPUT PARAMETRI =======================================


frase_ripristino = input('Frase di ripristino account creatore: ')
account_creatore = {}
account_creatore['chiave_pubblica'] = mnemonic.to_public_key(frase_ripristino)
account_creatore['chiave_privata'] = mnemonic.to_private_key(frase_ripristino)

asset_id = input('Asset ID: ')
asset_id = int(asset_id)

account_ricevente= input('Indirizzo ricevente: ')
account_ricevente = str(account_ricevente)

algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"

# Initialize an algod client
algod_client = algod.AlgodClient(algod_token=algod_token, algod_address=algod_address)

params = algod_client.suggested_params()
params.fee = 1000
params.flat_fee = True


# =========================== DEFREEZ RECEVER ACCOUNT  ================================


txn_1 = AssetFreezeTxn(
    sender=account_creatore['chiave_pubblica'],
    sp=params,
    index=asset_id,
    target=account_ricevente,
    new_freeze_state=False   
    )

# ========================= SEND ASA TO RECEVER ACCOUNT  ==============================

# transfer asset of 10 from account 1 to account 3
params = algod_client.suggested_params()
# comment these two lines if you want to use suggested params
params.fee = 1000
params.flat_fee = True
txn_2 = AssetTransferTxn(
    sender=account_creatore['chiave_pubblica'],
    sp=params,
    receiver=account_ricevente,
    amt=1,
    index=asset_id)


# ============================= FREEZ RECEVER ACCOUNT  ================================

txn_3 = AssetFreezeTxn(
    sender=account_creatore['chiave_pubblica'],
    sp=params,
    index=asset_id,
    target=account_ricevente,
    new_freeze_state=True   
    )


# ============================== GROUP TRANSACTIONS  ==================================
# get group id and assign it to transactions
gid = transaction.calculate_group_id([txn_1, txn_2, txn_3])
txn_1.group = gid
txn_2.group = gid
txn_3.group = gid

# ============================== SING TRANSACTIONS  ==================================
stxn_1 = txn_1.sign(account_creatore['chiave_privata'])
stxn_2 = txn_2.sign(account_creatore['chiave_privata'])
stxn_3 = txn_3.sign(account_creatore['chiave_privata'])

# ========================= assemble transaction group ================================
signed_group =  [stxn_1, stxn_2, stxn_3]


# ======================================= SEND ========================================
tx_id = algod_client.send_transactions(signed_group)

# wait for confirmation
wait_for_confirmation(algod_client, tx_id) 

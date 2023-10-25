import subprocess
from multiprocessing import Pool

print("Github: @kayaaicom")

##python Copy code input_file = r'C:\path\to\your\bitcoin_addresses.txt' output_file = r'C:\path\to\your\log.txt' These variables specify the path to the file with the input addresses and the path to the file where the results will be saved.
input_file = r'C:\path\to\your\bitcoin_addresses.txt'
output_file = r'C:\path\to\your\log.txt'

def check_balance(address):
    ##Enter the directory where electrumun is installed and the exe name in this field.
    result = subprocess.run(['C:\Program Files (x86)\Electrum\electrum-4.4.5.exe', 'getaddressbalance', address], capture_output=True, text=True)

    if result.returncode == 0:
        return True, result.stdout.strip()
    else:
        return False, result.stderr.strip()

def log_result(result):
    success, address, message = result

    if success:
        balance_info = eval(message)
        confirmed = float(balance_info['confirmed'])
        log_message = f"Address: {address}, Balance: {confirmed} BTC"
        print("Checking Kaya AI:", address)
    else:
        log_message = f"Address: {address}, Error: {message}"

    with open(output_file, 'a') as log:
        log.write(log_message + '\n')

    print(log_message)

def worker(address):
    success, message = check_balance(address)
    return success, address, message

if __name__ == '__main__':
    with open(input_file, 'r') as f:
        addresses = f.read().splitlines()

    pool = Pool(5)
    for address in addresses:
        pool.apply_async(worker, args=(address,), callback=log_result)

    pool.close()
    pool.join()

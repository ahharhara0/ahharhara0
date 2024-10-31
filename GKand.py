import os
from multiprocessing import Pool, Manager
from eth_keys import keys
from eth_utils import keccak
import time

def generate_private_key():
    """توليد مفتاح خاص عشوائي."""
    return os.urandom(32)

def private_key_to_public_key(private_key):
    """تحويل المفتاح الخاص إلى مفتاح عام."""
    return keys.PrivateKey(private_key).public_key

def public_key_to_eth_address(public_key):
    """تحويل المفتاح العام إلى عنوان Ethereum."""
    public_key_bytes = public_key.to_bytes()
    keccak_hash = keccak(public_key_bytes[1:])  # استخدم الجزء الثاني من المفتاح العام
    return '0x' + keccak_hash[-20:].hex()

def load_target_addresses(filename):
    """تحميل العناوين المستهدفة من ملف."""
    with open(filename, 'r') as f:
        return {line.strip() for line in f}

def save_match(address, private_key, filename='matched_keys.txt'):
    """حفظ عنوان متطابق مع المفتاح الخاص في ملف."""
    with open(filename, 'a') as f:
        f.write(f'{address} -> {private_key.hex()}\n')

def generate_and_compare_keys(target_addresses, matches_count, generated_count):
    """توليد المفاتيح الخاصة ومقارنة العناوين."""
    while True:  # حلقة لا نهائية
        private_key = generate_private_key()
        public_key = private_key_to_public_key(private_key)
        eth_address = public_key_to_eth_address(public_key)

        generated_count['count'] += 1  # زيادة عدد المفاتيح المولدة
        if generated_count['count'] % 1000 == 0:
            print(f'تم توليد {generated_count["count"]} مفتاح')

        if eth_address in target_addresses:
            matches_count['count'] += 1  # زيادة عدد المطابقات
            print(f'تم العثور على تطابق: {eth_address} -> {private_key.hex()}')
            save_match(eth_address, private_key)  # حفظ المطابقة مباشرة

def worker(target_addresses, matches_count, generated_count):
    """وظيفة العامل لتوليد المفاتيح."""
    generate_and_compare_keys(target_addresses, matches_count, generated_count)

if __name__ == '__main__':
    manager = Manager()
    matches_count = manager.dict()
    matches_count['count'] = 0  # عدد المطابقات
    generated_count = manager.dict()
    generated_count['count'] = 0  # عدد المفاتيح المولدة
    target_addresses = load_target_addresses('target_addresses.txt')

    # عدد العمليات (يمكنك تعديل العدد بناءً على عدد الأنوية في جهازك)
    num_processes = os.cpu_count()

    print("بدء توليد المفاتيح...")
    start_time = time.time()  # بدء التوقيت
    with Pool(processes=num_processes) as pool:
        pool.starmap(worker, [(target_addresses, matches_count, generated_count)] * num_processes)

    elapsed_time = time.time() - start_time  # حساب الوقت المستغرق
    print(f'الوقت المستغرق: {elapsed_time:.2f} ثانية')
    print(f'عدد المفاتيح المولدة: {generated_count["count"]}')
    print(f'عدد المطابقات: {matches_count["count"]}')

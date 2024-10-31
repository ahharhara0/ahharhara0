import os
from eth_keys import keys
from eth_utils import keccak
import time

# دالة لتوليد مفتاح خاص وعنوانه
def generate_key_and_address(_):
    private_key = keys.PrivateKey(os.urandom(32))  # توليد مفتاح خاص عشوائي
    public_key = private_key.public_key  # حساب المفتاح العام
    address = public_key.to_checksum_address()  # حساب عنوان الإيثريوم
    return private_key, address

# دالة لحفظ المفاتيح والعناوين في ملف
def save_keys_to_file(filename, keys_and_addresses):
    with open(filename, 'a') as file:
        for private_key, address in keys_and_addresses:
            file.write(f"Private Key: {private_key}\nAddress: {address}\n\n")

# دالة لتوليد عدد معين من المفاتيح وحفظها
def generate_and_save_keys(num_keys, filename):
    keys_and_addresses = []
    for _ in range(num_keys):
        keys_and_addresses.append(generate_key_and_address(_))
        
        # تحقق من عدد المفاتيح المولدة
        if len(keys_and_addresses) % 1000 == 0:
            print(f"تم توليد {len(keys_and_addresses)} مفتاحًا حتى الآن.")
            # حفظ المفاتيح في الملف
            save_keys_to_file(filename, keys_and_addresses)
            keys_and_addresses = []  # إعادة تعيين القائمة

    # حفظ أي مفاتيح متبقية في الملف
    if keys_and_addresses:
        save_keys_to_file(filename, keys_and_addresses)

# نقطة دخول البرنامج
if __name__ == '__main__':
    try:
        num_keys_to_generate = int(input("أدخل عدد المفاتيح المراد توليدها: "))
        if num_keys_to_generate <= 0:
            raise ValueError("يجب أن يكون العدد أكبر من 0.")
    except ValueError as e:
        print(f"خطأ: {e}. يجب إدخال عدد صحيح.")
    else:
        output_file = "keys_and_addresses.txt"
        
        start_time = time.time()
        
        # توليد المفاتيح
        generate_and_save_keys(num_keys_to_generate, output_file)

        end_time = time.time()
        print(f"تم توليد {num_keys_to_generate} مفتاحًا في {end_time - start_time:.2f} ثانية.")

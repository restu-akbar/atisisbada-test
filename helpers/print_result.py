import os
from datetime import datetime


def print_result(actual, expected, test_name="TEST_CASE"):
    write_to_log(actual, expected, test_name)
    status = "success" if actual == expected else "failed"
    symbol = "[✅]" if status == "success" else "[❌]"

    print(f"actual  : {actual}")
    print(f"expected: {expected}")
    print(f"status  : {status}")

    if status == "failed":
        print(f"{symbol} {test_name} gagal")
    else:
        print(f"{symbol} {test_name} berhasil")
    print("========================================================================")


def write_to_log(actual, expected, test_name="TEST_CASE"):
    log_dir = "logs"
    os.makedirs(log_dir, exist_ok=True)

    # Use a single log file
    log_file = os.path.join(log_dir, "test_log.txt")

    status = "success" if actual == expected else "failed"
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(log_file, "a") as f:
        f.write(f"[{timestamp}] {test_name}\n")
        f.write(f"actual  : {actual}\n")
        f.write(f"expected: {expected}\n")
        f.write(f"status  : {status}\n")
        f.write(f"{test_name} {'berhasil' if status == 'success' else 'gagal'}\n")
        f.write(
            "========================================================================\n"
        )


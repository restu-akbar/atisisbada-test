def print_result(actual, expected, test_name="TEST_CASE"):
    status = "success" if actual == expected else "failed"
    symbol = "[✅]" if status == "success" else "[❌]"

    print(f"actual  : {actual}")
    print(f"expected: {expected}")
    print(f"status  : {status}")

    if status == "failed":
        raise AssertionError(f"{symbol} {test_name} gagal")
    else:
        print(f"{symbol} {test_name} berhasil")
    print("========================================================================")

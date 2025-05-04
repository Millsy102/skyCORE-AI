def run_all_tests():
    try:
        from tests.test_boot import test_boot
        test_boot()
    except ImportError:
    except Exception as e:

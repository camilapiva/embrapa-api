from app.logging.logger import setup_logger


def test_setup_logger_multiple_calls():
    """
    Should not add multiple handlers when logger is called more than once.
    """
    logger1 = setup_logger("my_test_logger")
    logger2 = setup_logger("my_test_logger")
    assert logger1 is logger2

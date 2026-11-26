from shortener.utils import ALPHABET, CODE_LENGTH, generate_code


def test_default_length():
    assert len(generate_code()) == CODE_LENGTH


def test_custom_length():
    assert len(generate_code(12)) == 12


def test_only_uses_allowed_alphabet():
    assert set(generate_code(500)) <= set(ALPHABET)


def test_codes_differ():
    codes = {generate_code() for _ in range(100)}
    assert len(codes) == 100

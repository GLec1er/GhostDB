import subprocess


def test_ghostdb():
    # Запускаем cli.py как CLI
    result = subprocess.run(
        ['python', 'cli.py', '--script', 'tests.txt'],
        capture_output=True,
        text=True
    )

    with open('output.txt') as f:
        expected_output = f.read().strip().splitlines()

    actual_output = [line for line in result.stdout.strip().splitlines() if not line.startswith('>')]

    assert actual_output == expected_output, (
            "\nEXPECTED:\n" + "\n".join(expected_output) +
            "\n\nACTUAL:\n" + "\n".join(actual_output)
    )

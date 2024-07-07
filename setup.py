from setuptools import setup, find_packages

setup(
    name='tgconsole',
    version='1.0.0',
    packages=find_packages(),
    install_requires=[
        'pyTelegramBotAPI',
    ],
    entry_points={
        'console_scripts': [
            'tgconsole=tgconsole.bot:main',
        ],
    },
)

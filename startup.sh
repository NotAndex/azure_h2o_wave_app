#! /bin/bash
export H2O_WAVE_ADDRESS="http://127.0.0.1:${PORT}"
echo $H2O_WAVE_ADDRESS

export H2O_WAVE_LISTEN=":${PORT}"
echo $H2O_WAVE_LISTEN

export H2O_WAVE_APP_ADDRESS="http://127.0.0.1:10101"
echo $H2O_WAVE_APP_ADDRESS

./waved & uvicorn app:main
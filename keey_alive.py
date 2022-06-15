from flask import Flask
from threading import Thread

app=Flask('')

@app.route('/')
def main():
    return "Rickyistesting || Made by rickytsung. || wordle_rating || Ver: 1.3"

def run():
    app.run(host="0.0.0.0", port=8080)

def keep_alive():
    server = Thread(target=run)
    server.start()

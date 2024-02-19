# Программа на Python для создания блокчейна

import datetime # Для временной метки
import hashlib # Вычисление хэша для добавления цифровой подписи к блокам
import json # Для хранения данных в блокчейне
from flask import Flask, jsonify # Flask предназначен для создания веб-приложения, а jsonify - для отображения блокчейна
import psycopg2 # подключение к бд
import pandas as pd


# Импорт базы данных
def connect_db():
    print('Начало подключения к БД')
    conn = psycopg2.connect(dbname='tm_test_base', user='postgres', password='Qaz12345', host='localhost')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM main_table')
    df = cursor.fetchall()
    df = pd.DataFrame(df)

    return df

database = connect_db()
print('Данные получены')
print(database)

class Blockchain:
# Эта функция ниже создана для создания самого первого блока и установки его хэша равным "0"
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

# Эта функция ниже создана для добавления дополнительных блоков в цепочку
    def create_block(self, proof, previous_hash):
        block = {
            'index': len(self.chain) + 1,
            'passport_serial_number': str(database[0].iloc[len(self.chain)]),
            'full_name': str(database[1].iloc[len(self.chain)]),
            'gender': str(database[2].iloc[len(self.chain)]),
            'age': str(database[3].iloc[len(self.chain)]),
            'transport': str(database[4].iloc[len(self.chain)]),
            'tariff': str(database[5].iloc[len(self.chain)]),
            'city_from': str(database[6].iloc[len(self.chain)]),
            'city_to': str(database[7].iloc[len(self.chain)]),
            'price': str(database[8].iloc[len(self.chain)]),
            'seat': str(database[9].iloc[len(self.chain)]),
            'trip_date': str(database[10].iloc[len(self.chain)]),
            'ticket_number': str(database[11].iloc[len(self.chain)]),
            'timestamp': str(datetime.datetime.now()),
            'proof': proof,
            'previous_hash': previous_hash}
        self.chain.append(block)
        return block

# Эта функция ниже создана для отображения предыдущего блока
    def print_previous_block(self):
        return self.chain[-1]

# Это функция для проверки работы и используется для успешного майнинга блока
    def proof_of_work(self, previous_proof):
        new_proof = 1
        check_proof = False
        while check_proof is False:
            hash_operation = hashlib.sha256(
                str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:5] == '00000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def chain_valid(self, chain):
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(
                str(proof ** 2 - previous_proof ** 2).encode()).hexdigest()
            if hash_operation[:5] != '00000':
                return False
            previous_block = block
            block_index += 1
        return True

# Создание веб-приложения с использованием flask
app = Flask(__name__)
# Создаем объект класса blockchain
blockchain = Blockchain()

# Главная страница
@app.route('/')
def index() -> str:
    res = ('<p>Блокчейн в сфере Коммерческие транспортные средства и перевозки</p>'
           '<p>Майнинг нового блока: /mine_block</p>'
           '<p>Отобразить блокчейн в формате json: /display_chain</p>'
           '<p>Проверка валидности блокчейна: /valid</p>')
    return res

# Майнинг нового блока
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)
    response = {'message': 'A block is MINED',
                'index': block['index'],
                'passport_serial_number': block['passport_serial_number'],
                'full_name': block['full_name'],
                'gender': block['gender'],
                'age': block['age'],
                'transport': block['transport'],
                'tariff': block['tariff'],
                'city_from': block['city_from'],
                'city_to': block['city_to'],
                'price': block['price'],
                'seat': block['seat'],
                'trip_date': block['trip_date'],
                'ticket_number': block['ticket_number'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']}
    return jsonify(response), 200

# Отобразить блокчейн в формате json
@app.route('/display_chain', methods=['GET'])
def display_chain():
    chain = []
    for block in blockchain.chain:
        data = {
            'index': block['index'],
            'passport_serial_number': block['passport_serial_number'],
            'full_name': block['full_name'],
            'gender': block['gender'],
            'age': block['age'],
            'transport': block['transport'],
            'tariff': block['tariff'],
            'city_from': block['city_from'],
            'city_to': block['city_to'],
            'price': block['price'],
            'seat': block['seat'],
            'trip_date': block['trip_date'],
            'ticket_number': block['ticket_number'],
            'timestamp': block['timestamp'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash']
        }
        chain.append(data)
    response = {'chain': blockchain.chain, 'length': len(blockchain.chain)}
    return jsonify(response), 200


# Проверка валидности блокчейна
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.chain_valid(blockchain.chain)
    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200


# Запустите сервер flask локально
if __name__ == '__main__':
    app.run(host='localhost')
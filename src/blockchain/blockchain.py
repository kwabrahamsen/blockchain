import hashlib      # For å hashe blokkdata
import json         # For å konvertere data til JSON-streng
from time import time   # For å sette tidsstempel på blokkene


# -----------------------------
# Klassen som representerer én blokk i kjeden
# -----------------------------
class Block:
    def __init__(self, index, timestamp, data, previous_hash):
        self.index = index                  # Plass i kjeden
        self.timestamp = timestamp          # Når blokken ble opprettet
        self.data = data                    # Innholdet (f.eks. transaksjoner)
        self.previous_hash = previous_hash  # Hash til forrige blokk
        self.nonce = 0                      # Brukes for "proof of work"
        self.hash = self.calculate_hash()   # Hash for denne blokken

    # Beregner hash av blokkens innhold
    def calculate_hash(self):
        block_string = json.dumps({
            'index': self.index,
            'timestamp': self.timestamp,
            'data': self.data,
            'previous_hash': self.previous_hash,
            'nonce': self.nonce
        }, sort_keys=True).encode()

        return hashlib.sha256(block_string).hexdigest()

    # Simulerer mining ved å finne en hash som starter med X antall nuller
    def mine_block(self, difficulty):
        target = '0' * difficulty
        while self.hash[:difficulty] != target:
            self.nonce += 1
            self.hash = self.calculate_hash()
        
        print(f"✅ Blokk #{self.index} ferdig minet!")
        print(f"    Hash: {self.hash}")
        print(f"    Nonce: {self.nonce}")
        print(f"    Gyldig: {self.hash.startswith(target)}\n")


# -----------------------------
# Klassen som representerer selve blokkjeden
# -----------------------------
class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]  # Start med én blokk
        self.difficulty = 2  # Startvanskelighetsgrad
        self.target_block_time = 3  # Ønsket tid per blokk i sekunder
        self.mining_times = []  # Liste for å lagre mining-tider

    # Oppretter "genesis block" – første blokk i kjeden
    def create_genesis_block(self):
        return Block(0, time(), "Genesis Block", "0")

    # Returnerer siste blokk i kjeden
    def get_latest_block(self):
        return self.chain[-1]

    # Lager og legger til en ny blokk i kjeden
    def add_block(self, new_data):
        previous_block = self.get_latest_block()
        new_block = Block(len(self.chain), time(), new_data, previous_block.hash)

        start_time = time()
        new_block.mine_block(self.difficulty)
        end_time = time()

        mining_time = end_time - start_time
        self.mining_times.append(mining_time)

        self.chain.append(new_block)

        self.adjust_difficulty()

    # Justerer vanskelighetsgrad basert på mining-tid
    def adjust_difficulty(self):
        if len(self.mining_times) < 5:
            print("⏳ Ikke nok data til å justere vanskelighetsgrad ennå.\n")
            return

        avg_time = sum(self.mining_times) / len(self.mining_times)
        print(f"🕒 Gjennomsnittlig tid for mining: {avg_time:.2f} sekunder")

        if avg_time < self.target_block_time * 0.8:
            self.difficulty += 1
            print(f"⬆️ Øker vanskelighetsgrad til {self.difficulty}\n")
        elif avg_time > self.target_block_time * 1.2 and self.difficulty > 1:
            self.difficulty -= 1
            print(f"⬇️ Senker vanskelighetsgrad til {self.difficulty}\n")
        else:
            print(f"🔁 Beholder vanskelighetsgrad på {self.difficulty}\n")

    def is_block_valid(self, block, previous_block):
        if block.hash != block.calculate_hash():
            return False
        if block.previous_hash != previous_block.hash:
            return False
        return True

    # Sjekker om hele kjeden er gyldig (integritet)
    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            previous = self.chain[i - 1]

            # Sjekk om hash stemmer
            if current.hash != current.calculate_hash():
                return False

            # Sjekk om previous_hash stemmer
            if current.previous_hash != previous.hash:
                return False
        return True
    
    def break_block(self, index):
        if 0 < index < len(self.chain):
            self.chain[index].data += " [manipulert]"
            self.chain[index].hash = self.chain[index].calculate_hash() + "xx"  # gjør hashen feil
            return True
        return False
    
    def repair_chain(self):
        for i in range(1, len(self.chain)):
            current = self.chain[i]
            prev = self.chain[i - 1]

            current.previous_hash = prev.hash
            current.hash = current.calculate_hash()


# -----------------------------
# Eksempel på bruk av blokkjeden
# -----------------------------
if __name__ == "__main__":
    my_blockchain = Blockchain()

    # Legg til flere blokker for å se justering av vanskelighetsgrad
    for i in range(10):
        my_blockchain.add_block(f"Transaksjon {i+1}")

    # Skriv ut hele kjeden
    for block in my_blockchain.chain:
        print(f"Index: {block.index}")
        print(f"Tid: {block.timestamp}")
        print(f"Data: {block.data}")
        print(f"Hash: {block.hash}")
        print(f"Hash til forrige: {block.previous_hash}\n")

    # Sjekk om alt er gyldig
    print("Er kjeden gyldig?", my_blockchain.is_chain_valid())
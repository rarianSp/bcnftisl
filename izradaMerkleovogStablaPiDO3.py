import hashlib
import os
# rarianSp2024MITlicenca
# izračunavanje sažetaka
def sazetak(data):
    """zračunava SHA-256 sažetak podataka P"""
    return hashlib.sha256(data.encode('utf-8')).hexdigest()

def hash_file(file_path):
    """izračunava SHA-256 sažetak digitalnih objekata DO"""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        while chunk := f.read(8192):  # prolazak segmenata DO
            hasher.update(chunk)
    return hasher.hexdigest()

def merkleovo_stablo(listovi):
    """
    generira Merkleovo stablo 
    """
    stablo = [listovi]
    
    # generira obrnuto stablo od listova do korijena
    while len(stablo[-1]) > 1:
        current_razina = stablo[-1]
        next_razina = []
        
        # ako je broj čvorova neparan, mora se duplicirati posljednji čvor
        if len(current_razina) % 2 != 0:
            current_razina.append(current_razina[-1])
        
        # kombinira parove čvorova i stvara višu razinu stabla
        for i in range(0, len(current_razina), 2):
            next_razina.append(sazetak(current_razina[i] + current_razina[i+1]))
        
        stablo.append(next_razina)  # dodaje sljedeću razinu stabla
    
    return stablo

# glavni dio
if __name__ == "__main__":
    print("Odaberite vrstu izvora:")
    print("1 - Podaci")
    print("2 - Digitalni objekti (datoteke)")
    choice = input("Unesite svoj izbor (1 ili 2): ")
    
    if choice == "1":
        # odabir broja P koji se sažimaju
        n = int(input("Unesite broj podataka: "))
        
        # unos samih P
        listovi = []
        for i in range(n):
            listovi.append(input(f"Unesite podatke za {i+1} - to je razina 0: "))
        
        # generiranje Merkleovog stabla od P
        listovi_hashed = [sazetak(list) for list in listovi]
    
    elif choice == "2":
        # odabir broja DO
        n = int(input("Unesite broj datoteka: "))
        print("\n")
        
        # učitavanje prethodno odabranog broja DO
        listovi = []
        for i in range(n):
            file_path = input(f"Unesite putanju datoteke {i+1} - to je razina 0 (Mac Finder - Option - D klik - kopirati kao putanju, PC kopirati putanju): ")
            if os.path.exists(file_path):
                file_hash = hash_file(file_path)
                listovi.append(file_hash)
                print(f"Sažetak digitalnog objekta '{file_path}': {file_hash}")
                print("\n")
            else:
                print(f"Digitalni objekt '{file_path}' ne postoji - prekid skripte.")
                exit(1)
        
        # stvaranje Merkleovog stabla
        listovi_hashed = listovi
    
    else:
        print("Nevažeći izbor - prekid skripte.")
        exit(1)
    
    # stvaranje Merkleovog stabla
    stablo = merkleovo_stablo(listovi_hashed)

    # ispis stabla
    print("\nMerkleovo stablo:")

    # ispis razine 1 (sažeci podataka ili digitalnih objekata)
    print("\nRazina 1: Sažeci podataka ili digitalnih objekata:")
    for i, hashed in enumerate(listovi_hashed):
        print(f"List {i+1}: {hashed}")

    for razina_idx, razina in enumerate(stablo):
        print(f"\nRazina {razina_idx + 2}:")  # početna razina je "Razina 2" jer su na razini 1 sažeci, a na razini 0 ulazni P ili DO
        if razina_idx == len(stablo) - 1:  # posljednja razina sadrži samo korijenski sažetak Merkleovog stabla
            print(f"  Korijenski sažetak: {razina[0]}")
            print("\n")
        else:
            for i in range(0, len(razina), 2):
                # kombiniranje parova sažetaka u stablu
                if i + 1 < len(razina):
                    kombinirani_sazetak = sazetak(razina[i] + razina[i+1])
                    print(f"  Čvor {i+1} i {i+2}: {razina[i]} + {razina[i+1]} -> {kombinirani_sazetak}")
                else:
                    print(f"  Čvor {i+1}: {razina[i]} (neparan broj parova, dupliciran)")

# game.py
import random
from vikingsClasses import Viking, Saxon, War

# Funció per crear un exèrcit de Vikings
def create_viking_army(size):
    vikings = []
    names = ["Mar", "Tanya", "Gabriel", "Elena"]
    for _ in range(size):
        name = random.choice(names)
        strength = random.randint(1, 100)
        vikings.append(Viking(name, strength))
    return vikings

# Funció per crear un exèrcit de Saxons
def create_saxon_army(size):
    saxons = []
    names = ["Garm", "Hrolf", "Sigurd", "Bjorn"]
    for _ in range(size):
        name = random.choice(names)
        strength = random.randint(1, 100)
        saxons.append(Saxon(name, strength))
    return saxons

# Funció per executar la batalla
def battle(war):
    while True:
        result = war.showStatus()
        print(result)
        if result != "Vikings and Saxons are still in the thick of battle.":
            break
        war.vikingAttack()
        war.saxonAttack()

# Funció principal del joc
def main():
    # Crear els exèrcits
    viking_army = create_viking_army(5)
    saxon_army = create_saxon_army(5)
    
    # Crear la guerra
    war = War(viking_army, saxon_army)
    
    # Mostrar l'estat inicial
    print("Iniciant la guerra!")
    print(war.showStatus())
    
    # Iniciar la batalla
    battle(war)
    
    # Mostrar el resultat final
    print("La guerra ha acabat!")
    print(war.showStatus())

if __name__ == "__main__":
    main()

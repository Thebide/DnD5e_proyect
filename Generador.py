import os
import json

character_folder = "Characters"

character = {}

info = ["name", "race", "background"]

attributes = ["strength", "dexterity", "constitution", "intelligence", "wisdom", "charisma"]

def load_rules():
  with open("reglas.json", "r") as class_characteristic:
    data = json.load(class_characteristic)
  return data
rules = load_rules()

def capture_info():
  user_info = {}
  for keys in info:
    user_info[keys] = input(f"What is your {keys.capitalize()}? ").capitalize()
  while True:
    print("What class are you?")
    print(list(rules["Class"]))
    chosen_class = input().capitalize()
    if chosen_class in rules["Class"]:
      break
    else:
      print("Try one of the shown classes")
  user_info["class"] = chosen_class
  saving_proficiency = rules["Class"][user_info["class"]]["saving_throws_by_class"]
  user_info["proficiency"] = saving_proficiency

  while True:
    try:
      level = int(input("What level are you? "))
      break
    except ValueError:
      print("Try a number")
  user_info["level"] = level
  return user_info
  #print(f"Your proficiencies are:", ", ".join(saving_proficiency))


def capture_stats():
  stats = {}
  for keys in attributes:
    while True:
      try:
        stats[keys] = int(input(f"What value of {keys.capitalize()} did you roll? "))
        break
      except ValueError:
        print("Try a number")
  return stats

def calculate_mods(stats):
  modifier = {}
  for keys, value in stats.items():
    modifier[keys] = (value -10)// 2
  return modifier

def calculate_hp(user_info, modifier):
  base_die = rules["Class"][user_info["class"]]["hit_dice_by_class"]
  constitution_mod = modifier["constitution"]
  hp = base_die + constitution_mod
  if user_info["level"] > 1:
    hp += (base_die // 2 + 1 + constitution_mod) * (user_info["level"] - 1)
  return hp


def print_character(character):
  for k, i in character.items():
      if isinstance(i, dict):
          print(f"{k}:")
          for subk, subi in i.items():
              print(f"  {subk}: {subi}")
      elif isinstance(i, list):
          print(f"{k}: {', '.join(i)}")
      else:
          print(f"{k}: {i}")

def create_new_character(rules):
    """
    Función de coordinación: Llama a las otras funciones en orden para crear un PJ nuevo.
    Devuelve el diccionario completo del personaje.
    """
    print("\n--- CREANDO NUEVO PERSONAJE ---")
    # 1. Capturar info básica
    user_info = capture_info(rules)
    # 2. Capturar stats
    stats = capture_stats()
    # 3. Calcular mods
    modifier = calculate_mods(stats)
    # 4. Calcular HP
    hp = calculate_hp(user_info, modifier, rules)

    # 5. Empaquetar todo
    character = user_info
    character["stats"] = stats
    character["modifier"] = modifier
    character["hp"] = hp
    
    return character

print("--- Character Sheet ----")
print_character(character)

def save_character(character):
  if not os.path.exists(character_folder):
    os.makedirs(character_folder)
  
  file_name = input("Ingrese el nombre del personaje: ") + ".json"

  character_rout = os.path.join(character_folder, file_name)
  
  try:
    with open(character_rout, "w") as f:
      json.dump(character, f, indent=4)
      print(f"Personaje guardado correctamente!")
      return character
  except FileExistsError:
     print("El nombre ingresado ya existe intente otro nombre.")
     return None


def load_character():
  file_name = input("¿Qué personaje quiere cargar?") + ".json"

  character_rout = os.path.join(character_folder, file_name)

  try:
      with open(character_folder, "r") as f:
          personaje_cargado = json.load(f)
      print(f"¡Personaje '{character_rout}' cargado con éxito!")
      return personaje_cargado
  except FileNotFoundError:
      print(f"Error: No se encontró el archivo '{character_rout}'.")
      return None # Devolvemos 'None' para indicar que la carga falló.
  except json.JSONDecodeError:
      print(f"Error: El archivo '{character_rout}' no es un JSON válido.")
      return None

def main():
  while True:
    print("  MENÚ PRINCIPAL   ")
    print()
    print("1. Nuevo personaje.")
    print("2. Guardar personaje.")
    print("3. Cargar personaje.")
    print("4. Eliminar Personaje.")
    print()
    print("0. Salir del programa.")
    option = input("¿Que desea hacer?")
    match option:
       case "1":  character = create_new_character(rules)
       case "2":
       case "3":
       case "0":
          print("Saliendo del programa")
          break
       Print("Opcion invalida")
            

if __name__ == "__main__":
    main()
### Автономне ядро керування FPV-дроном на базі ROS2.

Система побудована за модульним принципом і працює як єдиний організм.

Проєкт орієнтований на:
- автономний політ
- пошук і супровід цілей
- антиколізію
- повернення додому
- роботу в групі (swarm)
- пріоритетне прийняття рішень
---
### СТРУКТУРА ПРОЄКТУ
 
     └── 📁 src
         └── 📁 autonomy_core	 
             └── 📁 autonomy_core
			 
                 ├── 🧠 core_node.py
                 ├── 🧩 behavior_tree.py
                 ├── 🎯 target_tracker.py
                 ├── 🛑 anti_collision.py
                 ├── 🏠 return_home.py
                 ├── 🧑‍🤝‍🧑 swarm_sync.py
                 ├── 🧭 mission_manager.py
                 ├── ⚙️ failsafe.py
                 ├── ❤️ health_monitor.py
                 ├── 📦 blackbox.py
                 ├── 🌐 web_ui.py
                 └── 📄 __init__.py

### ЗАГАЛЬНА АРХІТЕКТУРА
- СЕНСОРИ
- Camera (detections)
- LIDAR / Depth (LaserScan)
- Odometry
- Swarm data
  
↓

AUTONOMY CORE NODE

↓

- Behavior Tree (BT)
- Priority Selector
- Command Generator
  
↓

/cmd_vel_autonomy

### ЦЕНТРАЛЬНИЙ ВУЗОЛ 
— core_node.py

Головний мозок системи.

#### Функції:
- підписка на всі сенсори
- запуск behavior tree
- публікація команд руху
- контроль стану
- логування
- синхронізація дронів
---
#### BEHAVIOR TREE

Порядок виконання (зверху вниз):
- Anti-collision — найвищий пріоритет
- Return Home
- Target tracking
- Navigation
Якщо верхня гілка активна — нижні не виконуються.

#### ANTI-COLLISION
Використовується LaserScan.
Якщо мінімальна дистанція менше 1.5 м:
- керування повністю перехоплюється
- швидкість обнуляється
- місія зупиняється
Це рефлекс безпеки, а не логіка місії.

#### MISSION SYSTEM
- mission_manager.py — надсилання навігаційних цілей Nav2
- mission_loader.py — завантаження місій
  
#### TARGET TRACKING
Супровід цілі по камері:
- визначення центру bounding box
- помилка yaw
- корекція кутової швидкості

#### PRIORITY SELECTOR
Вибір головної цілі з усіх доступних детекцій.

#### RETURN HOME
Збереження координат старту та повернення у разі:
- втрати одометрії
- помилок сенсорів
- failsafe

#### SWARM SYSTEM
Обмін станами між дронами:
- позиція
- стан
- роль

#### FORMATION FLIGHT
Політ строєм:
- ведучий
- ведені
- позиційний офсет

#### FAILSAFE
Активація безпечних сценаріїв при збої системи.

#### HEALTH MONITOR
Контроль активності модулів та таймінгів.

#### BLACKBOX
Логування всіх подій системи.

#### WEB UI
Flask backend:
- телеметрія
- стан системи
- місії

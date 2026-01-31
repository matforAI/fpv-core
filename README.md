FPV AI Drone — Autonomous Core
Автономне ядро керування FPV-дроном на базі ROS2.
Система побудована за модульним принципом і працює як єдиний організм.
Проєкт орієнтований на:
автономний політ
пошук і супровід цілей
антиколізію
повернення додому
роботу в групі (swarm)
пріоритетне прийняття рішень
📁 Структура проєкту
Копировать код

fpv-core/
└── ros_ws/
    └── src/
        └── autonomy_core/
            └── autonomy_core/
                ├── core_node.py
                ├── state_machine.py
                ├── behavior_tree.py
                ├── priority_selector.py
                ├── mission_manager.py
                ├── mission_loader.py
                ├── target_tracker.py
                ├── anti_collision.py
                ├── return_home.py
                ├── formation.py
                ├── swarm_sync.py
                ├── failsafe.py
                ├── health_monitor.py
                ├── cmd_vel_bridge.py
                ├── blackbox.py
                ├── web_ui.py
                └── __init__.py
🧠 Загальна архітектура
Копировать код

СЕНСОРИ
Camera (detections)
LIDAR / Depth (LaserScan)
Odometry
Swarm data
        ↓
AUTONOMY CORE NODE
        ↓
Behavior Tree (BT)
        ↓
Priority Selector
        ↓
Command Generator
        ↓
/cmd_vel_autonomy
🔁 Центральний вузол
core_node.py
Головний мозок системи.
Функції:
підписка на всі сенсори
запуск behavior tree
публікація команд руху
контроль стану
логування
синхронізація дронів
🌳 Behavior Tree
Порядок виконання (зверху вниз):
Anti-collision — найвищий пріоритет
Return Home
Target tracking
Navigation
Якщо верхня гілка активна — нижні не виконуються.
🚨 Anti-Collision
Використовується LaserScan.
Якщо мінімальна дистанція < 1.5 м:
керування повністю перехоплюється
швидкість обнуляється
місія зупиняється
Це рефлекс безпеки, а не логіка місії.
🧭 Mission System
mission_manager.py — надсилання цілей Nav2
mission_loader.py — завантаження місій
🎯 Target Tracking
Супровід цілі по камері:
визначення центру bounding box
помилка yaw
корекція кутової швидкості
🧠 Priority Selector
Вибір головної цілі з усіх доступних детекцій.
🏠 Return Home
Збереження координат старту та повернення у разі:
помилки сенсорів
втрати одометрії
failsafe
🧑‍🤝‍🧑 Swarm System
Обмін станами між дронами:
позиція
стан
роль
🧩 Formation Flight
Політ строєм:
ведучий
ведені
позиційний офсет
⚠️ FailSafe
Активація безпечних сценаріїв при збоях.
❤️ Health Monitor
Контроль активності модулів та таймінгів.
📦 BlackBox
Логування всіх подій системи.
🌐 Web UI
Flask backend:
телеметрія
стан системи
місії
✅ Поточний стан
Реалізовано:
автономне ядро
behavior tree
антиколізія
супровід цілі
повернення додому
swarm-синхронізація
формації
health-monitor
blackbox
web UI

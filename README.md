### Features

Программа значительно расширяет возможности диагностики сетевых проблем.
Схема работы программы.

![](https://github.com/SkarioT/GUI_network-hardware-log-viewer/blob/main/example_screen/scheme.png)

Клиент принимает на вход логин или информация по интересующему нас коммутатору.
В ходе обработки входных данных, выполняются дол запросы к :
- **Sup tools** - веб-сервер получающий ограниченную информацию о сетевом соединении.
- **RDB** - веб-сервер хранящий информацию как об авторизациях, так и информацию о сетевом оборудовании и его спецификации
- **Mac-API** - позволяющий получить информацию о вендере, на основании mac-адреса

Пример работы программы:
![](https://github.com/SkarioT/GUI_network-hardware-log-viewer/blob/main/example_screen/jump_server_scr_1.png)
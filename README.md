# Console
## Описание
### Что это
Бот, предназначенный для управления терминалом **Termux**, который запущен на этом же устройстве, что и терминал

###  Как это работает
При отправке сообщения в чате с ботом, скрипт получает это сообщение и вставляет его в Termux. При успешом выполнении команды, выведет полученный текст в чат

### Кастомные команды
- `/restart`
- `/cd`
> По непонятным мне причинам, **Termux** делает что - то непонятное, при выполнени обычной команды **cd**. Поэтому пришлось адаптировать команду своими силами

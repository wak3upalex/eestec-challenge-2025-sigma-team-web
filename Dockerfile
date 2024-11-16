# Используем легковесный образ NGINX
FROM nginx:1.25

# Устанавливаем рабочую директорию
WORKDIR /usr/share/nginx/html

# Удаляем стандартные файлы NGINX (если есть)
RUN rm -rf ./*

# Копируем ваши файлы в директорию NGINX
COPY public/ .

# Открываем порт для HTTP
EXPOSE 80

# Запускаем NGINX
CMD ["nginx", "-g", "daemon off;"]

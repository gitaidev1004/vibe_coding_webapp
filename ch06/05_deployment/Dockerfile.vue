# ch06/05_deployment/Dockerfile.vue
# Vue.js 3 프런트엔드(ch04/vue_project)를 빌드하고 Nginx로 정적 파일을 서빙하는 Dockerfile
FROM node:20-slim AS build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM nginx:1.27-alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
EXPOSE 80

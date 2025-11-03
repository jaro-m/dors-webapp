# Build Stage
FROM node:20-alpine AS build

# provide correct API URL
ENV REACT_APP_API_URL="https://apiserver:8000"
WORKDIR /app

COPY package*.json ./
RUN npm install
COPY . .

RUN npm run build

# Production Stage
FROM nginx:stable-alpine AS production

COPY --from=build /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
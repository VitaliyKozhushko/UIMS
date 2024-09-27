FROM node:20-alpine

WORKDIR /app/frontend

COPY package*.json ./

RUN rm -rf node_modules package-lock.json

RUN npm install

COPY . .

RUN npm run build

EXPOSE 3000

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

CMD ["npm", "start"]

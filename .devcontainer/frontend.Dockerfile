FROM node:22

WORKDIR /workspace/frontend

COPY . ../

RUN yarn install

EXPOSE 3000
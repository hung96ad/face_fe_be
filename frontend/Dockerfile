FROM node:16.3.0-slim

ADD package.json /package.json

ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
RUN npm install --legacy-peer-deps

WORKDIR /app
ADD . /app

EXPOSE 8000
EXPOSE 35729

CMD ["npm", "start"]

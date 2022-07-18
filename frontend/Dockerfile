FROM node:16.10.0-slim

ADD package.json /package.json
ENV NODE_PATH=/node_modules
ENV PATH=$PATH:/node_modules/.bin
RUN npm install --legacy-peer-deps

WORKDIR /app
ADD . /app

EXPOSE 8000

CMD ["npm", "start"]

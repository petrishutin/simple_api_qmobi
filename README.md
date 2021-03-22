Simple api service parses USD/RUR EUR/RUR exchange rates from 'http://cbr.ru' and returns as a json string.
By default, local address is "/0.0.0.0:8080/"

Deploy in Docker:

 - Build docker image `docker build -t simple_api .`

 - Run server `docker run -e ENV=RUN -itd -p 8080:8080 simple_api`
Service will be available at "/0.0.0.0:8080/"

 - Run tests `docker run -e ENV=TEST -t simple_api`

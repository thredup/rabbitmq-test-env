FROM ruby:alpine
RUN gem install bunny
COPY ./producer.rb /app/producer.rb
CMD ruby /app/producer.rb
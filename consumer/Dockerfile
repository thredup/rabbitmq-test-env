FROM ruby:alpine
RUN gem install bunny
COPY ./consumer.rb /app/consumer.rb
CMD ruby /app/consumer.rb
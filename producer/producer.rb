#!/usr/bin/env ruby
require 'bunny'
require 'logger'

logger = Logger.new(STDOUT)
logger.level = Logger::DEBUG

host = ENV["RABBITMQ_HOST"] || "127.0.0.1"
connection = Bunny.new(host: host)
connection.start

channel = connection.create_channel
queue = channel.queue('hello')
logger.debug "Connected to #{host}"
i = 1
while true
  queue.publish("Hello #{i}")
  logger.debug " [#{host}] Sent 'Hello #{i}'"
  i += 1
  sleep 1
end
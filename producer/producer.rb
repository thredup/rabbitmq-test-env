#!/usr/bin/env ruby
require 'bunny'
require 'logger'
$stdout.sync = true

logger = Logger.new(STDOUT)
logger.level = Logger::DEBUG

host = ENV["RABBITMQ_HOST"] || "127.0.0.1"

begin 
  connection = Bunny.new(host: host)
  connection.start
rescue Bunny::TCPConnectionFailed => e
  logger.debug 'Connection Failed, waiting 5 seconds'
  sleep(5)
  retry
end

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
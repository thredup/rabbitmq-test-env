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

begin
    logger.debug ' [*] Waiting for messages. To exit press CTRL+C'
    queue.subscribe(block: true) do |_delivery_info, _properties, body|
      logger.debug " [#{host}] Received #{body}"
    end
  rescue Interrupt => _
    connection.close
  
    exit(0)
  end
  
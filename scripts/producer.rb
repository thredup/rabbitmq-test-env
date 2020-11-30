#!/usr/bin/env ruby
require 'bunny'

connection = Bunny.new
connection.start
channel = connection.create_channel
queue = channel.queue('hello')
i = 1
while true
  queue.publish("Hello #{i}")
  puts " [#{i}] Sent 'Hello #{i}'"
  i += 1
  sleep 1
end
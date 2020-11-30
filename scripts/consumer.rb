#!/usr/bin/env ruby
require 'bunny'
port = "32769"
connection = Bunny.new(port: port)
connection.start

channel = connection.create_channel
queue = channel.queue('hello')

begin
    puts ' [*] Waiting for messages. To exit press CTRL+C'
    queue.subscribe(block: true) do |_delivery_info, _properties, body|
      puts " [#{port}] Received #{body}"
    end
  rescue Interrupt => _
    connection.close
  
    exit(0)
  end
  
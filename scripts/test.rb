require "bunny"

# Start a communication session with RabbitMQ
conn = Bunny.new(port: "32769")
conn.start

# open a channel
ch = conn.create_channel

# declare a queue
q  = ch.queue("hello")

delivery_info, metadata, payload = q.pop

puts "This is the message: #{payload}"

# close the connection
conn.stop
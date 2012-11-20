def log(message)
  time = Time.new.ctime
  puts "[#{time}] #{message}\n"
end
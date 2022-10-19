#!/usr/bin/env ruby

require "wavefile"
include WaveFile

datadir = "data/voices/Matthew"
dest = "output"

square_wave_cycle = [0.0] * 10000
blank = Buffer.new(square_wave_cycle, Format.new(:mono, :float, 24000))

lines = File.read("data/digits.txt").split(/\n/)

LINES_PER_CHAPTER = 40

chapter = 0
lines.each_slice(LINES_PER_CHAPTER).each do |digits|
  # digits is a group of lines
  chapter = chapter + 1
  puts chapter
  puts digits.inspect
  Writer.new("#{dest}/chapter#{chapter}.wav", Format.new(:stereo, :pcm_16, 24000)) do |writer|
    digits.each do |line|
      puts line
      line.split(//).compact.each do |char|
        # puts char
        next if char == ' '

        Reader.new("#{datadir}/#{char}.wav").each_buffer do |buffer|
          writer.write(buffer)
        end
        writer.write(blank)
      end # grouping
    end # digits
  end # writer
end # lines
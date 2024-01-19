#!/usr/bin/env ruby

require "fileutils"
require "wavefile"
include WaveFile

LINES_PER_CHAPTER = 40

DATADIR = "samples"
dest = "output"

FileUtils.mkdir_p(DATADIR)
FileUtils.mkdir_p(dest)

def sample_for(contents)
  result = "#{DATADIR}/#{contents}.wav"
  raise StandardError.new "Missing #{result}" if !File.exist?(result)
  raise StandardError.new "null #{result}" if File.size(result).zero?

  result
end

def blank
  blank_data = [0.0] * 10 #000
  Buffer.new(blank_data, Format.new(:mono, :float, 24000))
end

# def add_sample(writer, char)
#   Reader.new(sample_for(char)).each_buffer do |buffer|
#     writer.write(buffer)
#   end
#   writer.write(blank)
# end

def add_break(writer)
  writer.write(blank)
end

def add_pause(writer)
  writer.write(blank)
end

def add_phrase(writer, phrase)
  puts phrase
  Reader.new(sample_for(phrase)).each_buffer do |buffer|
    writer.write(buffer)
  end
end


# lines = File.read("data/digits.txt").split(/\n/)
lines = File.read("data/short.txt").split(/\n/)

# soxi samples/00000.wav

# Input File     : 'samples/00000.wav'
# Channels       : 1
# Sample Rate    : 44100
# Precision      : 16-bit
# Duration       : 00:00:04.54 = 200038 samples = 340.201 CDDA sectors
# File Size      : 400k
# Bit Rate       : 706k
# Sample Encoding: 16-bit Signed Integer PCM

data = `soxi #{DATADIR}/00000.wav`

data = data.split(/\n/).select { |l| l.include?(':') }.map { |l| l.split(':', 2).map(&:strip) }.to_h
# {"Input File"=>"'samples/00000.wav'",
#  "Channels"=>"1",
#  "Sample Rate"=>"44100",
#  "Precision"=>"16-bit",
#  "Duration"=>"00:00:04.54 = 200038 samples = 340.201 CDDA sectors",
#  "File Size"=>"400k",
#  "Bit Rate"=>"706k",
#  "Sample Encoding"=>"16-bit Signed Integer PCM"}

puts data.inspect

channels = data['Channels'].to_i == 2 ? :stereo : :mono
precision = data['Precision'] == '16-bit' ? :pcm_16 : :pcm_32
sample_rate = data['Sample Rate'].to_i

chapter = 0
lines.each_slice(LINES_PER_CHAPTER).each do |digits|
  # digits is a group of lines
  chapter = chapter + 1
  puts chapter
  puts digits.inspect
  # Riff44100Hz16BitMonoPcm
  # :mono, :pcm_16, 44100
  Writer.new("#{dest}/chapter#{chapter}.wav", Format.new(channels, precision, sample_rate)) do |writer|
    digits.each do |line|
      # puts line
      groupings = line.split(/ +/)
      puts groupings.inspect
      groupings.each do |phrase|
        add_phrase(writer, phrase)
        add_pause(writer)
      end
      add_break(writer)

      # index = groupings.shift

      # puts index
      # index.split(//).each do |char|
      #   add_sample(writer, char)
      # end
      # add_blank(writer)

      # groupings.each do |grouping|
      #   puts grouping
      #   sleep 1
      #   grouping.split(//).each do |char|
      #     add_sample(writer, char)
      #   end
      #   add_blank(writer)
      # end
    end # digits
  end # writer
end # lines
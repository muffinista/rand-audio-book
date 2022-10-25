#!/usr/bin/env ruby

require 'aws-sdk-polly'
require "wavefile"
include WaveFile

LINES_PER_CHAPTER = 40

VOICE = "Joanna"
DATADIR = "data/voices/#{VOICE}"
dest = "output"

SAMPLE_SSML = JSON.parse(File.read("data/voice-samples.json")).map { |k, v| [k.gsub(/.wav$/, ''), v]}.to_h

FileUtils.mkdir_p( DATADIR)
FileUtils.mkdir_p(dest)

def sample_for(contents)
  result = "#{DATADIR}/#{contents}.wav"
  ogg_result = "#{DATADIR}/#{contents}.ogg"

  if !File.exist?(result)
    polly = Aws::Polly::Client.new
    contents = SAMPLE_SSML[contents] if SAMPLE_SSML.key?(contents)
    # contents = "<speak><amazon:domain name=\"news\">#{contents}</amazon:domain></speak>" unless contents.match?(/<speak/)
    contents = "<speak>#{contents}</speak>" unless contents.match?(/<speak/)
    puts contents

    resp = polly.synthesize_speech({
      output_format: "ogg_vorbis",
      text: contents,
      text_type: 'ssml',
      voice_id: VOICE,
    })

    IO.copy_stream(resp.audio_stream, ogg_result)

    puts 'Wrote Polly output to: ' +  ogg_result

    `sox #{ogg_result} --norm=-0.1 #{result}`
  end

  result
end

def blank
  blank_data = [0.0] * 10 #000
  Buffer.new(blank_data, Format.new(:mono, :float, 24000))
end

def add_sample(writer, char)
  Reader.new(sample_for(char)).each_buffer do |buffer|
    writer.write(buffer)
  end
  writer.write(blank)
end

def add_blank(writer)
  writer.write(blank)
end


# lines = File.read("data/digits.txt").split(/\n/)
lines = File.read("data/short.txt").split(/\n/)

chapter = 0
lines.each_slice(LINES_PER_CHAPTER).each do |digits|
  # digits is a group of lines
  chapter = chapter + 1
  puts chapter
  puts digits.inspect
  Writer.new("#{dest}/chapter#{chapter}.wav", Format.new(:stereo, :pcm_16, 24000)) do |writer|
    digits.each do |line|
      puts line
      groupings = line.split(/ +/)
      index = groupings.shift

      puts index
      index.split(//).each do |char|
        add_sample(writer, char)
      end
      add_blank(writer)

      groupings.each do |grouping|
        puts grouping
        sleep 1
        grouping.split(//).each do |char|
          add_sample(writer, char)
        end
        add_blank(writer)
      end
    end # digits
  end # writer
end # lines
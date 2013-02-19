#!/usr/bin/env ruby
# Author: Sébastien Boisvert

class Sequence

	def initialize name,sequence,quality
		@name=name
		@sequence=sequence
		@quality=quality
	end

	def sequence
		@sequence
	end

	def name
		@name
	end

	def quality
		@quality
	end

	def get_base_name
		name.split("/")[0]
	end

	def write file
		file.write name+"\n"
		file.write sequence+"\n"
		file.write "+\n"
		file.write quality+"\n"
	end
end

class FastqFile

	def initialize file_name
		@file_name=file_name
		@file=File.new @file_name, "r"
		@sequence=nil
		readSequence!
	end

	def has_next?
		!@sequence.nil?
	end

	def get_next!
		sequence=@sequence
		readSequence!
		sequence
	end

	def readSequence!
		name=@file.gets
		sequence=@file.gets
		quality=@file.gets
		quality=@file.gets

		[name,sequence,quality].each do |entry|
			if entry.nil?
				@sequence=nil
				return
			end
			entry.strip!
		end

		@sequence=Sequence.new name,sequence,quality
	end

	def count_sequences!
		@entries=0

		while has_next?
			if @entries%10000==0
				print "\r"+@file_name+" -> "+@entries.to_s+" entries"
			end
			sequence=get_next!
			@entries+=1
		end
		puts "\r"+@file_name+" -> "+@entries.to_s+" entries"
	end

	def get_number_of_sequences
		@entries
	end

	def get_file_name
		@file_name
	end
end

class Converter
	def initialize input1,input2,output1,output2

		@input1=input1
		@input2=input2
		@output1=output1
		@output2=output2
	end

	def count_sequences!

		reader1=FastqFile.new @input1
		reader2=FastqFile.new @input2

		[reader1,reader2].each do |reader|
			reader.count_sequences!
			puts reader.get_file_name+" "+reader.get_number_of_sequences.to_s
		end
	end

	def dump_output_files!

		puts "Inputs: "+@input1+" and "+@input2

		reader1=FastqFile.new @input1
		reader2=FastqFile.new @input2

		output_stream_1=File.new @output1, "w"
		output_stream_2=File.new @output2, "w"

		objects=Array.new
		minimum_number_of_objects=50000
		maximum_number_of_destroyed_objects=20000
		maximum_distance=300000

		destroyed_objects=0

		objectIndex=Hash.new

		matched_entries=0
		entries_from_1=0
		entries_from_2=0

		while reader1.has_next?
			sequence1=reader1.get_next!

			entries_from_1+=1

			print_progression matched_entries, entries_from_1, entries_from_2,false
# garbage collect array

			if destroyed_objects>maximum_number_of_destroyed_objects

				new_objects=Array.new
				objects.each do |value|
					if value[0].nil?
						next
					end

					if value[1]+maximum_distance< entries_from_2
						next
					end

					new_objects.push value
				end

				destroyed_objects=0
				objectIndex=Hash.new

				objects=new_objects

				objects.each_index do |index|
					objectIndex[objects[index][0].get_base_name]=index
				end
			end
			
# read objects
			while ( ( objects.size - destroyed_objects) <minimum_number_of_objects ) and reader2.has_next?
				sequence=reader2.get_next!
				objects.push [sequence,entries_from_2]

				objectIndex[sequence.get_base_name]=objects.size-1

				entries_from_2+=1
			end

			unless objectIndex.has_key? sequence1.get_base_name
				next
			end

			index=objectIndex[sequence1.get_base_name]

			sequence2=objects[index][0]

			sequence1.write output_stream_1
			sequence2.write output_stream_2
			objects[index][0]=nil
			destroyed_objects+=1
			matched_entries+=1 
		end

		print_progression matched_entries, entries_from_1, entries_from_2,true

	end

	def print_progression matched_entries, entries_from_1, entries_from_2,force

		if entries_from_1%10000==0 or force
			puts ""+" -> "+entries_from_1.to_s+" entries from first file"
		end

		if entries_from_2%10000==0 or force
			puts ""+" -> "+entries_from_2.to_s+" entries from second file"
		end

		if matched_entries%10000==0 or force
			puts ""+" -> "+matched_entries.to_s+" matched entries"
		end
	end
end

arguments=ARGV

if arguments.size!=4
	puts "Usage: KeepOnlyPairedSequences.rb input1.fastq input2.fastq output1.fastq output2.fastq"
	puts "The output files contain matched sequences from the input files"
	exit
end

input1=arguments[0]
input2=arguments[1]
output1=arguments[2]
output2=arguments[3]

converter=Converter.new input1,input2,output1,output2
#converter.count_sequences!
converter.dump_output_files!

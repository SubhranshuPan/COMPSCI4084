fav_song = input("Enter first line of your fav song: ")
length = len(fav_song)
print(length)

string_range = length - 1
start_index = int(input("Enter start index (0-{string_range}): "))
end_index = int(input("Enter end index (0-{string_range}): "))

print(fav_song[start_index:end_index+1])

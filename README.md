# Compress-Decompress
A video compressor and decompressor script made in python


## Script functionality

Args paramaters for the functioning of the program

-C or -c [path], cause the compression of the video file

-D or -d [Compressed_file_path] [fps:int] [final_path], decompress the file


## How it works

The scirpt works considering similarities betwene sucessive video frames, following the idea
that, if two o more consecutives frames are equal according to a certain degree (being that degree of equalaty)
specified by the user, then those frames don't need to be represented N numbers of times and as result the final
product of the compression is a file with smaller size compare to the orignal

## Disclaimer

In this example the real video size is the sum of the frames created, this is due the nature of .mp4 files wich themselfs
are heavely compressed. Thus the result comparassion must be done with relation to the sum of the frames (all .jpg which also suffers compression)
and the final product which is the sum of thoses frames compacted.

## Visualization of the process

![267544561-5c916702-ca20-4aa7-9ee1-1493b7648e11](https://github.com/dashdashRod/Compress-Decompress/assets/39976286/29be40a1-cbdd-4ded-b940-f51e4f3126e6)

which the letters refers to the type of frames which are not taken into consideration due the characteristics of this compression technic

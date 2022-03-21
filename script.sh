for dir in videos/out/*/ ; do
  videoTexturesFramePath=${dir}
  ffmpeg -i ${videoTexturesFramePath}frame%04d.png out/$(basename ${dir}).mp4 -y
done

# name='Sinkin_in_the_Bathtub'
# ext='mp4'

# videoTexturesFramePath="videos/source/${name}"
# outVideo="input_${name}.${ext}"

# ffmpeg  -i  $videoTexturesFramePath/%04d.png $outVideo -y
# ffmpeg -start_number 1578 -i  $videoTexturesFramePath/%04d.png $outVideo -y
from PIL import Image
from PIL.ExifTags import TAGS
# Open the image file
image_path = 'D:/2023/GPS/geo_tagging/geotagged_image.jpg'  # Replace with the path to your image file
image = Image.open(image_path)
# Extract the Exif metadata
exif_data = image._getexif()
# Print the metadata
if exif_data is not None:
    for tag_id, value in exif_data.items():
        tag_name = TAGS.get(tag_id, tag_id)
        print(f"{tag_name}: {value}")
else:
    print("No Exif metadata found.")
# Close the image
image.close()
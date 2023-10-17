import qrcode
img = qrcode.make('EventA-abc125xyz')
type(img)  # qrcode.image.pil.PilImage
img.save("notavailable.png")
print("Done")
# Hide Message To Image Using Steganography

Script made in Python that has the ability to hide message in image without change the colors of the image using steganography method.

# How to use

```
image = "myimage.jpg"
secret_message = "my secret message"
message_hide(image,secret_message) # will create a new image "myimage-secret.png"
reveal_message = reveal("myimage-secret.png")
print(reveal_message)
```

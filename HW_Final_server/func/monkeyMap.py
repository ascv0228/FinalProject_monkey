def monkeyMap():
    s = '''
<!DOCTYPE html>
<html>
<head>
    <title>中山猴子地圖</title>
    <script>
        function updateImage() {
            document.getElementById('image').src = '/image?' + new Date().getTime();
            document.getElementById('text1').innerHTML = new Date();
        }

        setInterval(updateImage, 1000);
    </script>
</head>
<body>
    <h3 id=text1>time: </h3>
    <img id="image" src="/image" alt="Image" width="800" height="600">
</body>
</html>
'''
    return s

_func = monkeyMap

__exports__ = {
    "name" : _func.__code__.co_name,
    "path" : "/monkeyMap",
    "methods": ['GET'],
    "execute": _func
}

if __name__ == "__main__":
    print(_func.__code__.co_name)



# <!DOCTYPE html>
# <html>
# <head>
#     <title>自動更新圖片</title>
#     <script>
#         function updateImage() {
#             var timestamp = new Date().getTime();
#             document.getElementById('image').src = '/image?' + timestamp;
#         }

#         setInterval(updateImage, 1000);
#     </script>
# </head>
# <body>
#     <img id="image" src="/image" alt="Image" width="400" height="300">
# </body>
# </html>
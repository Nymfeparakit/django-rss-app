
function resize_images() {
    images_list = Array.from(document.getElementsByTagName("img"))
    images_list.forEach(function (img) {
        img.setAttribute("style", "max-width: 600px;")
    })
}

document.addEventListener('DOMContentLoaded', function() {
    resize_images()
})
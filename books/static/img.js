
const image = Document.quarySelector("img"),
input = Document.quarySelector('input');
input.addEventListener('change',() => {
    image.src = URL.createObjectURL(input.files[0]);
});

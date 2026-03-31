const paragraphs = document.getElementsByTagName("p");
for (let paragraph of paragraphs) {
    paragraph.textContent = "Новый текст";
}

const ul = document.getElementsByTagName("ul")[0];
for (let i = 1; i <= 5; i++) {
    let el = document.createElement("li");
    el.textContent = `Элемент ${i}`;
    ul.appendChild(el);
}

const img = document.getElementsByTagName("img")[0];
img.src = "placeholder.jpg";
img.alt = "Изображение";

const classHighlight = document.getElementsByClassName("highlight");
for (element of classHighlight) {
    element.style.backgroundColor = 'yellow';
    element.style.fontSize = '20px';
}

const ol = document.getElementById("tasks");
console.log(ol);
for (let i = ol.children.length - 1; i >= 0; i -= 2) { 
    ol.children[i].remove();
}

// Задача 1

// дополнительные функции:
// - редактирования выбранного элемента из списка и добавления нового элемента в список
// - удаление элементов из списка через клавишу delete
// - выбор нескольких элементов через зажатый ctrl
// - отмена выделения через нажатие Esc

const listBooks = document.getElementById(`listBooks`);
const textarea = document.querySelector(`.task1 textarea`);

let targetObjs = [];
listBooks.addEventListener('click', (event) => {
    function checkingSelected(list) {
        if (list.length != 0) {
            return true;
        } else {
            return false;
        }
    }

    if (event.target.tagName == `P`) {
        if (event.ctrlKey) {
            if (targetObjs.includes(event.target)) {
                event.target.style.backgroundColor = '#eee';
                targetObjs.splice(targetObjs.indexOf(event.target), 1);
            } else {
                event.target.style.backgroundColor = '#ff8026';
                targetObjs.push(event.target);
                textarea.value = targetObjs.at(-1).innerText
            }
        } else {
        if (checkingSelected(targetObjs)) {
            for (let obj of targetObjs) {
                obj.style.backgroundColor = `#eee`;
            }
            targetObjs = [];
        }
        event.target.style.backgroundColor = '#ff8026';
        targetObjs.push(event.target);
        textarea.value = targetObjs.at(-1).innerText
        }
    }
});

document.addEventListener('keydown', (event) => {
    if (event.code == 'Delete' && targetObjs.length !=0 && document.activeElement != textarea) {
        for (let obj of targetObjs) {
            obj.parentElement.remove();
        }
        targetObjs = [];
    }
    if (event.code == 'Escape' && targetObjs != 0) {
        for (let obj of targetObjs) {
            obj.style.backgroundColor = '#eee';
        }
        targetObjs = [];
    };
});

textarea.addEventListener('keydown', (event) => {
    if (event.code == 'Enter' && targetObjs.length == 0 && textarea.value !== '') {
        event.preventDefault()
        let wrapperEl = document.createElement(`li`);
        let newEl = document.createElement(`p`);
        newEl.innerText = textarea.value;
        newEl.style.fontFamily = `monospace`
        wrapperEl.appendChild(newEl);
        listBooks.appendChild(wrapperEl);
        textarea.value = '';
    } else if (event.code == 'Enter' && targetObjs.length != 0) {
        event.preventDefault()
        targetObjs.at(-1).innerText = textarea.value;
        textarea.value = '';
        for (let obj of targetObjs) {
                obj.style.backgroundColor = `#eee`;
            }
        targetObjs = [];
    }
});

// Задание 2

// дополнительные функции:
// - реализовано контекстное меню только для данного задания
// - добавление новый элементов
// - удаление элементов
// - переименование элементов
// - так же отмена функций в момент добавления ввода имени через нажатие Esc

const tree = document.getElementById(`tree`);
let focusElementTree;

function clickTree (event) {
    if (event.target.tagName == 'SPAN') {
        event.target = event.target.parentElement;
        if (event.target.parentElement.children.length > 1) {
            if (event.target.parentElement.children[1].style.display == 'none') {
                for (let obj of event.target.parentElement.children) {
                    obj.style.display = 'block';
                }
            } else {
                for (let obj of event.target.parentElement.children) {
                    if (obj.tagName != 'SPAN') {
                        obj.style.display = 'none'
                    }
                }
            }
        }
    }
}

tree.addEventListener('click', clickTree);

const menu = document.getElementById('menu');
let flagMenu = false;

function closeMenu(event) {
    if (event.target !== menu) {
        menu.style.display = 'none';
        document.removeEventListener('click', closeMenu);
        // focusElementTree.style.fontWeight = 'normal';
        flagMenu = false;
    }
}

tree.addEventListener('contextmenu', (event) =>{
    if (event.target.tagName === 'SPAN') {
        event.preventDefault();
        if (!flagMenu) {
            document.addEventListener('click', closeMenu);
        }
        focusElementTree = event.target;
        flagMenu = true;
        menu.style.display = 'flex';
        menu.style.left = `${event.clientX}px`;
        menu.style.top = `${event.clientY}px`;
    }
});

function createTextareaEditTree(span, parent, value=null) {
    let textareaEditTree = document.createElement('textarea');
    textareaEditTree.rows = 1;
    textareaEditTree.value = value;
    textareaEditTree.addEventListener('keydown', (event) => {
        if (event.code === 'Enter') {
            event.preventDefault();
            span.innerText = textareaEditTree.value;
            textareaEditTree.replaceWith(span);
        }
        if (event.code === 'Escape') {
            if (value) {
                span.innerText = value;
                textareaEditTree.replaceWith(span);
            } else {
                parent.remove();
            }
        };
    });
    return textareaEditTree;
}

document.getElementById('menu-add').addEventListener('click', (event) => {
    let span = document.createElement('SPAN');
    let li = document.createElement('li');
    li.appendChild(span);
    focusElementTree.parentElement.parentElement.appendChild(li);
    let textarea = createTextareaEditTree(span, li);
    span.replaceWith(textarea);
    textarea.focus();
    focusElementTree = null;
});

document.getElementById('menu-addChild').addEventListener('click', (event) => {
    let span = document.createElement('SPAN');
    let li = document.createElement('li');
    li.appendChild(span);
    let ul;
    if (focusElementTree.nextElementSibling) {
        ul = focusElementTree.nextElementSibling;
    } else {
        ul = document.createElement('ul');
        focusElementTree.parentElement.appendChild(ul);
    }
    ul.appendChild(li);
    let textarea = createTextareaEditTree(span, li);
    span.replaceWith(textarea);
    textarea.focus();
    focusElementTree = null;
});

document.getElementById('menu-rename').addEventListener('click', (event) => {
    let textarea = createTextareaEditTree(focusElementTree, focusElementTree.parentElement, focusElementTree.innerText);
    focusElementTree.replaceWith(textarea);
    textarea.focus();
    focusElementTree = null;
});

document.getElementById('menu-del').addEventListener('click', (event) => {
    focusElementTree.parentElement.remove();
});

// Задание 3

const button_like = document.querySelector('.task3 button');
let likesCounter = 0;
const button_text = document.getElementById('task3-button-text');
button_text.innerText = `Like ${likesCounter}`;
button_like.addEventListener('click', (event) => {
    likesCounter++;
    button_text.innerText = `Like ${likesCounter}`;
    console.log(likesCounter);
});

// Задача 4

const buttons_del = document.getElementsByClassName('task4-conteiner-top-button');

for (let obj of buttons_del) {
    console.log(obj);
    console.log(obj.parentElement.parentElement);
    obj.addEventListener('click', (event) => {
        obj.parentElement.parentElement.remove();
    });
}


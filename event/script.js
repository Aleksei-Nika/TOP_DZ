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
                targetObjs.splice(targetObjs.indexOf(event.target));
            } else {
                event.target.style.backgroundColor = '#ff8026';
                targetObjs.push(event.target);
                textarea.value = targetObjs.at(-1).innerText
            }
        } else {
        if (checkingSelected(targetObjs)) {
            for (obj of targetObjs) {
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
        console.log(listBooks.children.length);
        for (obj of targetObjs) {
            if (listBooks.children.length > 1) {
                console.log('Удаление');
                obj.parentElement.remove();
            } else {
                console.log('Освобождение');
                obj.innerText = '';
            }
        }
    }
});

textarea.addEventListener('keydown', (event) => {
    if (event.code == 'Enter' && targetObjs.length == 0) {
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
        for (obj of targetObjs) {
                obj.style.backgroundColor = `#eee`;
            }
            targetObjs = [];
    }
});

// Задание 2
const tree = document.getElementById(`tree`);
let focusElementTree;

function mouseoverTree (event) {
    event.target.style.fontWeight = 'bold';
    focusElementTree = event.target;
}

tree.addEventListener('mouseover', mouseoverTree);

function mouseoutTree (event) {
    event.target.style.fontWeight = 'normal';
    focusElementTree = null;
}

tree.addEventListener('mouseout', mouseoutTree);

function clickTree (event) {
    if (event.target.children.length != 0) {
        if (event.target.children[0].style.display == 'none') {
            for (obj of event.target.children) {
                obj.style.display = 'block';
            }
        } else {
            for (obj of event.target.children) {
                obj.style.display = 'none';
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
        tree.addEventListener('mouseover', mouseoverTree);
        tree.addEventListener('mouseout', mouseoutTree);
        tree.addEventListener('click', clickTree);
        focusElementTree.style.fontWeight = 'normal';
        flagMenu = false;
    }
}

tree.addEventListener('contextmenu', (event) =>{
    event.preventDefault();
    if (!flagMenu) {
        document.addEventListener('click', closeMenu);
        tree.removeEventListener('mouseover', mouseoverTree);
        tree.removeEventListener('mouseout', mouseoutTree);
        tree.removeEventListener('click', clickTree);
    }
    flagMenu = true;
    object = event.target;
    menu.style.display = 'flex';
    menu.style.left = `${event.clientX}px`;
    menu.style.top = `${event.clientY}px`;
});

document.getElementById('menu-add').addEventListener('click', (event) => {
    console.log(focusElementTree.children);
});

document.getElementById('menu-addChild').addEventListener('click', (event) => {
    
});

document.getElementById('menu-rename').addEventListener('click', (event) => {
    if (focusElementTree.children.length === 0) {
        let edit = document.createElement('textarea');
        edit.value = focusElementTree.innerText;
        edit.rows = 1;
        edit.cols = 50;
        focusElementTree.replaceWith(edit);
    }
    focusElementTree.innerHTML = document.createElement('textarea');
});

document.getElementById('menu-del').addEventListener('click', (event) => {
    focusElementTree.remove();
});

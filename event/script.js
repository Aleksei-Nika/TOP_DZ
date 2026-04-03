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
                console.log(targetObjs);
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
        for (obj of targetObjs) {
            obj.parentElement.remove();
        }
        targetObjs = [];
    }
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
        for (obj of targetObjs) {
                obj.style.backgroundColor = `#eee`;
            }
        targetObjs = [];
    }
});

// Задание 2
const tree = document.getElementById(`tree`);
let focusElementTree;

function clickTree (event) {
    if (event.target.tagName == 'SPAN') {
        focusElementTree = event.target.parentElement;
        if (focusElementTree.children.length > 1) {
            if (focusElementTree.children[1].style.display == 'none') {
                for (obj of focusElementTree.children) {
                    obj.style.display = 'block';
                }
            } else {
                for (obj of focusElementTree.children) {
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
    event.preventDefault();
    if (!flagMenu) {
        document.addEventListener('click', closeMenu);
    }
    flagMenu = true;
    menu.style.display = 'flex';
    menu.style.left = `${event.clientX}px`;
    menu.style.top = `${event.clientY}px`;
});

document.getElementById('menu-add').addEventListener('click', (event) => {
    console.log(focusElementTree);
});

// document.getElementById('menu-addChild').addEventListener('click', (event) => {
    
// });

// document.getElementById('menu-rename').addEventListener('click', (event) => {
//     if (focusElementTree.children.length === 0) {
//         let edit = document.createElement('textarea');
//         edit.value = focusElementTree.innerText;
//         edit.rows = 1;
//         edit.cols = 50;
//         focusElementTree.replaceWith(edit);
//     }
//     focusElementTree.innerHTML = document.createElement('textarea');
// });

// document.getElementById('menu-del').addEventListener('click', (event) => {
//     focusElementTree.remove();
// });

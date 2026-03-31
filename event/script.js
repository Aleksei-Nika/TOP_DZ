const listBooks = document.getElementById(`listBooks`);

let targetObjs = [];
listBooks.addEventListener('click', (event) => {
    function clearingSelected(list) {
        for (el of list) {
            el.style.backgroundColor = 'white';
        }
    }
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
        }
    }
});

const textarea = document.querySelector(`.task1 textarea`);
textarea.addEventListener('keydown', (event) => {
    if (event.code == 'Enter') {
        event.preventDefault()
        let wrapperEl = document.createElement(`li`)
        let newEl = document.createElement(`p`)
        newEl.innerText = textarea.value;
        newEl.style.fontFamily = `monospace`
        wrapperEl.appendChild(newEl);
        listBooks.appendChild(wrapperEl);
    }
});